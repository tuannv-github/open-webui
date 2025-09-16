#!/usr/bin/env python3
"""
Test OpenWebUI Integration with vLLM

This script tests if OpenWebUI can properly connect to vLLM
and access the available models.
"""

import requests
import json
import time


def test_openwebui_vllm_integration():
    """Test OpenWebUI integration with vLLM"""
    print("🔍 Testing OpenWebUI integration with vLLM...")
    
    # Test 1: Check if OpenWebUI is accessible
    try:
        response = requests.get("http://localhost:8080", timeout=10)
        if response.status_code == 200:
            print("✅ OpenWebUI web interface is accessible")
        else:
            print(f"❌ OpenWebUI returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot access OpenWebUI: {e}")
        return False
    
    # Test 2: Check if vLLM is accessible from OpenWebUI's perspective
    try:
        # Test internal Docker network connection
        response = requests.get("http://vllm:8000/v1/models", timeout=10)
        if response.status_code == 200:
            print("✅ vLLM is accessible from Docker network")
            models = response.json()
            print(f"📋 Available models: {[model['id'] for model in models['data']]}")
        else:
            print(f"❌ vLLM returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot access vLLM from Docker network: {e}")
        return False
    
    # Test 3: Check OpenWebUI health
    try:
        response = requests.get("http://localhost:8080/health", timeout=10)
        if response.status_code == 200:
            print("✅ OpenWebUI health check passed")
        else:
            print(f"⚠️  OpenWebUI health check returned: {response.status_code}")
    except Exception as e:
        print(f"⚠️  OpenWebUI health check failed: {e}")
    
    print("\n🎉 Integration test completed!")
    print("\n📝 Next steps:")
    print("1. Open http://localhost:8080 in your browser")
    print("2. Create an account or login")
    print("3. Go to Settings > Connections")
    print("4. Add a new connection with:")
    print("   - Name: vLLM")
    print("   - Base URL: http://vllm:8000/v1")
    print("   - API Key: (leave empty)")
    print("5. Select the Qwen/Qwen3-8B model")
    
    return True


if __name__ == "__main__":
    success = test_openwebui_vllm_integration()
    if success:
        print("\n✅ All tests passed! OpenWebUI should be able to connect to vLLM.")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
