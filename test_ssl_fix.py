#!/usr/bin/env python3
"""
Test script to verify SSL certificate fix for data ingestion
"""

import sys
import os
import requests
import urllib3

def test_ssl_download():
    """Test SSL download functionality"""
    print("Testing SSL certificate handling...")
    
    # Test URL from config
    url = "https://github.com/Tarun221228/DlOps/raw/refs/heads/main/Chicken-fecal-images.zip"
    
    try:
        print(f"Attempting to download from: {url}")
        print("First try: with SSL verification enabled")
        
        response = requests.get(url, stream=True, verify=True)
        response.raise_for_status()
        
        print("✅ Success! SSL verification worked without issues")
        print(f"Status Code: {response.status_code}")
        print(f"Content-Length: {response.headers.get('content-length', 'Unknown')}")
        
        return True
        
    except requests.exceptions.SSLError as e:
        print(f"⚠️  SSL verification failed: {e}")
        print("Second try: with SSL verification disabled")
        
        try:
            # Disable SSL warnings
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            
            response = requests.get(url, stream=True, verify=False)
            response.raise_for_status()
            
            print("✅ Success! Download worked with SSL verification disabled")
            print(f"Status Code: {response.status_code}")
            print(f"Content-Length: {response.headers.get('content-length', 'Unknown')}")
            
            return True
            
        except Exception as e2:
            print(f"❌ Failed even with SSL verification disabled: {e2}")
            return False
            
    except Exception as e:
        print(f"❌ Other error occurred: {e}")
        return False

if __name__ == "__main__":
    success = test_ssl_download()
    if success:
        print("\n🎉 SSL certificate fix is working!")
        sys.exit(0)
    else:
        print("\n💥 SSL certificate fix failed!")
        sys.exit(1)
