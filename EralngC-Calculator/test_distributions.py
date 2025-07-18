#!/usr/bin/env python3
"""
Test script for distribution implementations in the Erlang C simulation server.
This script tests all supported distributions with various parameter combinations.
"""

import requests
import json
import time
import statistics

# Server configuration
SERVER_URL = "http://localhost:5000"

def test_distribution(distribution_name, distribution_params, test_name=""):
    """Test a specific distribution with given parameters"""
    print(f"\n🔬 Testing {distribution_name} distribution{' - ' + test_name if test_name else ''}")
    
    # Base payload
    payload = {
        'arrival_rate': 1.67,  # 100 calls/hour converted to per-minute
        'mean_service_time': 5.0,  # 5 minutes
        'service_distribution': distribution_name,
        'num_servers': 12,
        'sim_time': 100,  # Shorter simulation for testing
        'sla_target_pct': 80,
        'sla_threshold_seconds': 20,
        'seed': 42  # Fixed seed for reproducible results
    }
    
    # Add distribution-specific parameters
    payload.update(distribution_params)
    
    try:
        # Test simulate endpoint
        print(f"   📊 Testing /simulate endpoint...")
        response = requests.post(f"{SERVER_URL}/simulate", json=payload, timeout=30)
        
        if response.status_code != 200:
            print(f"   ❌ HTTP Error {response.status_code}: {response.text}")
            return False
            
        result = response.json()
        
        if 'error' in result:
            print(f"   ❌ Simulation Error: {result['error']}")
            return False
        
        # Validate results
        required_fields = ['total_arrivals', 'total_served', 'avg_wait_seconds', 'pct_within_sla', 'utilization_pct']
        for field in required_fields:
            if field not in result:
                print(f"   ❌ Missing field: {field}")
                return False
        
        print(f"   ✅ Simulation successful:")
        print(f"      • Total arrivals: {result['total_arrivals']}")
        print(f"      • Service level: {result['pct_within_sla']:.1f}%")
        print(f"      • Utilization: {result['utilization_pct']:.1f}%")
        print(f"      • Avg wait: {result['avg_wait_seconds']:.2f}s")
        
        # Test optimize endpoint (shorter test)
        print(f"   🎯 Testing /optimize endpoint...")
        optimize_payload = payload.copy()
        optimize_payload.update({
            'sim_time': 50,  # Even shorter for optimization
            'max_agents': 20,  # Limit search space
            'num_replications': 2  # Fewer replications for testing
        })
        
        response = requests.post(f"{SERVER_URL}/optimize", json=optimize_payload, timeout=60)
        
        if response.status_code != 200:
            print(f"   ❌ Optimize HTTP Error {response.status_code}: {response.text}")
            return False
            
        optimize_result = response.json()
        
        if 'error' in optimize_result:
            print(f"   ❌ Optimization Error: {optimize_result['error']}")
            return False
            
        if 'minimum_agents' not in optimize_result:
            print(f"   ❌ Missing minimum_agents in optimization result")
            return False
            
        print(f"   ✅ Optimization successful:")
        print(f"      • Minimum agents: {optimize_result['minimum_agents']}")
        print(f"      • Average SLA: {optimize_result['avg_sla_percentage']:.1f}%")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection Error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected Error: {e}")
        return False

def test_all_distributions():
    """Test all supported distributions"""
    print("🚀 Starting comprehensive distribution testing")
    print("="*60)
    
    # Test server connectivity
    try:
        response = requests.get(f"{SERVER_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ Server not available. Please start SimpleErlangC_server.py")
            return False
        print("✅ Server is running and healthy")
    except:
        print("❌ Cannot connect to server. Please start SimpleErlangC_server.py")
        return False
    
    test_results = []
    
    # Test 1: Exponential Distribution (baseline)
    success = test_distribution('exponential', {}, "baseline test")
    test_results.append(('Exponential (baseline)', success))
    
    # Test 2: Normal Distribution
    success = test_distribution('normal', {
        'service_std_dev': 1.0  # 1 minute std dev
    }, "1 min std dev")
    test_results.append(('Normal (1 min std dev)', success))
    
    # Test 3: Normal Distribution with high variability
    success = test_distribution('normal', {
        'service_std_dev': 2.0  # 2 minutes std dev
    }, "high variability")
    test_results.append(('Normal (high variability)', success))
    
    # Test 4: Lognormal Distribution
    success = test_distribution('lognormal', {
        'service_cv': 0.5  # Moderate variability
    }, "CV=0.5")
    test_results.append(('Lognormal (CV=0.5)', success))
    
    # Test 5: Lognormal Distribution with high variability
    success = test_distribution('lognormal', {
        'service_cv': 1.0  # High variability
    }, "high variability")
    test_results.append(('Lognormal (high variability)', success))
    
    # Test 6: Uniform Distribution
    success = test_distribution('uniform', {
        'service_range_factor': 0.3  # ±30% of mean
    }, "±30% range")
    test_results.append(('Uniform (±30%)', success))
    
    # Test 7: Uniform Distribution with wide range
    success = test_distribution('uniform', {
        'service_range_factor': 0.8  # ±80% of mean
    }, "wide range")
    test_results.append(('Uniform (wide range)', success))
    
    # Test 8: Gamma Distribution
    success = test_distribution('gamma', {
        'service_cv': 0.5  # Moderate variability
    }, "CV=0.5")
    test_results.append(('Gamma (CV=0.5)', success))
    
    # Test 9: Gamma Distribution with low variability
    success = test_distribution('gamma', {
        'service_cv': 0.2  # Low variability (more like deterministic)
    }, "low variability")
    test_results.append(('Gamma (low variability)', success))
    
    # Test 10: Deterministic Distribution
    success = test_distribution('deterministic', {}, "constant service time")
    test_results.append(('Deterministic', success))
    
    # Summary
    print("\n" + "="*60)
    print("📋 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, success in test_results if success)
    total = len(test_results)
    
    for test_name, success in test_results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n📊 Overall Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All distribution tests passed successfully!")
        return True
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return False

def test_error_handling():
    """Test error handling with invalid parameters"""
    print("\n🛡️  Testing error handling with invalid parameters")
    print("="*60)
    
    error_tests = [
        {
            'name': 'Normal with negative std dev',
            'distribution': 'normal',
            'params': {'service_std_dev': -1.0},
            'should_fail': True
        },
        {
            'name': 'Lognormal with zero CV',
            'distribution': 'lognormal', 
            'params': {'service_cv': 0.0},
            'should_fail': True
        },
        {
            'name': 'Uniform with invalid range factor',
            'distribution': 'uniform',
            'params': {'service_range_factor': 1.5},
            'should_fail': True
        },
        {
            'name': 'Gamma with negative CV',
            'distribution': 'gamma',
            'params': {'service_cv': -0.5},
            'should_fail': True
        }
    ]
    
    error_results = []
    
    for test in error_tests:
        print(f"\n🔍 Testing: {test['name']}")
        
        payload = {
            'arrival_rate': 1.67,
            'mean_service_time': 5.0,
            'service_distribution': test['distribution'],
            'num_servers': 12,
            'sim_time': 10,  # Very short simulation
            'sla_target_pct': 80,
            'sla_threshold_seconds': 20,
            'seed': 42
        }
        payload.update(test['params'])
        
        try:
            response = requests.post(f"{SERVER_URL}/simulate", json=payload, timeout=10)
            result = response.json()
            
            has_error = 'error' in result or response.status_code != 200
            
            if test['should_fail']:
                if has_error:
                    print(f"   ✅ Correctly rejected invalid parameters")
                    error_results.append(True)
                else:
                    print(f"   ❌ Should have failed but didn't")
                    error_results.append(False)
            else:
                if not has_error:
                    print(f"   ✅ Correctly accepted valid parameters")
                    error_results.append(True)
                else:
                    print(f"   ❌ Should have succeeded but failed: {result.get('error', 'Unknown error')}")
                    error_results.append(False)
                    
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")
            error_results.append(False)
    
    passed = sum(error_results)
    total = len(error_results)
    print(f"\n📊 Error handling tests: {passed}/{total} passed ({passed/total*100:.1f}%)")
    
    return passed == total

if __name__ == "__main__":
    print("🧪 Distribution Testing Suite for Erlang C Simulation Server")
    print("Make sure SimpleErlangC_server.py is running before executing tests!")
    
    # Run main distribution tests
    main_success = test_all_distributions()
    
    # Run error handling tests
    error_success = test_error_handling()
    
    # Final summary
    print("\n" + "="*60)
    print("🏁 FINAL RESULTS")
    print("="*60)
    
    if main_success and error_success:
        print("🎉 ALL TESTS PASSED! Distribution implementation is working correctly.")
        exit(0)
    else:
        print("❌ SOME TESTS FAILED. Please review the implementation.")
        exit(1) 