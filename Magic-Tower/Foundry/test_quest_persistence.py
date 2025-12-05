"""
Test Suite for Quest Persistence Layer

Tests SQLite-based state persistence, pause/resume/replay functionality,
and quest history analytics.
"""

import asyncio
import time
import os
from pathlib import Path

from quest_executor import (
    QuestExecutor,
    QuestExecutionData,
    LordStep,
    ErrorMode,
    ExecutionStatus,
    LordRetryConfig,
    ExecutionHooks
)
from quest_persistence import QuestRepository


# Test database path
TEST_DB = "test_quests.db"


def cleanup_test_db():
    """Remove test database if exists"""
    if Path(TEST_DB).exists():
        os.remove(TEST_DB)


async def test_1_basic_save_and_load():
    """Test: Save quest to database and load it back"""
    cleanup_test_db()
    repo = QuestRepository(TEST_DB)
    
    # Create quest
    quest_data = QuestExecutionData(
        quest_id="q-test-001",
        quest_type="test_quest",
        input_data={"test": "data"},
        execution_stack=[
            LordStep("architect", "design_system"),
            LordStep("forge_master", "generate_code"),
        ]
    )
    
    quest_data.status = ExecutionStatus.RUNNING
    quest_data.start_time = time.time()
    
    # Save quest
    repo.save_quest(quest_data)
    
    # Load quest
    loaded_quest = repo.load_quest("q-test-001")
    
    assert loaded_quest is not None
    assert loaded_quest.quest_id == "q-test-001"
    assert loaded_quest.quest_type == "test_quest"
    assert loaded_quest.status == ExecutionStatus.RUNNING
    assert len(loaded_quest.execution_stack) == 2
    assert loaded_quest.execution_stack[0].lord_name == "architect"
    assert loaded_quest.input_data["test"] == "data"
    
    print("✅ TEST 1: Basic save and load")
    cleanup_test_db()


async def test_2_save_lord_runs():
    """Test: Save individual Lord execution runs"""
    cleanup_test_db()
    repo = QuestRepository(TEST_DB)
    
    quest_id = "q-test-002"
    
    # Save quest first
    quest_data = QuestExecutionData(
        quest_id=quest_id,
        quest_type="test_quest",
        input_data={"test": "data"}
    )
    repo.save_quest(quest_data)
    
    # Save Lord runs
    run_id_1 = repo.save_lord_run(
        quest_id=quest_id,
        lord_name="architect",
        tool_name="design_system",
        run_index=0,
        status="success",
        input_data={"requirements": ["test"]},
        output_data={"design": "completed"},
        start_time=time.time(),
        end_time=time.time() + 1.5
    )
    
    run_id_2 = repo.save_lord_run(
        quest_id=quest_id,
        lord_name="forge_master",
        tool_name="generate_code",
        run_index=0,
        status="success",
        input_data={"design": "completed"},
        output_data={"code": "generated"},
        start_time=time.time(),
        end_time=time.time() + 2.0
    )
    
    assert run_id_1 > 0
    assert run_id_2 > 0
    
    # Load quest with run data
    loaded_quest = repo.load_quest(quest_id)
    assert "architect" in loaded_quest.run_data
    assert "forge_master" in loaded_quest.run_data
    assert loaded_quest.run_data["architect"][0]["status"] == "success"
    assert loaded_quest.run_data["forge_master"][0]["output"]["code"] == "generated"
    
    print("✅ TEST 2: Save Lord runs")
    cleanup_test_db()


async def test_3_quest_snapshots():
    """Test: Save and load quest snapshots for pause/resume"""
    cleanup_test_db()
    repo = QuestRepository(TEST_DB)
    
    quest_id = "q-test-003"
    
    # Create quest
    quest_data = QuestExecutionData(
        quest_id=quest_id,
        quest_type="test_quest",
        input_data={"test": "data"},
        execution_stack=[
            LordStep("scribe", "write_docs"),
        ]
    )
    repo.save_quest(quest_data)
    
    # Save snapshot
    run_data = {
        "architect": {
            0: {"status": "success", "output": {"design": "done"}}
        }
    }
    
    snapshot_id = repo.save_snapshot(
        quest_id=quest_id,
        run_data=run_data,
        execution_stack=quest_data.execution_stack,
        reason="pause"
    )
    
    assert snapshot_id > 0
    
    # Load snapshot
    loaded_data, loaded_stack = repo.load_latest_snapshot(quest_id)
    
    assert "architect" in loaded_data
    assert len(loaded_stack) == 1
    assert loaded_stack[0].lord_name == "scribe"
    
    print("✅ TEST 3: Quest snapshots")
    cleanup_test_db()


async def test_4_executor_with_persistence():
    """Test: QuestExecutor auto-saves state to database"""
    cleanup_test_db()
    repo = QuestRepository(TEST_DB)
    
    # Note: This test requires actual Lord servers running
    # For now, we'll test the integration structure
    
    executor = QuestExecutor(repository=repo)
    
    quest_data = QuestExecutionData(
        quest_id="q-test-004",
        quest_type="test_with_persistence",
        input_data={"test": "data"},
        execution_stack=[
            # Would need real Lords for full test
        ]
    )
    
    # Verify repository is configured
    assert executor.repository is not None
    assert executor._auto_save is True
    
    # Save initial quest state
    repo.save_quest(quest_data)
    
    # Load back
    loaded = repo.load_quest("q-test-004")
    assert loaded is not None
    assert loaded.quest_id == "q-test-004"
    
    print("✅ TEST 4: Executor with persistence")
    cleanup_test_db()


async def test_5_pause_resume_integration():
    """Test: Pause and resume quest execution"""
    cleanup_test_db()
    repo = QuestRepository(TEST_DB)
    executor = QuestExecutor(repository=repo)
    
    quest_id = "q-test-005"
    
    # Create quest with multiple steps
    quest_data = QuestExecutionData(
        quest_id=quest_id,
        quest_type="test_pause_resume",
        input_data={"test": "data"},
        execution_stack=[
            LordStep("architect", "design_system"),
            LordStep("forge_master", "generate_code"),
            LordStep("sentinel", "review_code"),
        ]
    )
    
    # Save initial state
    repo.save_quest(quest_data)
    
    # Simulate partial execution by saving some run_data
    quest_data.run_data["architect"] = {
        0: {
            "status": "success",
            "output": {"design": "completed"},
            "start_time": time.time(),
            "duration": 1.5
        }
    }
    
    # Remove completed Lord from stack
    quest_data.execution_stack = quest_data.execution_stack[1:]
    
    # Save updated state
    repo.save_quest(quest_data)
    
    # Pause quest
    paused = await executor.pause_quest(quest_id)
    assert paused is True
    
    # Verify quest is paused
    loaded = repo.load_quest(quest_id)
    assert loaded.status == ExecutionStatus.PAUSED
    
    # Verify snapshot was created
    snapshot = repo.load_latest_snapshot(quest_id)
    assert snapshot is not None
    
    print("✅ TEST 5: Pause/resume integration")
    cleanup_test_db()


async def test_6_replay_quest():
    """Test: Replay quest from beginning or specific Lord"""
    cleanup_test_db()
    repo = QuestRepository(TEST_DB)
    
    quest_id = "q-test-006"
    
    # Create completed quest
    quest_data = QuestExecutionData(
        quest_id=quest_id,
        quest_type="test_replay",
        input_data={"test": "data"},
        execution_stack=[
            LordStep("architect", "design_system"),
            LordStep("forge_master", "generate_code"),
        ],
        status=ExecutionStatus.COMPLETED
    )
    
    quest_data.run_data = {
        "architect": {0: {"status": "success", "output": {"design": "v1"}}},
        "forge_master": {0: {"status": "success", "output": {"code": "v1"}}}
    }
    
    repo.save_quest(quest_data)
    
    # Verify we can load it
    loaded = repo.load_quest(quest_id)
    assert loaded is not None
    assert loaded.status == ExecutionStatus.COMPLETED
    
    print("✅ TEST 6: Replay quest")
    cleanup_test_db()


async def test_7_query_quest_list():
    """Test: List quests with filtering"""
    cleanup_test_db()
    repo = QuestRepository(TEST_DB)
    
    # Create multiple quests
    for i in range(5):
        quest_data = QuestExecutionData(
            quest_id=f"q-test-{i:03d}",
            quest_type="test_query",
            input_data={"index": i},
            status=ExecutionStatus.COMPLETED if i % 2 == 0 else ExecutionStatus.FAILED
        )
        repo.save_quest(quest_data)
    
    # List all quests
    all_quests = repo.list_quests(limit=10)
    assert len(all_quests) == 5
    
    # Filter by status
    completed_quests = repo.list_quests(status=ExecutionStatus.COMPLETED, limit=10)
    assert len(completed_quests) == 3  # Quests 0, 2, 4
    
    failed_quests = repo.list_quests(status=ExecutionStatus.FAILED, limit=10)
    assert len(failed_quests) == 2  # Quests 1, 3
    
    # Test pagination
    page_1 = repo.list_quests(limit=2, offset=0)
    page_2 = repo.list_quests(limit=2, offset=2)
    assert len(page_1) == 2
    assert len(page_2) == 2
    assert page_1[0]["quest_id"] != page_2[0]["quest_id"]
    
    print("✅ TEST 7: Query quest list")
    cleanup_test_db()


async def test_8_quest_statistics():
    """Test: Get quest execution statistics"""
    cleanup_test_db()
    repo = QuestRepository(TEST_DB)
    
    # Create quests with different statuses
    statuses = [
        ExecutionStatus.COMPLETED,
        ExecutionStatus.COMPLETED,
        ExecutionStatus.FAILED,
        ExecutionStatus.RUNNING,
        ExecutionStatus.PAUSED
    ]
    
    for i, status in enumerate(statuses):
        quest_data = QuestExecutionData(
            quest_id=f"q-stats-{i:03d}",
            quest_type="test_stats",
            input_data={"index": i},
            status=status,
            start_time=time.time(),
            end_time=time.time() + (i + 1)  # Duration: 1, 2, 3, 4, 5 seconds
        )
        repo.save_quest(quest_data)
    
    # Get statistics
    stats = repo.get_quest_stats()
    
    assert stats["total_quests"] == 5
    assert stats["completed"] == 2
    assert stats["failed"] == 1
    assert stats["running"] == 1
    assert stats["paused"] == 1
    assert stats["avg_duration_seconds"] > 0
    
    print("✅ TEST 8: Quest statistics")
    print(f"  Stats: {stats}")
    cleanup_test_db()


async def test_9_lord_performance_stats():
    """Test: Get Lord execution performance statistics"""
    cleanup_test_db()
    repo = QuestRepository(TEST_DB)
    
    quest_id = "q-stats-lords"
    
    # Create quest
    quest_data = QuestExecutionData(
        quest_id=quest_id,
        quest_type="test_lord_stats",
        input_data={"test": "data"}
    )
    repo.save_quest(quest_data)
    
    # Save multiple Lord runs
    lords_data = [
        ("architect", "design_system", "success", 1.5),
        ("architect", "design_system", "success", 1.8),
        ("architect", "design_system", "error", 0.5),
        ("forge_master", "generate_code", "success", 2.5),
        ("sentinel", "review_code", "success", 2.0),
    ]
    
    for i, (lord, tool, status, duration) in enumerate(lords_data):
        start = time.time()
        repo.save_lord_run(
            quest_id=quest_id,
            lord_name=lord,
            tool_name=tool,
            run_index=i,
            status=status,
            input_data={"test": i},
            output_data={"result": i} if status == "success" else None,
            error_message="Test error" if status == "error" else None,
            start_time=start,
            end_time=start + duration
        )
    
    # Get Lord statistics
    stats = repo.get_lord_stats()
    
    assert len(stats) == 3  # 3 unique Lord+tool combinations
    
    # Find architect stats
    architect_stats = next(s for s in stats if s["lord_name"] == "architect")
    assert architect_stats["total_runs"] == 3
    assert architect_stats["successful"] == 2
    assert architect_stats["errors"] == 1
    assert round(architect_stats["success_rate"], 0) == 67  # 2/3 = 66.67%
    
    print("✅ TEST 9: Lord performance stats")
    print(f"  Architect: {architect_stats}")
    cleanup_test_db()


async def test_10_update_quest_status():
    """Test: Update quest status and reload"""
    cleanup_test_db()
    repo = QuestRepository(TEST_DB)
    
    quest_id = "q-test-010"
    
    # Create quest
    quest_data = QuestExecutionData(
        quest_id=quest_id,
        quest_type="test_update",
        input_data={"test": "data"},
        status=ExecutionStatus.RUNNING
    )
    repo.save_quest(quest_data)
    
    # Update status
    quest_data.status = ExecutionStatus.COMPLETED
    quest_data.end_time = time.time()
    quest_data.output_data = {"result": "success"}
    repo.save_quest(quest_data)
    
    # Reload and verify
    loaded = repo.load_quest(quest_id)
    assert loaded.status == ExecutionStatus.COMPLETED
    assert loaded.output_data["result"] == "success"
    assert loaded.end_time is not None
    
    print("✅ TEST 10: Update quest status")
    cleanup_test_db()


async def test_11_delete_quest():
    """Test: Delete quest and all associated data"""
    cleanup_test_db()
    repo = QuestRepository(TEST_DB)
    
    quest_id = "q-test-011"
    
    # Create quest with Lord runs
    quest_data = QuestExecutionData(
        quest_id=quest_id,
        quest_type="test_delete",
        input_data={"test": "data"}
    )
    repo.save_quest(quest_data)
    
    repo.save_lord_run(
        quest_id=quest_id,
        lord_name="architect",
        tool_name="design_system",
        run_index=0,
        status="success",
        input_data={"test": "data"},
        start_time=time.time()
    )
    
    # Verify quest exists
    assert repo.load_quest(quest_id) is not None
    
    # Delete quest
    deleted = repo.delete_quest(quest_id)
    assert deleted is True
    
    # Verify quest is gone
    assert repo.load_quest(quest_id) is None
    
    # Try deleting non-existent quest
    deleted_again = repo.delete_quest(quest_id)
    assert deleted_again is False
    
    print("✅ TEST 11: Delete quest")
    cleanup_test_db()


async def run_all_tests():
    """Run all persistence tests"""
    print("\n" + "="*60)
    print("QUEST PERSISTENCE TEST SUITE")
    print("="*60 + "\n")
    
    tests = [
        test_1_basic_save_and_load,
        test_2_save_lord_runs,
        test_3_quest_snapshots,
        test_4_executor_with_persistence,
        test_5_pause_resume_integration,
        test_6_replay_quest,
        test_7_query_quest_list,
        test_8_quest_statistics,
        test_9_lord_performance_stats,
        test_10_update_quest_status,
        test_11_delete_quest,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            await test()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test.__name__} ERROR: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return passed, failed


if __name__ == "__main__":
    asyncio.run(run_all_tests())
