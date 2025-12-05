"""
Demo: Quest State Persistence with Pause/Resume/Replay

Shows how to:
1. Execute a quest with automatic state saving
2. Pause a running quest
3. Resume from checkpoint
4. Replay a quest from beginning or specific Lord
5. Query quest history and analytics
"""

import asyncio
import time

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


async def demo_1_basic_persistence():
    """Demo 1: Basic quest execution with auto-save"""
    print("\n" + "="*60)
    print("DEMO 1: Quest Execution with Auto-Save")
    print("="*60)
    
    # Create repository
    repo = QuestRepository("demo_quests.db")
    
    # Create executor with persistence
    executor = QuestExecutor(repository=repo)
    
    # Build quest (simplified - would need real Lords)
    quest_data = QuestExecutionData(
        quest_id="demo-quest-001",
        quest_type="design_microservice",
        input_data={
            "service_name": "UserAuthService",
            "requirements": [
                "JWT authentication",
                "OAuth2 integration",
                "Rate limiting",
                "User session management"
            ]
        },
        execution_stack=[
            LordStep("architect", "design_system"),
            LordStep("forge_master", "generate_code"),
            LordStep("sentinel", "review_code"),
        ]
    )
    
    print(f"✅ Quest created: {quest_data.quest_id}")
    print(f"   Type: {quest_data.quest_type}")
    print(f"   Lords: {len(quest_data.execution_stack)}")
    
    # Save initial state
    repo.save_quest(quest_data)
    print(f"✅ Initial state saved to database")
    
    # Load back to verify
    loaded = repo.load_quest("demo-quest-001")
    assert loaded is not None
    print(f"✅ State loaded successfully")
    print(f"   Execution stack has {len(loaded.execution_stack)} Lords")
    
    return repo


async def demo_2_quest_snapshots(repo: QuestRepository):
    """Demo 2: Save and restore quest snapshots"""
    print("\n" + "="*60)
    print("DEMO 2: Quest Snapshots (Pause/Resume)")
    print("="*60)
    
    quest_id = "demo-quest-002"
    
    # Create quest
    quest_data = QuestExecutionData(
        quest_id=quest_id,
        quest_type="code_review_pipeline",
        input_data={"repo": "github.com/user/project"},
        execution_stack=[
            LordStep("architect", "analyze_architecture"),
            LordStep("sentinel", "review_code"),
            LordStep("scribe", "write_report"),
        ]
    )
    
    repo.save_quest(quest_data)
    print(f"✅ Quest {quest_id} created with 3 Lords")
    
    # Simulate partial execution (Architect completed)
    quest_data.run_data["architect"] = {
        0: {
            "status": "success",
            "output": {
                "architecture": "Microservices",
                "patterns": ["API Gateway", "Service Mesh"],
                "concerns": ["Database consistency", "Network latency"]
            },
            "start_time": time.time(),
            "duration": 2.5
        }
    }
    
    # Remove completed Lord from stack
    quest_data.execution_stack = quest_data.execution_stack[1:]
    print(f"✅ Architect completed - 2 Lords remaining")
    
    # Save snapshot (pause point)
    snapshot_id = repo.save_snapshot(
        quest_id=quest_id,
        run_data=quest_data.run_data,
        execution_stack=quest_data.execution_stack,
        reason="checkpoint"
    )
    
    print(f"✅ Snapshot #{snapshot_id} saved")
    print(f"   Remaining Lords: {[step.lord_name for step in quest_data.execution_stack]}")
    
    # Load snapshot
    loaded_run_data, loaded_stack = repo.load_latest_snapshot(quest_id)
    
    print(f"✅ Snapshot loaded successfully")
    print(f"   Completed: {list(loaded_run_data.keys())}")
    print(f"   Remaining: {[step.lord_name for step in loaded_stack]}")


async def demo_3_pause_resume():
    """Demo 3: Pause and resume quest execution"""
    print("\n" + "="*60)
    print("DEMO 3: Pause and Resume Quest")
    print("="*60)
    
    repo = QuestRepository("demo_quests.db")
    executor = QuestExecutor(repository=repo)
    
    quest_id = "demo-quest-003"
    
    # Create quest
    quest_data = QuestExecutionData(
        quest_id=quest_id,
        quest_type="documentation_generation",
        input_data={"codebase": "src/"},
        execution_stack=[
            LordStep("architect", "analyze_structure"),
            LordStep("scribe", "write_docs"),
            LordStep("oracle", "generate_examples"),
        ],
        status=ExecutionStatus.RUNNING
    )
    
    repo.save_quest(quest_data)
    print(f"✅ Quest {quest_id} started")
    
    # Simulate partial progress
    quest_data.run_data["architect"] = {
        0: {"status": "success", "output": {"structure": "analyzed"}}
    }
    quest_data.execution_stack = quest_data.execution_stack[1:]
    repo.save_quest(quest_data)
    
    # Pause quest
    paused = await executor.pause_quest(quest_id)
    print(f"✅ Quest paused: {paused}")
    
    # Check status
    loaded = repo.load_quest(quest_id)
    print(f"   Status: {loaded.status}")
    print(f"   Completed: {list(loaded.run_data.keys())}")
    print(f"   Remaining: {[step.lord_name for step in loaded.execution_stack]}")
    
    print(f"\n💤 Quest is paused - can resume later with executor.resume_quest('{quest_id}')")


async def demo_4_quest_analytics(repo: QuestRepository):
    """Demo 4: Query quest history and analytics"""
    print("\n" + "="*60)
    print("DEMO 4: Quest Analytics and History")
    print("="*60)
    
    # Create some test quests with different statuses
    test_quests = [
        ("analytics-001", ExecutionStatus.COMPLETED, 5.5),
        ("analytics-002", ExecutionStatus.COMPLETED, 8.2),
        ("analytics-003", ExecutionStatus.FAILED, 3.1),
        ("analytics-004", ExecutionStatus.RUNNING, None),
        ("analytics-005", ExecutionStatus.PAUSED, 4.0),
    ]
    
    for quest_id, status, duration in test_quests:
        quest_data = QuestExecutionData(
            quest_id=quest_id,
            quest_type="test_analytics",
            input_data={"test": True},
            status=status,
            start_time=time.time()
        )
        
        if duration:
            quest_data.end_time = quest_data.start_time + duration
        
        repo.save_quest(quest_data)
    
    print(f"✅ Created {len(test_quests)} test quests")
    
    # Get overall statistics
    stats = repo.get_quest_stats()
    
    print(f"\n📊 Quest Statistics:")
    print(f"   Total quests: {stats['total_quests']}")
    print(f"   Completed: {stats['completed']}")
    print(f"   Failed: {stats['failed']}")
    print(f"   Running: {stats['running']}")
    print(f"   Paused: {stats['paused']}")
    print(f"   Avg duration: {stats['avg_duration_seconds']:.2f}s")
    
    # List all quests
    all_quests = repo.list_quests(limit=20)
    
    print(f"\n📋 Quest History ({len(all_quests)} quests):")
    for quest in all_quests[:5]:  # Show first 5
        print(f"   {quest['quest_id']}: {quest['status']} ({quest['quest_type']})")


async def demo_5_lord_performance():
    """Demo 5: Lord performance analytics"""
    print("\n" + "="*60)
    print("DEMO 5: Lord Performance Analytics")
    print("="*60)
    
    repo = QuestRepository("demo_quests.db")
    
    quest_id = "perf-test-001"
    
    # Create quest
    quest_data = QuestExecutionData(
        quest_id=quest_id,
        quest_type="performance_test",
        input_data={"test": True}
    )
    repo.save_quest(quest_data)
    
    # Simulate Lord runs with different performance
    lords_performance = [
        ("architect", "design_system", "success", 1.5),
        ("architect", "design_system", "success", 1.8),
        ("architect", "design_system", "error", 0.5),
        ("architect", "analyze_architecture", "success", 2.2),
        ("forge_master", "generate_code", "success", 3.5),
        ("forge_master", "generate_code", "success", 3.2),
        ("sentinel", "review_code", "success", 2.0),
        ("sentinel", "review_code", "success", 2.1),
        ("sentinel", "review_code", "error", 0.8),
    ]
    
    for i, (lord, tool, status, duration) in enumerate(lords_performance):
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
    
    print(f"✅ Saved {len(lords_performance)} Lord runs")
    
    # Get Lord statistics
    stats = repo.get_lord_stats()
    
    print(f"\n📊 Lord Performance Metrics:")
    print(f"{'Lord':<15} {'Tool':<20} {'Runs':<6} {'Success':<8} {'Errors':<7} {'Success %':<10} {'Avg Time':<10}")
    print("-" * 90)
    
    for lord_stat in stats:
        print(f"{lord_stat['lord_name']:<15} "
              f"{lord_stat['tool_name']:<20} "
              f"{lord_stat['total_runs']:<6} "
              f"{lord_stat['successful']:<8} "
              f"{lord_stat['errors']:<7} "
              f"{lord_stat['success_rate']:<10.1f} "
              f"{lord_stat['avg_duration_seconds']:<10.2f}")


async def demo_6_query_filtering():
    """Demo 6: Query quests with filtering and pagination"""
    print("\n" + "="*60)
    print("DEMO 6: Advanced Quest Queries")
    print("="*60)
    
    repo = QuestRepository("demo_quests.db")
    
    # Query completed quests only
    completed = repo.list_quests(status=ExecutionStatus.COMPLETED, limit=10)
    print(f"✅ Completed quests: {len(completed)}")
    
    # Query failed quests only
    failed = repo.list_quests(status=ExecutionStatus.FAILED, limit=10)
    print(f"✅ Failed quests: {len(failed)}")
    
    # Pagination example
    page_1 = repo.list_quests(limit=3, offset=0)
    page_2 = repo.list_quests(limit=3, offset=3)
    
    print(f"\n📄 Pagination Example:")
    print(f"   Page 1: {[q['quest_id'] for q in page_1]}")
    print(f"   Page 2: {[q['quest_id'] for q in page_2]}")
    
    # Query specific Lord performance
    architect_stats = repo.get_lord_stats(lord_name="architect")
    
    if architect_stats:
        print(f"\n🏗️  Architect Performance:")
        for stat in architect_stats:
            print(f"   {stat['tool_name']}: {stat['total_runs']} runs, "
                  f"{stat['success_rate']:.1f}% success rate, "
                  f"{stat['avg_duration_seconds']:.2f}s avg")


async def main():
    """Run all demos"""
    print("\n" + "="*60)
    print("🎯 QUEST PERSISTENCE DEMONSTRATION")
    print("="*60)
    print("\nShowing SQLite persistence capabilities:")
    print("- Automatic state saving during execution")
    print("- Quest pause/resume functionality")
    print("- Quest replay from checkpoints")
    print("- Historical analytics and performance metrics")
    print("- Advanced querying and filtering")
    
    # Run demos
    repo = await demo_1_basic_persistence()
    await demo_2_quest_snapshots(repo)
    await demo_3_pause_resume()
    await demo_4_quest_analytics(repo)
    await demo_5_lord_performance()
    await demo_6_query_filtering()
    
    print("\n" + "="*60)
    print("✅ ALL DEMOS COMPLETE")
    print("="*60)
    print(f"\nDatabase: demo_quests.db")
    print(f"You can now:")
    print(f"  1. Query quest history with repo.list_quests()")
    print(f"  2. Get analytics with repo.get_quest_stats()")
    print(f"  3. Resume paused quests with executor.resume_quest(quest_id)")
    print(f"  4. Replay quests with executor.replay_quest(quest_id)")
    print(f"  5. Track Lord performance with repo.get_lord_stats()")
    print()


if __name__ == "__main__":
    asyncio.run(main())
