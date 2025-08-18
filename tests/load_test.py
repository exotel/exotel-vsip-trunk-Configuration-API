#!/usr/bin/env python3

"""
Load Testing Script for Exotel vSIP APIs
Tests API performance, rate limiting, and concurrent request handling
"""

import asyncio
import aiohttp
import time
import json
import statistics
import logging
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
import datetime
import os

@dataclass
class LoadTestResult:
    """Data class for load test results"""
    endpoint: str
    method: str
    status_code: int
    response_time: float
    success: bool
    error_message: str = ""
    timestamp: str = ""

class LoadTester:
    def __init__(self, base_url: str, auth: tuple, max_concurrent: int = 10):
        self.base_url = base_url
        self.auth = auth
        self.max_concurrent = max_concurrent
        self.results: List[LoadTestResult] = []
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    async def make_request(self, session: aiohttp.ClientSession, endpoint: str, 
                          method: str, payload: Dict[str, Any] = None) -> LoadTestResult:
        """Make a single async HTTP request"""
        
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        try:
            if method.upper() == 'POST':
                async with session.post(url, json=payload) as response:
                    response_text = await response.text()
                    response_time = time.time() - start_time
                    
                    return LoadTestResult(
                        endpoint=endpoint,
                        method=method,
                        status_code=response.status,
                        response_time=response_time,
                        success=200 <= response.status < 300,
                        error_message=response_text if response.status >= 400 else "",
                        timestamp=datetime.datetime.utcnow().isoformat()
                    )
            else:
                async with session.get(url) as response:
                    response_text = await response.text()
                    response_time = time.time() - start_time
                    
                    return LoadTestResult(
                        endpoint=endpoint,
                        method=method,
                        status_code=response.status,
                        response_time=response_time,
                        success=200 <= response.status < 300,
                        error_message=response_text if response.status >= 400 else "",
                        timestamp=datetime.datetime.utcnow().isoformat()
                    )
                    
        except Exception as e:
            response_time = time.time() - start_time
            return LoadTestResult(
                endpoint=endpoint,
                method=method,
                status_code=0,
                response_time=response_time,
                success=False,
                error_message=str(e),
                timestamp=datetime.datetime.utcnow().isoformat()
            )
    
    async def test_trunk_creation_load(self, num_requests: int = 50) -> List[LoadTestResult]:
        """Load test trunk creation endpoint"""
        
        self.logger.info(f"🚀 Starting trunk creation load test with {num_requests} requests")
        
        # Create session with authentication
        auth = aiohttp.BasicAuth(self.auth[0], self.auth[1])
        timeout = aiohttp.ClientTimeout(total=30)
        
        async with aiohttp.ClientSession(auth=auth, timeout=timeout) as session:
            tasks = []
            
            for i in range(num_requests):
                payload = {
                    "trunk_name": f"load_test_trunk_{i}_{int(time.time())}",
                    "nso_code": "ANY-ANY",
                    "domain_name": f"{os.getenv('EXO_ACCOUNT_SID', 'test')}.pstn.exotel.com"
                }
                
                task = self.make_request(session, "/trunks", "POST", payload)
                tasks.append(task)
            
            # Execute requests with concurrency limit
            semaphore = asyncio.Semaphore(self.max_concurrent)
            
            async def limited_request(task):
                async with semaphore:
                    return await task
            
            results = await asyncio.gather(*[limited_request(task) for task in tasks])
            
        self.results.extend(results)
        return results
    
    async def test_rate_limiting(self, requests_per_second: int = 20, duration: int = 60) -> List[LoadTestResult]:
        """Test API rate limiting"""
        
        self.logger.info(f"⏱️ Testing rate limiting: {requests_per_second} req/sec for {duration} seconds")
        
        auth = aiohttp.BasicAuth(self.auth[0], self.auth[1])
        timeout = aiohttp.ClientTimeout(total=30)
        
        results = []
        start_time = time.time()
        request_count = 0
        
        async with aiohttp.ClientSession(auth=auth, timeout=timeout) as session:
            while time.time() - start_time < duration:
                batch_start = time.time()
                
                # Create batch of requests for this second
                tasks = []
                for _ in range(requests_per_second):
                    payload = {
                        "trunk_name": f"rate_test_{request_count}_{int(time.time())}",
                        "nso_code": "ANY-ANY",
                        "domain_name": f"{os.getenv('EXO_ACCOUNT_SID', 'test')}.pstn.exotel.com"
                    }
                    
                    task = self.make_request(session, "/trunks", "POST", payload)
                    tasks.append(task)
                    request_count += 1
                
                # Execute batch
                batch_results = await asyncio.gather(*tasks)
                results.extend(batch_results)
                
                # Wait for remainder of second
                elapsed = time.time() - batch_start
                if elapsed < 1.0:
                    await asyncio.sleep(1.0 - elapsed)
        
        self.results.extend(results)
        return results
    
    async def test_concurrent_endpoints(self, concurrent_requests: int = 25) -> List[LoadTestResult]:
        """Test multiple endpoints concurrently"""
        
        self.logger.info(f"🔀 Testing concurrent access to multiple endpoints: {concurrent_requests} requests")
        
        auth = aiohttp.BasicAuth(self.auth[0], self.auth[1])
        timeout = aiohttp.ClientTimeout(total=30)
        
        # Define test scenarios for different endpoints
        test_scenarios = [
            {
                "endpoint": "/trunks",
                "method": "POST",
                "payload": {
                    "trunk_name": f"concurrent_test_{int(time.time())}",
                    "nso_code": "ANY-ANY",
                    "domain_name": f"{os.getenv('EXO_ACCOUNT_SID', 'test')}.pstn.exotel.com"
                }
            }
            # Add more endpoints when trunk_sid is available
        ]
        
        async with aiohttp.ClientSession(auth=auth, timeout=timeout) as session:
            tasks = []
            
            for i in range(concurrent_requests):
                scenario = test_scenarios[i % len(test_scenarios)]
                
                # Modify payload to ensure uniqueness
                if "payload" in scenario and scenario["payload"]:
                    payload = scenario["payload"].copy()
                    if "trunk_name" in payload:
                        payload["trunk_name"] = f"{payload['trunk_name']}_{i}"
                else:
                    payload = None
                
                task = self.make_request(
                    session, 
                    scenario["endpoint"], 
                    scenario["method"], 
                    payload
                )
                tasks.append(task)
            
            results = await asyncio.gather(*tasks)
        
        self.results.extend(results)
        return results
    
    def analyze_results(self, results: List[LoadTestResult]) -> Dict[str, Any]:
        """Analyze load test results"""
        
        if not results:
            return {"error": "No results to analyze"}
        
        # Basic statistics
        response_times = [r.response_time for r in results]
        success_count = sum(1 for r in results if r.success)
        total_count = len(results)
        
        # Group by status code
        status_codes = {}
        for result in results:
            code = result.status_code
            if code not in status_codes:
                status_codes[code] = 0
            status_codes[code] += 1
        
        # Group by endpoint
        endpoint_stats = {}
        for result in results:
            endpoint = result.endpoint
            if endpoint not in endpoint_stats:
                endpoint_stats[endpoint] = {
                    "total": 0,
                    "success": 0,
                    "response_times": []
                }
            
            endpoint_stats[endpoint]["total"] += 1
            if result.success:
                endpoint_stats[endpoint]["success"] += 1
            endpoint_stats[endpoint]["response_times"].append(result.response_time)
        
        # Calculate endpoint statistics
        for endpoint in endpoint_stats:
            times = endpoint_stats[endpoint]["response_times"]
            if times:
                endpoint_stats[endpoint]["avg_response_time"] = statistics.mean(times)
                endpoint_stats[endpoint]["min_response_time"] = min(times)
                endpoint_stats[endpoint]["max_response_time"] = max(times)
                endpoint_stats[endpoint]["p95_response_time"] = statistics.quantiles(times, n=20)[18]  # 95th percentile
        
        analysis = {
            "summary": {
                "total_requests": total_count,
                "successful_requests": success_count,
                "failed_requests": total_count - success_count,
                "success_rate": (success_count / total_count * 100) if total_count > 0 else 0,
                "avg_response_time": statistics.mean(response_times) if response_times else 0,
                "min_response_time": min(response_times) if response_times else 0,
                "max_response_time": max(response_times) if response_times else 0,
                "p95_response_time": statistics.quantiles(response_times, n=20)[18] if len(response_times) >= 20 else 0
            },
            "status_codes": status_codes,
            "endpoint_stats": endpoint_stats,
            "errors": [
                {
                    "endpoint": r.endpoint,
                    "status_code": r.status_code,
                    "error_message": r.error_message,
                    "timestamp": r.timestamp
                }
                for r in results if not r.success
            ][:10]  # Limit to first 10 errors
        }
        
        return analysis
    
    def save_results(self, filename: str = None):
        """Save results to JSON file"""
        
        if not filename:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"logs/load_test_results_{timestamp}.json"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        data = {
            "test_config": {
                "base_url": self.base_url,
                "max_concurrent": self.max_concurrent,
                "timestamp": datetime.datetime.utcnow().isoformat()
            },
            "results": [asdict(result) for result in self.results],
            "analysis": self.analyze_results(self.results)
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        self.logger.info(f"📁 Results saved to {filename}")
        return filename

async def main():
    """Main load test execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Load test Exotel vSIP APIs")
    parser.add_argument("--concurrent", "-c", type=int, default=10, help="Max concurrent requests")
    parser.add_argument("--requests", "-r", type=int, default=50, help="Total requests for load test")
    parser.add_argument("--rate-limit", "-rl", type=int, default=0, help="Test rate limiting (req/sec)")
    parser.add_argument("--duration", "-d", type=int, default=60, help="Rate limit test duration (seconds)")
    parser.add_argument("--mock", "-m", action="store_true", help="Use mock server")
    
    args = parser.parse_args()
    
    # Configure base URL
    if args.mock:
        base_url = "http://localhost:8080/v2/accounts/test_account"
        auth = ("test_key", "test_token")
    else:
        auth_key = os.getenv('EXO_AUTH_KEY')
        auth_token = os.getenv('EXO_AUTH_TOKEN')
        domain = os.getenv('EXO_SUBSCRIBIX_DOMAIN')
        account_sid = os.getenv('EXO_ACCOUNT_SID')
        
        if not all([auth_key, auth_token, domain, account_sid]):
            print("❌ Missing required environment variables")
            return
        
        base_url = f"https://{domain}/v2/accounts/{account_sid}"
        auth = (auth_key, auth_token)
    
    # Initialize load tester
    tester = LoadTester(base_url, auth, args.concurrent)
    
    print(f"🚀 Starting load tests against {base_url}")
    print(f"📊 Configuration: {args.concurrent} concurrent, {args.requests} total requests")
    
    try:
        # Run load test
        await tester.test_trunk_creation_load(args.requests)
        
        # Run rate limiting test if specified
        if args.rate_limit > 0:
            await tester.test_rate_limiting(args.rate_limit, args.duration)
        
        # Run concurrent endpoint test
        await tester.test_concurrent_endpoints(args.concurrent)
        
        # Analyze and save results
        analysis = tester.analyze_results(tester.results)
        results_file = tester.save_results()
        
        # Print summary
        summary = analysis["summary"]
        print(f"\n📊 Load Test Results:")
        print(f"   Total Requests: {summary['total_requests']}")
        print(f"   Success Rate: {summary['success_rate']:.1f}%")
        print(f"   Avg Response Time: {summary['avg_response_time']:.3f}s")
        print(f"   95th Percentile: {summary['p95_response_time']:.3f}s")
        print(f"   Results saved to: {results_file}")
        
    except KeyboardInterrupt:
        print("\n🛑 Load test interrupted")
    except Exception as e:
        print(f"❌ Load test failed: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 