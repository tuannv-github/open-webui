#!/usr/bin/env python3
"""
Simple vLLM Test Script

A minimal example to test vLLM text generation.
This script demonstrates basic usage of vLLM API.
"""

import requests
import json


def test_vllm_simple():
    """Simple test function for vLLM"""
    url = "http://localhost:8000/v1/chat/completions"
    
    payload = {
        "model": "Qwen/Qwen3-8B",
        "messages": [
            {"role": "user", "content": "Hello! How are you today?"}
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }
    
    try:
        print("🚀 Testing vLLM connection...")
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            generated_text = result["choices"][0]["message"]["content"]
            print("✅ vLLM is working!")
            print(f"📝 Generated text: {generated_text}")
            return True
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to vLLM. Is it running on localhost:8000?")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    success = test_vllm_simple()
    if success:
        print("\n🎉 vLLM test completed successfully!")
    else:
        print("\n⚠️  vLLM test failed. Check if the service is running.")
