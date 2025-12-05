"""
Test script for Round Table King Gateway MVP

Tests:
1. Health check endpoints
2. Lord listing
3. Quest routing to Lord Architect
4. Quest routing to Lord Scribe
5. Error handling (unknown quest type, Lord down)
"""

import httpx
import asyncio
import json


async def test_health_checks():
    """Test health check endpoints for all services"""
    print("\n" + "="*70)
    print("TEST 1: Health Checks")
    print("="*70)
    
    services = [
        ("King Gateway", "http://localhost:8000"),
        ("Lord Architect", "http://localhost:8001"),
        ("Lord Scribe", "http://localhost:8002"),
    ]
    
    async with httpx.AsyncClient() as client:
        for name, url in services:
            try:
                response = await client.get(url, timeout=5.0)
                print(f"✓ {name:20} Status: {response.status_code}")
                print(f"  Response: {response.json()}")
            except Exception as e:
                print(f"✗ {name:20} Error: {str(e)}")


async def test_list_lords():
    """Test listing registered Lords"""
    print("\n" + "="*70)
    print("TEST 2: List Registered Lords")
    print("="*70)
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://localhost:8000/lords", timeout=5.0)
            print(f"Status: {response.status_code}")
            print(f"Response:\n{json.dumps(response.json(), indent=2)}")
        except Exception as e:
            print(f"✗ Error: {str(e)}")


async def test_architect_quest():
    """Test routing quest to Lord Architect"""
    print("\n" + "="*70)
    print("TEST 3: Route Quest to Lord Architect (design_system)")
    print("="*70)
    
    quest = {
        "quest_type": "design_system",
        "quest_data": {
            "app_name": "E-Commerce Platform",
            "requirements": [
                "Handle 10k concurrent users",
                "Support multiple payment gateways",
                "Real-time inventory management",
                "Mobile-responsive frontend"
            ],
            "scale": "large"
        }
    }
    
    print(f"Sending quest:\n{json.dumps(quest, indent=2)}")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://localhost:8000/quest",
                json=quest,
                timeout=30.0
            )
            print(f"\nStatus: {response.status_code}")
            result = response.json()
            print(f"Lord: {result.get('lord')}")
            print(f"Status: {result.get('status')}")
            print(f"\nResult (first 500 chars):")
            result_text = str(result.get('result', {}).get('content', [{}])[0].get('text', ''))
            print(result_text[:500] + "..." if len(result_text) > 500 else result_text)
        except Exception as e:
            print(f"✗ Error: {str(e)}")


async def test_scribe_quest():
    """Test routing quest to Lord Scribe"""
    print("\n" + "="*70)
    print("TEST 4: Route Quest to Lord Scribe (write_docs)")
    print("="*70)
    
    quest = {
        "quest_type": "write_docs",
        "quest_data": {
            "topic": "FastAPI Best Practices",
            "format": "markdown",
            "detail_level": "comprehensive"
        }
    }
    
    print(f"Sending quest:\n{json.dumps(quest, indent=2)}")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://localhost:8000/quest",
                json=quest,
                timeout=30.0
            )
            print(f"\nStatus: {response.status_code}")
            result = response.json()
            print(f"Lord: {result.get('lord')}")
            print(f"Status: {result.get('status')}")
            print(f"\nResult (first 500 chars):")
            result_text = str(result.get('result', {}).get('content', [{}])[0].get('text', ''))
            print(result_text[:500] + "..." if len(result_text) > 500 else result_text)
        except Exception as e:
            print(f"✗ Error: {str(e)}")


async def test_explicit_lord_routing():
    """Test explicit Lord targeting"""
    print("\n" + "="*70)
    print("TEST 5: Explicit Lord Routing")
    print("="*70)
    
    quest = {
        "quest_type": "create_summary",
        "quest_data": {
            "content": "This is a long piece of text that needs to be summarized. " * 20,
            "max_length": 100
        },
        "lord_name": "scribe"
    }
    
    print(f"Sending quest with explicit lord_name='scribe'")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://localhost:8000/quest",
                json=quest,
                timeout=30.0
            )
            print(f"\nStatus: {response.status_code}")
            result = response.json()
            print(f"✓ Routed to Lord: {result.get('lord')}")
        except Exception as e:
            print(f"✗ Error: {str(e)}")


async def test_error_handling():
    """Test error handling for unknown quest types"""
    print("\n" + "="*70)
    print("TEST 6: Error Handling (unknown quest type)")
    print("="*70)
    
    quest = {
        "quest_type": "unknown_quest_type",
        "quest_data": {}
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://localhost:8000/quest",
                json=quest,
                timeout=5.0
            )
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
        except httpx.HTTPStatusError as e:
            print(f"✓ Expected error received: HTTP {e.response.status_code}")
            print(f"  Detail: {e.response.json()}")


async def run_all_tests():
    """Run all tests in sequence"""
    print("\n" + "="*70)
    print("ROUND TABLE KING GATEWAY - MVP TEST SUITE")
    print("="*70)
    print("\nMake sure all services are running:")
    print("  Terminal 1: python king_gateway.py")
    print("  Terminal 2: python lord_architect.py")
    print("  Terminal 3: python lord_scribe.py")
    print("\nStarting tests in 3 seconds...")
    await asyncio.sleep(3)
    
    await test_health_checks()
    await test_list_lords()
    await test_architect_quest()
    await test_scribe_quest()
    await test_explicit_lord_routing()
    await test_error_handling()
    
    print("\n" + "="*70)
    print("TEST SUITE COMPLETE")
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(run_all_tests())
