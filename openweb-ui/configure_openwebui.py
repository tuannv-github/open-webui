#!/usr/bin/env python3
"""
OpenWebUI Configuration Helper

This script helps configure OpenWebUI to connect to vLLM by providing
step-by-step instructions and testing the connection.
"""

import requests
import json
import time


def test_vllm_connection():
    """Test if vLLM is accessible"""
    print("🔍 Testing vLLM connection...")
    
    try:
        response = requests.get("http://localhost:8000/v1/models", timeout=10)
        if response.status_code == 200:
            models = response.json()
            print(f"✅ vLLM is accessible with {len(models['data'])} model(s)")
            for model in models['data']:
                print(f"   - {model['id']}")
            return True
        else:
            print(f"❌ vLLM returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to vLLM: {e}")
        return False


def test_openwebui_connection():
    """Test if OpenWebUI is accessible"""
    print("\n🔍 Testing OpenWebUI connection...")
    
    try:
        response = requests.get("http://localhost:8080", timeout=10)
        if response.status_code == 200:
            print("✅ OpenWebUI is accessible")
            return True
        else:
            print(f"❌ OpenWebUI returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to OpenWebUI: {e}")
        return False


def provide_configuration_instructions():
    """Provide step-by-step configuration instructions"""
    print("\n📋 OpenWebUI Configuration Instructions:")
    print("=" * 50)
    
    print("\n1. 🌐 Open OpenWebUI in your browser:")
    print("   http://localhost:8080")
    
    print("\n2. 👤 Create an account or login")
    
    print("\n3. ⚙️  Go to Settings (gear icon in top right)")
    
    print("\n4. 🔗 Navigate to 'Connections' tab")
    
    print("\n5. ➕ Click 'Add Connection' or 'New Connection'")
    
    print("\n6. 📝 Fill in the connection details:")
    print("   - Name: vLLM")
    print("   - Base URL: http://vllm:8000/v1")
    print("   - API Key: (leave empty)")
    print("   - Model: Qwen/Qwen3-8B")
    
    print("\n7. ✅ Click 'Test Connection' to verify")
    
    print("\n8. 💾 Save the connection")
    
    print("\n9. 🔄 Refresh the models list")
    
    print("\n10. 🎯 The model should now appear in the model dropdown")


def test_docker_network_connectivity():
    """Test if OpenWebUI can reach vLLM from within Docker network"""
    print("\n🔍 Testing Docker network connectivity...")
    
    try:
        # Test from OpenWebUI container to vLLM
        import subprocess
        result = subprocess.run([
            "docker", "exec", "open-webui", 
            "curl", "-s", "http://vllm:8000/v1/models"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            models = json.loads(result.stdout)
            print(f"✅ OpenWebUI can reach vLLM: {len(models['data'])} model(s) found")
            return True
        else:
            print(f"❌ OpenWebUI cannot reach vLLM: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Network test failed: {e}")
        return False


def main():
    """Main function"""
    print("🚀 OpenWebUI Configuration Helper")
    print("=" * 50)
    
    # Test connections
    vllm_ok = test_vllm_connection()
    openwebui_ok = test_openwebui_connection()
    network_ok = test_docker_network_connectivity()
    
    if vllm_ok and openwebui_ok and network_ok:
        print("\n✅ All connections are working!")
        provide_configuration_instructions()
        
        print("\n🔧 Alternative: Manual Configuration via Environment")
        print("If the web interface doesn't work, try these environment variables:")
        print("   OPENAI_API_BASE_URL=http://vllm:8000/v1")
        print("   OPENAI_API_KEY=EMPTY")
        print("   ENABLE_OPENAI_API=true")
        
    else:
        print("\n❌ Some connections are not working. Please check:")
        if not vllm_ok:
            print("   - vLLM service is not running or accessible")
        if not openwebui_ok:
            print("   - OpenWebUI service is not running or accessible")
        if not network_ok:
            print("   - Docker network connectivity issues")


if __name__ == "__main__":
    main()
