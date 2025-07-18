#!/usr/bin/env python3
"""
OAuth Server Starter with ngrok Integration
This script starts the OAuth server and ngrok, then helps you update your redirect URI.
"""

import subprocess
import time
import requests
import json
import os
import sys
from threading import Thread

def get_ngrok_url():
    """Get the ngrok public URL from the ngrok API"""
    try:
        response = requests.get('http://localhost:4040/api/tunnels')
        if response.status_code == 200:
            tunnels = response.json()['tunnels']
            for tunnel in tunnels:
                if tunnel['proto'] == 'https':
                    return tunnel['public_url']
    except:
        pass
    return None

def start_oauth_server():
    """Start the OAuth server in the background"""
    print("🚀 Starting OAuth server on port 8000...")
    subprocess.Popen([sys.executable, 'simple_oauth_server.py'])

def start_ngrok():
    """Start ngrok tunnel"""
    print("🌐 Starting ngrok tunnel...")
    subprocess.Popen(['ngrok', 'http', '8000'])

def wait_for_ngrok():
    """Wait for ngrok to start and return the URL"""
    print("⏳ Waiting for ngrok to start...")
    for i in range(30):  # Wait up to 30 seconds
        url = get_ngrok_url()
        if url:
            return url
        time.sleep(1)
        if i % 5 == 0:
            print(f"   Still waiting... ({i+1}/30 seconds)")
    return None

def main():
    print("=" * 60)
    print("🔐 Schwab OAuth Server Starter")
    print("=" * 60)
    
    # Start OAuth server
    start_oauth_server()
    time.sleep(2)
    
    # Start ngrok
    start_ngrok()
    
    # Wait for ngrok URL
    ngrok_url = wait_for_ngrok()
    
    if not ngrok_url:
        print("❌ Failed to get ngrok URL. Please check if ngrok is running.")
        return
    
    print("\n" + "=" * 60)
    print("✅ SUCCESS! Your OAuth server is ready.")
    print("=" * 60)
    print(f"🌐 Public URL: {ngrok_url}")
    print(f"🔗 Redirect URI: {ngrok_url}/")
    print("\n📋 NEXT STEPS:")
    print("1. Go to your Charles Schwab Developer Portal")
    print("2. Update your app's redirect URI to:")
    print(f"   {ngrok_url}/")
    print("3. Run: python main.py")
    print("\n💡 TIP: This URL will change each time you restart ngrok.")
    print("   Consider upgrading to ngrok paid plan for static URLs.")
    print("=" * 60)
    
    # Keep the script running
    try:
        while True:
            time.sleep(10)
            url = get_ngrok_url()
            if not url:
                print("⚠️  ngrok tunnel appears to be down. Restart the script.")
                break
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")

if __name__ == "__main__":
    main() 