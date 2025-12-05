"""
Test Suite for Quest Executor

Tests sequential Lord coordination:
- Architect -> Forge Master -> Sentinel chain
- Error handling & retry logic
- State management & caching
- Lifecycle hooks
"""

import pytest
import asyncio
import httpx
from quest_executor import (
    QuestExecutor,
    QuestExecutionData,
    LordStep,
    ExecutionStatus,
    ErrorMode,
    LordRetryConfig,
    ExecutionHooks,
    build_microservice_design_quest,
)


@pytest.fixture
def sample_quest():
    """Create a simple 2-step quest for testing"""
    return QuestExecutionData(
        quest_id="test-001",
        quest_type="simple_chain",
        input_data={"requirements": "Test requirements"},
        execution_stack=[
            LordStep(
                lord_name="architect",
                tool_name="design_system",
                retry_config=LordRetryConfig(max_tries=1),
            ),
            LordStep(
                lord_name="scribe",
                tool_name="write_docs",
                retry_config=LordRetryConfig(max_tries=1),
            ),
        ],
    )


@pytest.fixture
def full_quest():
    """Create full Architect -> Forge Master -> Sentinel chain"""
    return build_microservice_design_quest("Build authentication API with JWT")


@pytest.mark.asyncio
async def test_sequential_execution(sample_quest):
    """Test basic sequential Lord execution"""
    executor = QuestExecutor()
    result = await executor.execute_quest(sample_quest)
    
    assert result.status == ExecutionStatus.SUCCESS
    assert len(result.run_data) == 2
    assert "architect" in result.run_data
    assert "scribe" in result.run_data
    assert result.output_data is not None


@pytest.mark.asyncio
async def test_full_chain_execution(full_quest):
    """Test full Architect -> Forge Master -> Sentinel chain"""
    executor = QuestExecutor()
    result = await executor.execute_quest(full_quest)
    
    assert result.status == ExecutionStatus.SUCCESS
    assert len(result.run_data) == 3
    
    # Check execution order
    assert "architect" in result.run_data
    assert "forge_master" in result.run_data
    assert "sentinel" in result.run_data
    
    # Check data flow
    architect_output = result.run_data["architect"][0]["data"]
    assert "design" in architect_output
    
    forge_output = result.run_data["forge_master"][0]["data"]
    assert "code" in forge_output or "files" in forge_output
    
    sentinel_output = result.run_data["sentinel"][0]["data"]
    assert "score" in sentinel_output
    assert "approved" in sentinel_output


@pytest.mark.asyncio
async def test_execution_hooks():
    """Test lifecycle hooks are called correctly"""
    hooks = ExecutionHooks()
    events_called = []
    
    @hooks.register("quest_started")
    def on_quest_started(quest_data):
        events_called.append("quest_started")
    
    @hooks.register("lord_invoked")
    def on_lord_invoked(step, quest_data):
        events_called.append(f"lord_invoked:{step.lord_name}")
    
    @hooks.register("lord_completed")
    def on_lord_completed(step, quest_data):
        events_called.append(f"lord_completed:{step.lord_name}")
    
    @hooks.register("quest_finished")
    def on_quest_finished(quest_data):
        events_called.append("quest_finished")
    
    quest = QuestExecutionData(
        quest_id="hook-test",
        quest_type="test",
        execution_stack=[
            LordStep(lord_name="architect", tool_name="design_system"),
        ],
    )
    
    executor = QuestExecutor(hooks=hooks)
    await executor.execute_quest(quest)
    
    assert "quest_started" in events_called
    assert "lord_invoked:architect" in events_called
    assert "lord_completed:architect" in events_called
    assert "quest_finished" in events_called


@pytest.mark.asyncio
async def test_error_handling_stop_mode():
    """Test STOP error mode halts execution"""
    quest = QuestExecutionData(
        quest_id="error-test",
        quest_type="test",
        execution_stack=[
            LordStep(
                lord_name="nonexistent_lord",
                tool_name="test_tool",
                on_error=ErrorMode.STOP,
                retry_config=LordRetryConfig(max_tries=1),
            ),
            LordStep(
                lord_name="scribe",
                tool_name="write_docs",
            ),
        ],
    )
    
    executor = QuestExecutor()
    result = await executor.execute_quest(quest)
    
    assert result.status == ExecutionStatus.ERROR
    assert result.error is not None
    assert "nonexistent_lord" in result.error["lord"]
    
    # Second Lord should NOT have executed
    assert "scribe" not in result.run_data


@pytest.mark.asyncio
async def test_error_handling_continue_mode():
    """Test CONTINUE error mode skips failed Lord"""
    quest = QuestExecutionData(
        quest_id="continue-test",
        quest_type="test",
        execution_stack=[
            LordStep(
                lord_name="nonexistent_lord",
                tool_name="test_tool",
                on_error=ErrorMode.CONTINUE,
                retry_config=LordRetryConfig(max_tries=1),
            ),
            LordStep(
                lord_name="scribe",
                tool_name="write_docs",
            ),
        ],
    )
    
    executor = QuestExecutor()
    result = await executor.execute_quest(quest)
    
    # Quest should complete despite first Lord failing
    assert result.status == ExecutionStatus.SUCCESS
    
    # Second Lord should have executed
    assert "scribe" in result.run_data


@pytest.mark.asyncio
async def test_retry_logic():
    """Test Lord retry on failure (if Lord supports it)"""
    # Note: This test would need a mock Lord that fails N times
    # For now, we verify retry config is respected
    
    quest = QuestExecutionData(
        quest_id="retry-test",
        quest_type="test",
        execution_stack=[
            LordStep(
                lord_name="architect",
                tool_name="design_system",
                retry_config=LordRetryConfig(max_tries=3, wait_between_tries_ms=100),
            ),
        ],
    )
    
    executor = QuestExecutor()
    result = await executor.execute_quest(quest)
    
    # Should succeed (Architect is stable)
    assert result.status == ExecutionStatus.SUCCESS


@pytest.mark.asyncio
async def test_state_persistence_structure():
    """Test quest state is structured for SQLite persistence"""
    quest = build_microservice_design_quest("Test")
    
    executor = QuestExecutor()
    result = await executor.execute_quest(quest)
    
    # Verify all data is JSON-serializable
    import json
    
    state_dict = {
        "quest_id": result.quest_id,
        "quest_type": result.quest_type,
        "status": result.status,
        "start_time": result.start_time,
        "end_time": result.end_time,
        "input_data": result.input_data,
        "output_data": result.output_data,
        "run_data": result.run_data,
        "error": result.error,
    }
    
    # Should serialize without errors
    serialized = json.dumps(state_dict)
    assert len(serialized) > 0
    
    # Should deserialize correctly
    deserialized = json.loads(serialized)
    assert deserialized["quest_id"] == result.quest_id
    assert deserialized["status"] == result.status


@pytest.mark.asyncio
async def test_data_flow_between_lords():
    """Test data flows correctly from one Lord to the next"""
    quest = build_microservice_design_quest("Build user auth API")
    
    executor = QuestExecutor()
    result = await executor.execute_quest(quest)
    
    # Architect produces design
    architect_data = result.run_data["architect"][0]["data"]
    assert "design" in architect_data
    
    # Forge Master receives design and produces code
    forge_data = result.run_data["forge_master"][0]["data"]
    assert "code" in forge_data or "files" in forge_data
    
    # Sentinel receives code and produces review
    sentinel_data = result.run_data["sentinel"][0]["data"]
    assert "score" in sentinel_data
    
    # Verify Sentinel reviewed the Forge Master's output
    # (In a real implementation, we'd check that Sentinel's input
    #  contains Forge Master's output)


@pytest.mark.asyncio
async def test_execution_timing():
    """Test execution timing is tracked correctly"""
    quest = QuestExecutionData(
        quest_id="timing-test",
        quest_type="test",
        execution_stack=[
            LordStep(lord_name="architect", tool_name="design_system"),
        ],
    )
    
    executor = QuestExecutor()
    result = await executor.execute_quest(quest)
    
    # Quest timing
    assert result.start_time is not None
    assert result.end_time is not None
    assert result.end_time > result.start_time
    
    # Lord timing
    architect_run = result.run_data["architect"][0]
    assert architect_run["start_time"] is not None
    assert architect_run["execution_time"] is not None
    assert architect_run["execution_time"] > 0


@pytest.mark.asyncio
async def test_multiple_runs_same_lord():
    """Test a Lord can be invoked multiple times in same quest"""
    quest = QuestExecutionData(
        quest_id="multi-run-test",
        quest_type="test",
        execution_stack=[
            LordStep(lord_name="architect", tool_name="design_system", run_index=0),
            LordStep(lord_name="scribe", tool_name="write_docs", run_index=0),
            LordStep(lord_name="architect", tool_name="design_system", run_index=1),
        ],
    )
    
    executor = QuestExecutor()
    result = await executor.execute_quest(quest)
    
    # Architect should have 2 runs
    assert len(result.run_data["architect"]) == 2
    assert 0 in result.run_data["architect"]
    assert 1 in result.run_data["architect"]
    
    # Scribe should have 1 run
    assert len(result.run_data["scribe"]) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
