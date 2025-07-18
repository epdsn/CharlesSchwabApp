#!/usr/bin/env python3
"""
OAuth Server Starter with Cloudflare Tunnel
This script starts the OAuth server and creates a static tunnel URL.
"""

import subprocess
import time
import sys
import os

def start_oauth_server():
    """Start the OAuth server in the background"""
    print("🚀 Starting OAuth server on port 8000...")
    subprocess.Popen([sys.executable, 'simple_oauth_server.py'])
    time.sleep(2)

def start_cloudflared_tunnel():
    """Start cloudflared tunnel with a custom subdomain"""
    print("🌐 Starting Cloudflare tunnel...")
    print("📝 This will create a static URL that won't change!")
    
    # Try to create a tunnel with a custom subdomain
    try:
        # First, try to authenticate with Cloudflare (if needed)
        print("🔐 Authenticating with Cloudflare...")
        auth_process = subprocess.run(['cloudflared', 'tunnel', 'login'], 
                                    capture_output=True, text=True)
        
        if auth_process.returncode == 0:
            print("✅ Authentication successful!")
        else:
            print("ℹ️  Authentication may be required. Follow the browser prompt if it opens.")
        
        # Create and start the tunnel
        print("🚇 Creating tunnel...")
        tunnel_process = subprocess.Popen([
            'cloudflared', 'tunnel', 
            '--url', 'http://localhost:8000',
            '--hostname', 'schwab-oauth-demo.your-domain.com'  # You'll need to replace this
        ])
        
        return tunnel_process
        
    except Exception as e:
        print(f"❌ Error with cloudflared: {e}")
        print("🔄 Falling back to ngrok...")
        return start_ngrok_fallback()

def start_ngrok_fallback():
    """Fallback to ngrok if cloudflared fails"""
    print("🌐 Starting ngrok tunnel...")
    return subprocess.Popen(['ngrok', 'http', '8000'])

def main():
    print("=" * 60)
    print("🔐 Schwab OAuth Server Starter (Cloudflare Edition)")
    print("=" * 60)
    
    # Start OAuth server
    start_oauth_server()
    
    # Start tunnel
    tunnel_process = start_cloudflared_tunnel()
    
    print("\n" + "=" * 60)
    print("✅ Your OAuth server is starting up!")
    print("=" * 60)
    print("\n📋 NEXT STEPS:")
    print("1. Wait for the tunnel URL to appear above")
    print("2. Copy the HTTPS URL (starts with https://)")
    print("3. Go to your Charles Schwab Developer Portal")
    print("4. Update your app's redirect URI to: [URL]/")
    print("5. Run: python main.py")
    print("\n💡 TIP: With Cloudflare, you can get a static URL!")
    print("   To set up a custom domain, run: cloudflared tunnel login")
    print("=" * 60)
    
    try:
        # Keep the script running
        tunnel_process.wait()
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
        tunnel_process.terminate()

if __name__ == "__main__":
    main() 