#!/usr/bin/env python3
"""
vLLM Health Check and Test Script

This script checks if vLLM is running and tests its functionality.
It connects to the vLLM service running on localhost:8000 and performs
various tests including health checks and text generation.
"""

import requests
import json
import time
import sys
from typing import Dict, Any, Optional


class VLLMChecker:
    """vLLM service checker and tester"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.timeout = 30
    
    def check_health(self) -> Dict[str, Any]:
        """Check if vLLM service is healthy"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                return {
                    "status": "healthy",
                    "response": response.json() if response.content else {"message": "OK"}
                }
            else:
                return {
                    "status": "unhealthy",
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
        except requests.exceptions.ConnectionError:
            return {
                "status": "unreachable",
                "error": "Cannot connect to vLLM service. Is it running?"
            }
        except requests.exceptions.Timeout:
            return {
                "status": "timeout",
                "error": "Request timed out"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def get_models(self) -> Dict[str, Any]:
        """Get available models from vLLM"""
        try:
            response = self.session.get(f"{self.base_url}/v1/models")
            if response.status_code == 200:
                return {
                    "status": "success",
                    "models": response.json()
                }
            else:
                return {
                    "status": "error",
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def generate_text(self, prompt: str, max_tokens: int = 100, temperature: float = 0.7) -> Dict[str, Any]:
        """Generate text using vLLM"""
        payload = {
            "model": "Qwen/Qwen3-8B",  # Based on docker-compose configuration
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": False
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/v1/chat/completions",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "status": "success",
                    "response": result,
                    "generated_text": result.get("choices", [{}])[0].get("message", {}).get("content", "")
                }
            else:
                return {
                    "status": "error",
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run a comprehensive test of vLLM functionality"""
        results = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "base_url": self.base_url,
            "tests": {}
        }
        
        print("🔍 Checking vLLM service...")
        
        # Test 1: Health Check
        print("1. Health Check...")
        health_result = self.check_health()
        results["tests"]["health"] = health_result
        print(f"   Status: {health_result['status']}")
        if health_result['status'] != 'healthy':
            print(f"   Error: {health_result.get('error', 'Unknown error')}")
            return results
        
        # Test 2: Get Models
        print("2. Getting available models...")
        models_result = self.get_models()
        results["tests"]["models"] = models_result
        if models_result['status'] == 'success':
            model_count = len(models_result['models'].get('data', []))
            print(f"   Found {model_count} model(s)")
            for model in models_result['models'].get('data', []):
                print(f"   - {model.get('id', 'Unknown')}")
        else:
            print(f"   Error: {models_result.get('error', 'Unknown error')}")
        
        # Test 3: Simple Text Generation
        print("3. Testing text generation...")
        simple_prompt = "Hello! Please respond with a brief greeting."
        generation_result = self.generate_text(simple_prompt, max_tokens=50)
        results["tests"]["simple_generation"] = generation_result
        if generation_result['status'] == 'success':
            generated_text = generation_result.get('generated_text', '')
            print(f"   Generated: {generated_text[:100]}{'...' if len(generated_text) > 100 else ''}")
        else:
            print(f"   Error: {generation_result.get('error', 'Unknown error')}")
        
        # Test 4: Complex Text Generation
        print("4. Testing complex text generation...")
        complex_prompt = "Explain the concept of artificial intelligence in 2-3 sentences."
        complex_result = self.generate_text(complex_prompt, max_tokens=150, temperature=0.5)
        results["tests"]["complex_generation"] = complex_result
        if complex_result['status'] == 'success':
            generated_text = complex_result.get('generated_text', '')
            print(f"   Generated: {generated_text[:150]}{'...' if len(generated_text) > 150 else ''}")
        else:
            print(f"   Error: {complex_result.get('error', 'Unknown error')}")
        
        return results


def main():
    """Main function to run vLLM checks"""
    print("🚀 vLLM Health Check and Test Script")
    print("=" * 50)
    
    # Allow custom URL via command line argument
    base_url = "http://localhost:8000"
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    checker = VLLMChecker(base_url)
    
    # Run comprehensive test
    results = checker.run_comprehensive_test()
    
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    
    # Count successful tests
    successful_tests = 0
    total_tests = len(results["tests"])
    
    for test_name, test_result in results["tests"].items():
        status = test_result.get("status", "unknown")
        if status in ["success", "healthy"]:
            successful_tests += 1
            print(f"✅ {test_name}: {status}")
        else:
            print(f"❌ {test_name}: {status}")
            if "error" in test_result:
                print(f"   Error: {test_result['error']}")
    
    print(f"\n🎯 Results: {successful_tests}/{total_tests} tests passed")
    
    if successful_tests == total_tests:
        print("🎉 All tests passed! vLLM is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
