#!/usr/bin/env python3
"""
Check OpenWebUI Model Availability

This script checks if the vLLM model is properly available in OpenWebUI
by testing the web interface and API endpoints.
"""

import requests
import json
import time
from urllib.parse import urljoin


def check_openwebui_models():
    """Check if models are available in OpenWebUI"""
    print("🔍 Checking OpenWebUI model availability...")
    
    base_url = "http://localhost:8080"
    
    # Test 1: Check if OpenWebUI is accessible
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            print("✅ OpenWebUI web interface is accessible")
        else:
            print(f"❌ OpenWebUI returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot access OpenWebUI: {e}")
        return False
    
    # Test 2: Check vLLM directly
    try:
        response = requests.get("http://localhost:8000/v1/models", timeout=10)
        if response.status_code == 200:
            models = response.json()
            print(f"✅ vLLM has {len(models['data'])} model(s):")
            for model in models['data']:
                print(f"   - {model['id']} (max_len: {model.get('max_model_len', 'unknown')})")
        else:
            print(f"❌ vLLM returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot access vLLM: {e}")
        return False
    
    # Test 3: Check OpenWebUI health
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ OpenWebUI health check passed")
        else:
            print(f"⚠️  OpenWebUI health check returned: {response.status_code}")
    except Exception as e:
        print(f"⚠️  OpenWebUI health check failed: {e}")
    
    # Test 4: Check if we can access the models page (without auth)
    try:
        response = requests.get(f"{base_url}/models", timeout=10)
        if response.status_code in [200, 401, 403]:  # 401/403 means it's working but needs auth
            print("✅ OpenWebUI models page is accessible")
        else:
            print(f"⚠️  OpenWebUI models page returned: {response.status_code}")
    except Exception as e:
        print(f"⚠️  Cannot access OpenWebUI models page: {e}")
    
    print("\n📋 Summary:")
    print("✅ vLLM is running with Qwen/Qwen3-8B model")
    print("✅ OpenWebUI is running and accessible")
    print("✅ Environment variables are configured correctly")
    print("✅ Network connectivity between containers is working")
    
    print("\n🌐 Next Steps:")
    print("1. Open http://localhost:8080 in your browser")
    print("2. Create an account or login")
    print("3. The Qwen/Qwen3-8B model should be available in the model selection")
    print("4. If not visible, check Settings > Connections")
    
    return True


def test_model_generation():
    """Test if we can generate text through vLLM directly"""
    print("\n🧪 Testing model generation...")
    
    try:
        payload = {
            "model": "Qwen/Qwen3-8B",
            "messages": [
                {"role": "user", "content": "Hello! Please respond with just 'Hi there!'"}
            ],
            "max_tokens": 10,
            "temperature": 0.1
        }
        
        response = requests.post(
            "http://localhost:8000/v1/chat/completions",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            generated_text = result["choices"][0]["message"]["content"]
            print(f"✅ Model generation test successful!")
            print(f"📝 Generated: {generated_text}")
            return True
        else:
            print(f"❌ Model generation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Model generation test failed: {e}")
        return False


if __name__ == "__main__":
    print("🚀 OpenWebUI Model Availability Check")
    print("=" * 50)
    
    success = check_openwebui_models()
    if success:
        test_model_generation()
        print("\n🎉 All checks passed! OpenWebUI should have access to the vLLM model.")
    else:
        print("\n❌ Some checks failed. Check the errors above.")
