"""
Quest State Persistence Layer

SQLite-based persistence for QuestExecutor state management.
Enables quest pause/resume/replay and historical analysis.

Based on n8n workflow execution storage patterns.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import asdict
from contextlib import contextmanager

from quest_executor import QuestExecutionData, ExecutionStatus, LordStep


# Database schema version for migrations
SCHEMA_VERSION = 1


class QuestRepository:
    """
    Repository pattern for quest state persistence.
    
    Responsibilities:
    - Quest execution CRUD operations
    - Lord run tracking
    - State serialization/deserialization
    - Query interface for analytics
    """
    
    def __init__(self, db_path: str = "quests.db"):
        """
        Initialize repository with SQLite database.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self._init_database()
    
    def _init_database(self):
        """Create database schema if not exists."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Quest executions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS quest_executions (
                    quest_id TEXT PRIMARY KEY,
                    quest_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    
                    -- Timing
                    start_time REAL,
                    end_time REAL,
                    duration_seconds REAL,
                    
                    -- Data
                    input_data TEXT NOT NULL,  -- JSON
                    output_data TEXT,           -- JSON
                    
                    -- Stack state
                    execution_stack TEXT NOT NULL,  -- JSON array of LordStep
                    
                    -- Metadata
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    schema_version INTEGER NOT NULL
                )
            """)
            
            # Lord runs table (one row per Lord invocation)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS lord_runs (
                    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    quest_id TEXT NOT NULL,
                    
                    -- Lord details
                    lord_name TEXT NOT NULL,
                    tool_name TEXT NOT NULL,
                    run_index INTEGER NOT NULL,  -- Multiple runs of same Lord
                    
                    -- Execution
                    status TEXT NOT NULL,        -- success, error, skipped
                    start_time REAL NOT NULL,
                    end_time REAL,
                    duration_seconds REAL,
                    
                    -- Data
                    input_data TEXT NOT NULL,    -- JSON
                    output_data TEXT,             -- JSON
                    error_message TEXT,
                    
                    -- Retry tracking
                    attempt_number INTEGER NOT NULL DEFAULT 1,
                    max_attempts INTEGER NOT NULL,
                    
                    -- Timestamps
                    created_at TEXT NOT NULL,
                    
                    FOREIGN KEY (quest_id) REFERENCES quest_executions(quest_id)
                )
            """)
            
            # Quest state snapshots (for pause/resume)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS quest_snapshots (
                    snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    quest_id TEXT NOT NULL,
                    
                    -- Complete state dump
                    run_data TEXT NOT NULL,      -- JSON: full run_data dict
                    execution_stack TEXT NOT NULL,  -- JSON: current stack
                    
                    -- Snapshot metadata
                    snapshot_reason TEXT NOT NULL,  -- 'pause', 'checkpoint', 'error'
                    created_at TEXT NOT NULL,
                    
                    FOREIGN KEY (quest_id) REFERENCES quest_executions(quest_id)
                )
            """)
            
            # Indexes for performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_quest_status 
                ON quest_executions(status)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_quest_created 
                ON quest_executions(created_at DESC)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_lord_runs_quest 
                ON lord_runs(quest_id, run_index)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_lord_runs_lord 
                ON lord_runs(lord_name, created_at DESC)
            """)
            
            conn.commit()
    
    @contextmanager
    def _get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
        finally:
            conn.close()
    
    # ============================================================
    # QUEST EXECUTION CRUD
    # ============================================================
    
    def save_quest(self, quest_data: QuestExecutionData) -> None:
        """
        Save or update quest execution state.
        
        Args:
            quest_data: Quest execution data to persist
        """
        now = datetime.now().isoformat()
        
        # Serialize complex fields
        input_json = json.dumps(quest_data.input_data)
        output_json = json.dumps(quest_data.output_data) if quest_data.output_data else None
        stack_json = json.dumps([self._serialize_lord_step(step) for step in quest_data.execution_stack])
        
        # Calculate duration if finished
        duration = None
        if quest_data.start_time and quest_data.end_time:
            duration = quest_data.end_time - quest_data.start_time
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if quest exists
            cursor.execute("SELECT quest_id FROM quest_executions WHERE quest_id = ?", 
                          (quest_data.quest_id,))
            exists = cursor.fetchone()
            
            if exists:
                # Update existing quest
                cursor.execute("""
                    UPDATE quest_executions
                    SET status = ?,
                        end_time = ?,
                        duration_seconds = ?,
                        output_data = ?,
                        execution_stack = ?,
                        updated_at = ?
                    WHERE quest_id = ?
                """, (
                    quest_data.status.value,
                    quest_data.end_time,
                    duration,
                    output_json,
                    stack_json,
                    now,
                    quest_data.quest_id
                ))
            else:
                # Insert new quest
                cursor.execute("""
                    INSERT INTO quest_executions (
                        quest_id, quest_type, status,
                        start_time, end_time, duration_seconds,
                        input_data, output_data,
                        execution_stack,
                        created_at, updated_at, schema_version
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    quest_data.quest_id,
                    quest_data.quest_type,
                    quest_data.status.value,
                    quest_data.start_time,
                    quest_data.end_time,
                    duration,
                    input_json,
                    output_json,
                    stack_json,
                    now,
                    now,
                    SCHEMA_VERSION
                ))
            
            conn.commit()
    
    def load_quest(self, quest_id: str) -> Optional[QuestExecutionData]:
        """
        Load quest execution state from database.
        
        Args:
            quest_id: Quest identifier
            
        Returns:
            QuestExecutionData if found, None otherwise
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT quest_id, quest_type, status,
                       start_time, end_time,
                       input_data, output_data, execution_stack
                FROM quest_executions
                WHERE quest_id = ?
            """, (quest_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            # Deserialize JSON fields
            input_data = json.loads(row["input_data"])
            output_data = json.loads(row["output_data"]) if row["output_data"] else None
            stack_data = json.loads(row["execution_stack"])
            
            # Reconstruct execution stack
            execution_stack = [self._deserialize_lord_step(step) for step in stack_data]
            
            # Load run_data from lord_runs table
            run_data = self._load_run_data(quest_id, conn)
            
            return QuestExecutionData(
                quest_id=row["quest_id"],
                quest_type=row["quest_type"],
                status=ExecutionStatus(row["status"]),
                start_time=row["start_time"],
                end_time=row["end_time"],
                input_data=input_data,
                output_data=output_data,
                execution_stack=execution_stack,
                run_data=run_data
            )
    
    def delete_quest(self, quest_id: str) -> bool:
        """
        Delete quest and all associated data.
        
        Args:
            quest_id: Quest identifier
            
        Returns:
            True if deleted, False if not found
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Delete lord runs first (foreign key)
            cursor.execute("DELETE FROM lord_runs WHERE quest_id = ?", (quest_id,))
            cursor.execute("DELETE FROM quest_snapshots WHERE quest_id = ?", (quest_id,))
            
            # Delete quest
            cursor.execute("DELETE FROM quest_executions WHERE quest_id = ?", (quest_id,))
            
            deleted = cursor.rowcount > 0
            conn.commit()
            return deleted
    
    # ============================================================
    # LORD RUN TRACKING
    # ============================================================
    
    def save_lord_run(
        self,
        quest_id: str,
        lord_name: str,
        tool_name: str,
        run_index: int,
        status: str,
        input_data: Dict[str, Any],
        output_data: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
        attempt_number: int = 1,
        max_attempts: int = 3
    ) -> int:
        """
        Save Lord execution run to database.
        
        Args:
            quest_id: Parent quest identifier
            lord_name: Name of Lord (e.g., 'Lord Architect')
            tool_name: Tool invoked (e.g., 'design_system')
            run_index: Execution index for this Lord in quest
            status: 'success', 'error', 'skipped'
            input_data: Input data passed to Lord
            output_data: Output data from Lord
            error_message: Error message if failed
            start_time: Start timestamp
            end_time: End timestamp
            attempt_number: Current attempt (for retries)
            max_attempts: Maximum retry attempts
            
        Returns:
            run_id: Database ID of saved run
        """
        now = datetime.now().isoformat()
        
        # Calculate duration
        duration = None
        if start_time and end_time:
            duration = end_time - start_time
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO lord_runs (
                    quest_id, lord_name, tool_name, run_index,
                    status, start_time, end_time, duration_seconds,
                    input_data, output_data, error_message,
                    attempt_number, max_attempts, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                quest_id,
                lord_name,
                tool_name,
                run_index,
                status,
                start_time,
                end_time,
                duration,
                json.dumps(input_data),
                json.dumps(output_data) if output_data else None,
                error_message,
                attempt_number,
                max_attempts,
                now
            ))
            
            run_id = cursor.lastrowid
            conn.commit()
            return run_id
    
    def _load_run_data(self, quest_id: str, conn: sqlite3.Connection) -> Dict[str, Dict[int, Dict[str, Any]]]:
        """
        Load run_data structure from lord_runs table.
        
        Args:
            quest_id: Quest identifier
            conn: Database connection
            
        Returns:
            run_data dict matching QuestExecutionData structure
        """
        cursor = conn.cursor()
        cursor.execute("""
            SELECT lord_name, run_index, 
                   input_data, output_data, error_message,
                   start_time, end_time, duration_seconds, status
            FROM lord_runs
            WHERE quest_id = ?
            ORDER BY run_index ASC
        """, (quest_id,))
        
        run_data: Dict[str, Dict[int, Dict[str, Any]]] = {}
        
        for row in cursor.fetchall():
            lord_name = row["lord_name"]
            run_index = row["run_index"]
            
            if lord_name not in run_data:
                run_data[lord_name] = {}
            
            run_data[lord_name][run_index] = {
                "input": json.loads(row["input_data"]),
                "output": json.loads(row["output_data"]) if row["output_data"] else None,
                "error": row["error_message"],
                "start_time": row["start_time"],
                "end_time": row["end_time"],
                "duration": row["duration_seconds"],
                "status": row["status"]
            }
        
        return run_data
    
    # ============================================================
    # QUEST SNAPSHOTS (for pause/resume)
    # ============================================================
    
    def save_snapshot(
        self,
        quest_id: str,
        run_data: Dict[str, Dict[int, Dict[str, Any]]],
        execution_stack: List[LordStep],
        reason: str = "checkpoint"
    ) -> int:
        """
        Save quest state snapshot for pause/resume.
        
        Args:
            quest_id: Quest identifier
            run_data: Complete run_data dict
            execution_stack: Current execution stack
            reason: Reason for snapshot ('pause', 'checkpoint', 'error')
            
        Returns:
            snapshot_id: Database ID of snapshot
        """
        now = datetime.now().isoformat()
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO quest_snapshots (
                    quest_id, run_data, execution_stack,
                    snapshot_reason, created_at
                ) VALUES (?, ?, ?, ?, ?)
            """, (
                quest_id,
                json.dumps(run_data),
                json.dumps([self._serialize_lord_step(step) for step in execution_stack]),
                reason,
                now
            ))
            
            snapshot_id = cursor.lastrowid
            conn.commit()
            return snapshot_id
    
    def load_latest_snapshot(self, quest_id: str) -> Optional[Tuple[Dict, List[LordStep]]]:
        """
        Load most recent snapshot for quest.
        
        Args:
            quest_id: Quest identifier
            
        Returns:
            Tuple of (run_data, execution_stack) or None if no snapshot
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT run_data, execution_stack
                FROM quest_snapshots
                WHERE quest_id = ?
                ORDER BY created_at DESC
                LIMIT 1
            """, (quest_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            run_data = json.loads(row["run_data"])
            stack_data = json.loads(row["execution_stack"])
            execution_stack = [self._deserialize_lord_step(step) for step in stack_data]
            
            return (run_data, execution_stack)
    
    # ============================================================
    # QUERY INTERFACE
    # ============================================================
    
    def list_quests(
        self,
        status: Optional[ExecutionStatus] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        List quests with optional filtering.
        
        Args:
            status: Filter by execution status
            limit: Maximum results to return
            offset: Pagination offset
            
        Returns:
            List of quest summaries
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            query = """
                SELECT quest_id, quest_type, status,
                       start_time, end_time, duration_seconds,
                       created_at, updated_at
                FROM quest_executions
            """
            params = []
            
            if status:
                query += " WHERE status = ?"
                params.append(status.value)
            
            query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])
            
            cursor.execute(query, params)
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    "quest_id": row["quest_id"],
                    "quest_type": row["quest_type"],
                    "status": row["status"],
                    "start_time": row["start_time"],
                    "end_time": row["end_time"],
                    "duration_seconds": row["duration_seconds"],
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"]
                })
            
            return results
    
    def get_quest_stats(self) -> Dict[str, Any]:
        """
        Get overall quest execution statistics.
        
        Returns:
            Statistics dictionary with counts and averages
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Overall counts
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_quests,
                    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                    SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed,
                    SUM(CASE WHEN status = 'running' THEN 1 ELSE 0 END) as running,
                    SUM(CASE WHEN status = 'paused' THEN 1 ELSE 0 END) as paused,
                    AVG(duration_seconds) as avg_duration,
                    MAX(duration_seconds) as max_duration,
                    MIN(duration_seconds) as min_duration
                FROM quest_executions
            """)
            
            row = cursor.fetchone()
            
            return {
                "total_quests": row["total_quests"],
                "completed": row["completed"],
                "failed": row["failed"],
                "running": row["running"],
                "paused": row["paused"],
                "avg_duration_seconds": row["avg_duration"],
                "max_duration_seconds": row["max_duration"],
                "min_duration_seconds": row["min_duration"]
            }
    
    def get_lord_stats(self, lord_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get Lord execution statistics.
        
        Args:
            lord_name: Optional filter for specific Lord
            
        Returns:
            List of Lord performance statistics
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            query = """
                SELECT 
                    lord_name,
                    tool_name,
                    COUNT(*) as total_runs,
                    SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as successful,
                    SUM(CASE WHEN status = 'error' THEN 1 ELSE 0 END) as errors,
                    AVG(duration_seconds) as avg_duration,
                    MAX(duration_seconds) as max_duration,
                    MIN(duration_seconds) as min_duration
                FROM lord_runs
            """
            params = []
            
            if lord_name:
                query += " WHERE lord_name = ?"
                params.append(lord_name)
            
            query += " GROUP BY lord_name, tool_name ORDER BY total_runs DESC"
            
            cursor.execute(query, params)
            
            results = []
            for row in cursor.fetchall():
                success_rate = (row["successful"] / row["total_runs"] * 100) if row["total_runs"] > 0 else 0
                
                results.append({
                    "lord_name": row["lord_name"],
                    "tool_name": row["tool_name"],
                    "total_runs": row["total_runs"],
                    "successful": row["successful"],
                    "errors": row["errors"],
                    "success_rate": round(success_rate, 2),
                    "avg_duration_seconds": row["avg_duration"],
                    "max_duration_seconds": row["max_duration"],
                    "min_duration_seconds": row["min_duration"]
                })
            
            return results
    
    # ============================================================
    # SERIALIZATION HELPERS
    # ============================================================
    
    def _serialize_lord_step(self, step: LordStep) -> Dict[str, Any]:
        """Convert LordStep to JSON-serializable dict."""
        return {
            "lord_name": step.lord_name,
            "tool_name": step.tool_name,
            "on_error": step.on_error.value,
            "retry_config": {
                "max_tries": step.retry_config.max_tries,
                "wait_between_tries_ms": step.retry_config.wait_between_tries_ms,
                "exponential_backoff": getattr(step.retry_config, "exponential_backoff", False)
            }
        }
    
    def _deserialize_lord_step(self, data: Dict[str, Any]) -> LordStep:
        """Convert dict to LordStep."""
        from quest_executor import ErrorMode, LordRetryConfig
        
        retry_config = LordRetryConfig(
            max_tries=data["retry_config"]["max_tries"],
            wait_between_tries_ms=data["retry_config"]["wait_between_tries_ms"]
        )
        
        return LordStep(
            lord_name=data["lord_name"],
            tool_name=data["tool_name"],
            on_error=ErrorMode(data["on_error"]),
            retry_config=retry_config
        )


# ============================================================
# CONVENIENCE FUNCTIONS
# ============================================================

def get_repository(db_path: str = "quests.db") -> QuestRepository:
    """
    Get or create quest repository instance.
    
    Args:
        db_path: Path to SQLite database
        
    Returns:
        QuestRepository instance
    """
    return QuestRepository(db_path)
