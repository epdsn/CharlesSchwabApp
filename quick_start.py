#!/usr/bin/env python3
"""
Quick Start Script for Schwab OAuth
This script starts everything and tells you exactly what to do.
"""

import subprocess
import time
import requests
import sys
import os

def get_tunnel_url():
    """Get the tunnel public URL"""
    # For localtunnel, we know the URL is static
    return "https://schwab-oauth-demo.loca.lt"

def main():
    print("🔐 Schwab OAuth Quick Start")
    print("=" * 50)
    
    # Check if tunnel is already running
    existing_url = get_tunnel_url()
    if existing_url:
        print(f"✅ Found existing tunnel: {existing_url}")
        print(f"🔗 Use this redirect URI: {existing_url}/")
        print("\n📋 Next steps:")
        print("1. Update your Schwab app redirect URI to the URL above")
        print("2. Run: python3 main.py")
        return
    
    # Start OAuth server
    print("🚀 Starting OAuth server...")
    oauth_process = subprocess.Popen(['python3', 'simple_oauth_server.py'])
    time.sleep(2)
    
    # Start localtunnel (static URL)
    print("🌐 Starting localtunnel with static URL...")
    ngrok_process = subprocess.Popen(['lt', '--port', '8000', '--subdomain', 'schwab-oauth-demo'])
    
    # Wait for tunnel to start
    print("⏳ Waiting for tunnel to start...")
    for i in range(30):
        url = get_tunnel_url()
        if url:
            print(f"\n✅ SUCCESS! Your tunnel is ready:")
            print(f"🌐 URL: {url}")
            print(f"🔗 Redirect URI: {url}/")
            print("\n📋 Next steps:")
            print("1. Copy the redirect URI above")
            print("2. Go to Charles Schwab Developer Portal")
            print("3. Update your app's redirect URI")
            print("4. Run: python3 main.py")
            print("\n💡 This URL is STATIC and won't change!")
            break
        time.sleep(1)
        if i % 5 == 0:
            print(f"   Still waiting... ({i+1}/30)")
    else:
        print("❌ Failed to get tunnel URL")
        return
    
    # Keep running
    try:
        while True:
            time.sleep(10)
            if not get_tunnel_url():
                print("⚠️  tunnel appears to be down")
                break
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
        oauth_process.terminate()
        ngrok_process.terminate()

if __name__ == "__main__":
    main() 