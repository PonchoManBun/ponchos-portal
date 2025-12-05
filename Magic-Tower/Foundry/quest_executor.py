"""
Quest Executor - Sequential Lord Coordination Engine

Inspired by n8n's WorkflowExecute (workflow-execute.ts)
Executes multi-step quests by coordinating Lords in sequence.

Architecture:
- Stack-based execution (FIFO queue)
- State persistence-ready (designed for SQLite)
- Lifecycle hooks for observability
- Error handling with retry logic
"""

import asyncio
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Callable, Set
from datetime import datetime
import httpx

try:
    from quest_persistence import QuestRepository
    PERSISTENCE_AVAILABLE = True
except ImportError:
    PERSISTENCE_AVAILABLE = False
    QuestRepository = None


class ExecutionStatus(str, Enum):
    """Quest/Lord execution status"""
    NEW = "new"
    RUNNING = "running"
    SUCCESS = "success"
    ERROR = "error"
    WAITING = "waiting"
    CANCELED = "canceled"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class ErrorMode(str, Enum):
    """How to handle Lord execution errors"""
    STOP = "stop"                    # Stop quest on error (default)
    CONTINUE = "continue"            # Continue with next Lord
    CONTINUE_WITH_INPUT = "continue_with_input"  # Pass input data through


@dataclass
class LordRetryConfig:
    """Retry configuration for a Lord (per n8n pattern)"""
    max_tries: int = 1
    wait_between_tries_ms: int = 0
    
    def __post_init__(self):
        # Enforce n8n-style limits
        self.max_tries = min(5, max(1, self.max_tries))
        self.wait_between_tries_ms = min(5000, max(0, self.wait_between_tries_ms))


@dataclass
class LordStep:
    """A single Lord invocation in a quest chain"""
    lord_name: str
    tool_name: str
    on_error: ErrorMode = ErrorMode.STOP
    retry_config: LordRetryConfig = field(default_factory=LordRetryConfig)
    
    # Execution metadata (set during execution)
    status: ExecutionStatus = ExecutionStatus.NEW
    start_time: Optional[float] = None
    execution_time: Optional[float] = None
    run_index: int = 0
    error: Optional[Dict[str, Any]] = None
    data: Optional[Dict[str, Any]] = None


@dataclass
class QuestExecutionData:
    """
    Execution state for a quest (n8n's IRunExecutionData)
    
    Designed for SQLite persistence:
    - All fields are JSON-serializable
    - Timestamps for audit trail
    - Complete execution history in run_data
    """
    quest_id: str
    quest_type: str
    
    # Execution stack (FIFO queue of pending steps)
    execution_stack: List[LordStep] = field(default_factory=list)
    
    # Historical run data (completed Lord invocations)
    # Structure: { "lord_name": { "run_index": <LordStep data> } }
    run_data: Dict[str, Dict[int, Dict[str, Any]]] = field(default_factory=dict)
    
    # Waiting queue for multi-input Lords (future use)
    waiting_execution: Dict[str, Any] = field(default_factory=dict)
    
    # Quest metadata
    status: ExecutionStatus = ExecutionStatus.NEW
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    last_lord_executed: Optional[str] = None
    error: Optional[Dict[str, Any]] = None
    
    # Input data from client
    input_data: Dict[str, Any] = field(default_factory=dict)
    
    # Final output data
    output_data: Optional[Dict[str, Any]] = None


class ExecutionHooks:
    """
    Lifecycle hooks for observability (n8n pattern)
    
    Future: WebSocket event emission, logging, metrics
    """
    def __init__(self):
        self._hooks: Dict[str, List[Callable]] = {
            "quest_started": [],
            "quest_finished": [],
            "lord_invoked": [],
            "lord_completed": [],
            "lord_error": [],
        }
    
    def register(self, event: str, callback: Callable):
        """Register a callback for an event"""
        if event in self._hooks:
            self._hooks[event].append(callback)
    
    async def emit(self, event: str, *args, **kwargs):
        """Emit an event to all registered callbacks"""
        for callback in self._hooks.get(event, []):
            if asyncio.iscoroutinefunction(callback):
                await callback(*args, **kwargs)
            else:
                callback(*args, **kwargs)


class QuestExecutor:
    """
    Sequential Lord coordination engine (n8n's WorkflowExecute)
    
    Executes quests by:
    1. Popping Lord from execution stack
    2. Invoking Lord via JSON-RPC
    3. Storing result in run_data
    4. Pushing next Lord to stack
    5. Repeating until stack empty
    """
    
    # Lord registry (name -> port)
    LORD_REGISTRY = {
        "architect": 8001,
        "scribe": 8002,
        "forge_master": 8003,
        "sentinel": 8004,
    }
    
    def __init__(self, hooks: Optional[ExecutionHooks] = None, repository: Optional['QuestRepository'] = None):
        self.hooks = hooks or ExecutionHooks()
        self.status = ExecutionStatus.NEW
        self.repository = repository
        self._auto_save = repository is not None  # Enable auto-save if repository provided
    
    async def execute_quest(self, quest_data: QuestExecutionData) -> QuestExecutionData:
        """
        Execute a quest by processing the execution stack
        
        Args:
            quest_data: Quest with pre-populated execution_stack
        
        Returns:
            Updated quest_data with run_data and output_data
        """
        quest_data.status = ExecutionStatus.RUNNING
        quest_data.start_time = time.time()
        
        await self.hooks.emit("quest_started", quest_data)
        
        # Main execution loop (n8n's executionLoop)
        while quest_data.execution_stack:
            # Pop next Lord step
            current_step = quest_data.execution_stack.pop(0)
            
            # Execute Lord with retry logic
            try:
                await self._execute_lord_step(current_step, quest_data)
            except Exception as e:
                # Handle error based on error mode
                if current_step.on_error == ErrorMode.STOP:
                    quest_data.status = ExecutionStatus.ERROR
                    quest_data.error = {
                        "lord": current_step.lord_name,
                        "tool": current_step.tool_name,
                        "message": str(e),
                    }
                    await self.hooks.emit("quest_finished", quest_data)
                    break
                elif current_step.on_error == ErrorMode.CONTINUE:
                    # Skip this Lord, continue to next
                    continue
                elif current_step.on_error == ErrorMode.CONTINUE_WITH_INPUT:
                    # Pass input data as output, continue
                    current_step.data = self._get_previous_output(quest_data)
            
            # Update quest state
            quest_data.last_lord_executed = current_step.lord_name
            
            # Store result in run_data
            if current_step.lord_name not in quest_data.run_data:
                quest_data.run_data[current_step.lord_name] = {}
            
            quest_data.run_data[current_step.lord_name][current_step.run_index] = {
                "status": current_step.status,
                "start_time": current_step.start_time,
                "execution_time": current_step.execution_time,
                "data": current_step.data,
                "error": current_step.error,
            }
            
            # Auto-save quest state after each Lord execution
            if self._auto_save and self.repository:
                self.repository.save_quest(quest_data)
                self.repository.save_lord_run(
                    quest_id=quest_data.quest_id,
                    lord_name=current_step.lord_name,
                    tool_name=current_step.tool_name,
                    run_index=current_step.run_index,
                    status="success" if current_step.status == ExecutionStatus.SUCCESS else "error",
                    input_data=self._get_previous_output(quest_data) or quest_data.input_data,
                    output_data=current_step.data,
                    error_message=current_step.error.get("message") if current_step.error else None,
                    start_time=current_step.start_time,
                    end_time=current_step.start_time + current_step.execution_time if current_step.execution_time else None
                )
        
        # Quest completed
        if quest_data.status == ExecutionStatus.RUNNING:
            quest_data.status = ExecutionStatus.COMPLETED
        
        quest_data.end_time = time.time()
        quest_data.output_data = self._get_previous_output(quest_data)
        
        # Save final quest state
        if self._auto_save and self.repository:
            self.repository.save_quest(quest_data)
        
        await self.hooks.emit("quest_finished", quest_data)
        
        return quest_data
    
    async def _execute_lord_step(self, step: LordStep, quest_data: QuestExecutionData):
        """
        Execute a single Lord step with retry logic (n8n pattern)
        
        Args:
            step: Lord step to execute
            quest_data: Current quest execution state
        """
        step.start_time = time.time()
        step.status = ExecutionStatus.RUNNING
        
        await self.hooks.emit("lord_invoked", step, quest_data)
        
        # Get input data from previous Lord
        input_data = self._get_previous_output(quest_data)
        
        # Merge with quest input for first Lord
        if not quest_data.run_data:
            input_data = {**quest_data.input_data, **(input_data or {})}
        
        # Retry loop (n8n pattern)
        last_error = None
        for attempt in range(step.retry_config.max_tries):
            try:
                # Delay before retry (skip on first attempt)
                if attempt > 0 and step.retry_config.wait_between_tries_ms > 0:
                    await asyncio.sleep(step.retry_config.wait_between_tries_ms / 1000)
                
                # Invoke Lord via JSON-RPC
                result = await self._call_lord_jsonrpc(
                    step.lord_name,
                    step.tool_name,
                    input_data or {}
                )
                
                # Success!
                step.status = ExecutionStatus.SUCCESS
                step.data = result
                step.execution_time = time.time() - step.start_time
                
                await self.hooks.emit("lord_completed", step, quest_data)
                return
            
            except Exception as e:
                last_error = e
                if attempt < step.retry_config.max_tries - 1:
                    # Not final attempt, will retry
                    continue
        
        # All retries failed
        step.status = ExecutionStatus.ERROR
        step.execution_time = time.time() - step.start_time
        step.error = {
            "message": str(last_error),
            "attempts": step.retry_config.max_tries,
        }
        
        await self.hooks.emit("lord_error", step, quest_data)
        raise last_error
    
    async def _call_lord_jsonrpc(
        self,
        lord_name: str,
        tool_name: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Call a Lord's tool via JSON-RPC 2.0 (MCP protocol)
        
        Args:
            lord_name: Name of Lord (e.g., "architect")
            tool_name: Tool to invoke (e.g., "design_system")
            params: Tool parameters
        
        Returns:
            Tool result
        
        Raises:
            Exception: If Lord returns error or unreachable
        """
        port = self.LORD_REGISTRY.get(lord_name)
        if not port:
            raise ValueError(f"Unknown Lord: {lord_name}")
        
        url = f"http://localhost:{port}/mcp"
        
        # MCP protocol format: tools/call with nested tool name and arguments
        request_payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": params,
            },
            "id": 1,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=request_payload, timeout=30.0)
            response.raise_for_status()
            
            rpc_response = response.json()
            
            # Check for JSON-RPC error
            if "error" in rpc_response and rpc_response["error"] is not None:
                error = rpc_response["error"]
                raise Exception(f"Lord {lord_name} error: {error.get('message', 'Unknown error')}")
            
            return rpc_response.get("result", {})
    
    def _get_previous_output(self, quest_data: QuestExecutionData) -> Optional[Dict[str, Any]]:
        """
        Get output data from the last executed Lord
        
        Args:
            quest_data: Current quest state
        
        Returns:
            Last Lord's output data, or None if no Lords executed yet
        """
        if not quest_data.last_lord_executed:
            return None
        
        lord_runs = quest_data.run_data.get(quest_data.last_lord_executed, {})
        if not lord_runs:
            return None
        
        # Get latest run
        latest_run_index = max(lord_runs.keys())
        return lord_runs[latest_run_index].get("data")
    
    # ============================================================
    # QUEST PAUSE/RESUME/REPLAY
    # ============================================================
    
    async def pause_quest(self, quest_id: str) -> bool:
        """
        Pause a running quest and save snapshot.
        
        Args:
            quest_id: Quest identifier
            
        Returns:
            True if paused successfully
            
        Note: Quest must be manually stopped externally before calling pause.
        This method saves the current state for later resumption.
        """
        if not self.repository:
            raise RuntimeError("Cannot pause quest: no repository configured")
        
        # Load current quest state
        quest_data = self.repository.load_quest(quest_id)
        if not quest_data:
            return False
        
        # Mark as paused
        quest_data.status = ExecutionStatus.PAUSED
        quest_data.end_time = time.time()
        
        # Save snapshot
        self.repository.save_snapshot(
            quest_id=quest_id,
            run_data=quest_data.run_data,
            execution_stack=quest_data.execution_stack,
            reason="pause"
        )
        
        # Update quest status
        self.repository.save_quest(quest_data)
        
        return True
    
    async def resume_quest(self, quest_id: str) -> QuestExecutionData:
        """
        Resume a paused quest from latest snapshot.
        
        Args:
            quest_id: Quest identifier
            
        Returns:
            Updated quest data after resuming execution
        """
        if not self.repository:
            raise RuntimeError("Cannot resume quest: no repository configured")
        
        # Load quest and snapshot
        quest_data = self.repository.load_quest(quest_id)
        if not quest_data:
            raise ValueError(f"Quest {quest_id} not found")
        
        if quest_data.status != ExecutionStatus.PAUSED:
            raise ValueError(f"Quest {quest_id} is not paused (status: {quest_data.status})")
        
        # Load latest snapshot
        snapshot = self.repository.load_latest_snapshot(quest_id)
        if snapshot:
            run_data, execution_stack = snapshot
            quest_data.run_data = run_data
            quest_data.execution_stack = execution_stack
        
        # Reset timing
        quest_data.status = ExecutionStatus.RUNNING
        quest_data.start_time = time.time()
        quest_data.end_time = None
        
        # Resume execution
        return await self.execute_quest(quest_data)
    
    async def replay_quest(self, quest_id: str, from_lord: Optional[str] = None) -> QuestExecutionData:
        """
        Replay a quest from the beginning or from a specific Lord.
        
        Args:
            quest_id: Quest identifier
            from_lord: Optional Lord name to start from (replays from that point)
            
        Returns:
            Updated quest data after replay
        """
        if not self.repository:
            raise RuntimeError("Cannot replay quest: no repository configured")
        
        # Load original quest
        original_quest = self.repository.load_quest(quest_id)
        if not original_quest:
            raise ValueError(f"Quest {quest_id} not found")
        
        # Create new quest data with same input
        new_quest_id = f"{quest_id}-replay-{int(time.time())}"
        
        if from_lord:
            # Find where to start in execution stack
            start_index = None
            for i, step in enumerate(original_quest.execution_stack):
                if step.lord_name == from_lord:
                    start_index = i
                    break
            
            if start_index is None:
                raise ValueError(f"Lord {from_lord} not found in quest execution stack")
            
            # Build execution stack from this point
            execution_stack = original_quest.execution_stack[start_index:]
            
            # Use run_data up to this point as starting context
            run_data = {}
            for lord_name, runs in original_quest.run_data.items():
                if lord_name != from_lord:
                    run_data[lord_name] = runs
        else:
            # Full replay from beginning
            execution_stack = list(original_quest.execution_stack)
            run_data = {}
        
        replay_quest_data = QuestExecutionData(
            quest_id=new_quest_id,
            quest_type=original_quest.quest_type,
            input_data=original_quest.input_data,
            execution_stack=execution_stack,
            run_data=run_data
        )
        
        # Execute replay
        return await self.execute_quest(replay_quest_data)
    
    def load_quest(self, quest_id: str) -> Optional[QuestExecutionData]:
        """
        Load quest state from repository.
        
        Args:
            quest_id: Quest identifier
            
        Returns:
            QuestExecutionData if found, None otherwise
        """
        if not self.repository:
            raise RuntimeError("Cannot load quest: no repository configured")
        
        return self.repository.load_quest(quest_id)


# Example: Build a quest chain
def build_microservice_design_quest(requirements: str) -> QuestExecutionData:
    """
    Build a quest for: Client -> Architect -> Forge Master -> Sentinel
    
    Quest flow:
    1. Architect designs system architecture
    2. Forge Master generates code from design
    3. Sentinel reviews code for quality
    """
    quest_data = QuestExecutionData(
        quest_id="q-001",
        quest_type="design_microservice",
        input_data={"requirements": requirements},
        execution_stack=[
            LordStep(
                lord_name="architect",
                tool_name="design_system",
                on_error=ErrorMode.STOP,  # Critical - must succeed
                retry_config=LordRetryConfig(max_tries=3, wait_between_tries_ms=1000),
            ),
            LordStep(
                lord_name="forge_master",
                tool_name="generate_code",
                on_error=ErrorMode.STOP,
                retry_config=LordRetryConfig(max_tries=2, wait_between_tries_ms=2000),
            ),
            LordStep(
                lord_name="sentinel",
                tool_name="review_code",
                on_error=ErrorMode.STOP,
                retry_config=LordRetryConfig(max_tries=1, wait_between_tries_ms=0),
            ),
        ],
    )
    
    return quest_data


# Example: Execution with hooks
async def main():
    """Demo: Execute a multi-Lord quest with observability"""
    
    # Set up hooks for logging
    hooks = ExecutionHooks()
    
    def on_quest_started(quest_data: QuestExecutionData):
        print(f"🎯 Quest {quest_data.quest_id} started: {quest_data.quest_type}")
    
    def on_lord_invoked(step: LordStep, quest_data: QuestExecutionData):
        print(f"  ⚔️  Invoking Lord {step.lord_name}.{step.tool_name}")
    
    def on_lord_completed(step: LordStep, quest_data: QuestExecutionData):
        print(f"  ✅ Lord {step.lord_name} completed in {step.execution_time:.2f}s")
    
    def on_lord_error(step: LordStep, quest_data: QuestExecutionData):
        print(f"  ❌ Lord {step.lord_name} failed: {step.error}")
    
    def on_quest_finished(quest_data: QuestExecutionData):
        if quest_data.end_time and quest_data.start_time:
            total_time = quest_data.end_time - quest_data.start_time
            print(f"🏁 Quest {quest_data.quest_id} finished: {quest_data.status} ({total_time:.2f}s)")
        else:
            print(f"🏁 Quest {quest_data.quest_id} finished: {quest_data.status}")
    
    hooks.register("quest_started", on_quest_started)
    hooks.register("lord_invoked", on_lord_invoked)
    hooks.register("lord_completed", on_lord_completed)
    hooks.register("lord_error", on_lord_error)
    hooks.register("quest_finished", on_quest_finished)
    
    # Build quest
    quest = build_microservice_design_quest(
        requirements="Build a REST API for user authentication with JWT tokens"
    )
    
    # Execute quest
    executor = QuestExecutor(hooks=hooks)
    result = await executor.execute_quest(quest)
    
    # Print results
    print("\n📊 Quest Results:")
    print(f"  Status: {result.status}")
    print(f"  Lords executed: {len(result.run_data)}")
    for lord_name, runs in result.run_data.items():
        for run_index, run_data in runs.items():
            print(f"    - {lord_name} (run {run_index}): {run_data['status']}")


if __name__ == "__main__":
    asyncio.run(main())
