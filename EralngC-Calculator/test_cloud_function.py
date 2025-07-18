#!/usr/bin/env python3
"""
Test script for Erlang C Server Cloud Function
Run this script to verify your deployment is working correctly.
"""

import requests
import json
import time
import sys

def test_cloud_function(base_url):
    """Test all endpoints of the deployed Cloud Function"""
    
    print(f"🧪 Testing Erlang C Server at: {base_url}")
    print("=" * 60)
    
    # Test 1: Health Check
    print("\n1️⃣  Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: Server Info
    print("\n2️⃣  Testing Server Info...")
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            print("✅ Server info retrieved")
            data = response.json()
            print(f"   Message: {data.get('message', 'N/A')}")
            print(f"   Version: {data.get('version', 'N/A')}")
        else:
            print(f"❌ Server info failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Server info error: {e}")
    
    # Test 3: Basic Simulation
    print("\n3️⃣  Testing Basic Simulation...")
    simulation_data = {
        "arrival_rate": 1.67,
        "mean_service_time": 5,
        "num_servers": 12,
        "sim_time": 500,  # Shorter for testing
        "sla_target_pct": 80,
        "sla_threshold_seconds": 20
    }
    
    try:
        response = requests.post(
            f"{base_url}/simulate",
            json=simulation_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Basic simulation successful")
            data = response.json()
            
            if 'error' in data:
                print(f"❌ Simulation error: {data['error']}")
                return False
            
            print(f"   Wait Time: {data.get('avg_wait_time_seconds', 'N/A')} seconds")
            print(f"   Service Level: {data.get('service_level_achieved', 'N/A')}%")
            print(f"   Utilization: {data.get('utilization', 'N/A')}%")
            print(f"   Total Customers: {data.get('total_customers', 'N/A')}")
        else:
            print(f"❌ Basic simulation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Basic simulation error: {e}")
        return False
    
    # Test 4: Distribution Simulation (Normal)
    print("\n4️⃣  Testing Distribution Simulation (Normal)...")
    normal_data = {
        "arrival_rate": 1.67,
        "mean_service_time": 5,
        "num_servers": 12,
        "sim_time": 300,
        "sla_target_pct": 80,
        "sla_threshold_seconds": 20,
        "service_distribution": "normal",
        "service_std_dev": 2
    }
    
    try:
        response = requests.post(
            f"{base_url}/simulate",
            json=normal_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'error' not in data:
                print("✅ Normal distribution simulation successful")
                print(f"   Service Level: {data.get('service_level_achieved', 'N/A')}%")
            else:
                print(f"❌ Normal distribution error: {data['error']}")
        else:
            print(f"⚠️  Normal distribution failed: {response.status_code}")
    except Exception as e:
        print(f"⚠️  Normal distribution error: {e}")
    
    # Test 5: Optimization
    print("\n5️⃣  Testing Optimization...")
    optimization_data = {
        "arrival_rate": 1.67,
        "mean_service_time": 5,
        "target_service_level": 80,
        "sla_threshold_seconds": 20,
        "min_agents": 8,
        "max_agents": 20,
        "num_replications": 2  # Fewer replications for testing
    }
    
    try:
        response = requests.post(
            f"{base_url}/optimize",
            json=optimization_data,
            headers={'Content-Type': 'application/json'},
            timeout=60  # Longer timeout for optimization
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'error' not in data:
                print("✅ Optimization successful")
                print(f"   Minimum Agents: {data.get('minimum_agents_needed', 'N/A')}")
                print(f"   Achieved SL: {data.get('achieved_service_level', 'N/A')}%")
            else:
                print(f"❌ Optimization error: {data['error']}")
        else:
            print(f"❌ Optimization failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Optimization error: {e}")
    
    # Test 6: CORS Check
    print("\n6️⃣  Testing CORS...")
    try:
        # OPTIONS request
        response = requests.options(f"{base_url}/simulate", timeout=10)
        if response.status_code in [200, 204]:
            print("✅ CORS preflight working")
            cors_headers = {
                'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
            }
            print(f"   CORS Headers: {cors_headers}")
        else:
            print(f"⚠️  CORS preflight issue: {response.status_code}")
    except Exception as e:
        print(f"⚠️  CORS test error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Testing completed!")
    print("\n💡 If tests passed, your Cloud Function is ready for use!")
    print("📝 Update your frontend to use this URL instead of localhost:5000")
    return True


def main():
    """Main test function"""
    if len(sys.argv) != 2:
        print("Usage: python test_cloud_function.py <FUNCTION_URL>")
        print("\nExample:")
        print("python test_cloud_function.py https://us-central1-myproject.cloudfunctions.net/erlang-c-server")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    
    print("🔗 Erlang C Server Cloud Function Tester")
    print(f"🎯 Target URL: {base_url}")
    print(f"⏰ Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    success = test_cloud_function(base_url)
    
    if success:
        print("\n✅ All critical tests passed! Your deployment is working.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Check the logs and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main() 