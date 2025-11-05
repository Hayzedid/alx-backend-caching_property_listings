#!/usr/bin/env python
"""
Test script to verify caching functionality.
Run this after setting up the project and starting the services.
"""

import requests
import time
import json

BASE_URL = 'http://127.0.0.1:8000'

def test_property_list_caching():
    """Test property list endpoint caching"""
    print("🏠 Testing Property List Caching...")
    
    url = f"{BASE_URL}/properties/"
    
    # First request (should hit database)
    print("📡 Making first request (cache miss expected)...")
    start_time = time.time()
    response1 = requests.get(url)
    end_time = time.time()
    
    if response1.status_code == 200:
        data1 = response1.json()
        print(f"✅ First request successful: {data1['count']} properties found")
        print(f"⏱️  Response time: {(end_time - start_time)*1000:.2f}ms")
    else:
        print(f"❌ First request failed: {response1.status_code}")
        return
    
    # Second request (should hit cache)
    print("\n📡 Making second request (cache hit expected)...")
    start_time = time.time()
    response2 = requests.get(url)
    end_time = time.time()
    
    if response2.status_code == 200:
        data2 = response2.json()
        print(f"✅ Second request successful: {data2['count']} properties found")
        print(f"⏱️  Response time: {(end_time - start_time)*1000:.2f}ms")
        
        # Compare data
        if data1 == data2:
            print("✅ Data consistency: Both responses are identical")
        else:
            print("❌ Data inconsistency: Responses differ")
    else:
        print(f"❌ Second request failed: {response2.status_code}")


def test_cache_metrics():
    """Test cache metrics endpoint"""
    print("\n📊 Testing Cache Metrics...")
    
    url = f"{BASE_URL}/properties/cache-metrics/"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            metrics = data['cache_metrics']
            
            print("✅ Cache metrics retrieved successfully:")
            print(f"   🎯 Cache Hits: {metrics['keyspace_hits']}")
            print(f"   ❌ Cache Misses: {metrics['keyspace_misses']}")
            print(f"   📈 Total Requests: {metrics['total_requests']}")
            print(f"   📊 Hit Ratio: {metrics['hit_ratio']}%")
        else:
            print(f"❌ Cache metrics request failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")


def main():
    """Main test function"""
    print("🚀 ALX Backend Caching Property Listings - Test Suite")
    print("=" * 60)
    
    try:
        # Test if server is running
        response = requests.get(f"{BASE_URL}/admin/", timeout=5)
        print("✅ Django server is running")
    except requests.exceptions.RequestException:
        print("❌ Django server is not running. Please start it with: python manage.py runserver")
        return
    
    # Run tests
    test_property_list_caching()
    test_cache_metrics()
    
    print("\n" + "=" * 60)
    print("🎉 Test suite completed!")
    print("\n💡 Tips:")
    print("   - Run multiple requests to see caching in action")
    print("   - Create/update/delete properties to test cache invalidation")
    print("   - Monitor cache metrics to optimize performance")


if __name__ == "__main__":
    main()
