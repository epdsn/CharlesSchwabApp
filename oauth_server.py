from flask import Flask, request
import threading
import time

app = Flask(__name__)

# Global variable to store the redirect URL
redirect_url = None
redirect_received = threading.Event()

@app.route('/')
def oauth_callback():
    global redirect_url
    redirect_url = request.url
    redirect_received.set()
    return "OAuth redirect received! You can close this window and return to your Python script."

def start_server():
    app.run(host='127.0.0.1', port=8000, debug=False)

def get_redirect_url():
    global redirect_received, redirect_url
    redirect_received.wait(timeout=300)  # Wait up to 5 minutes
    return redirect_url

if __name__ == '__main__':
    start_server() 