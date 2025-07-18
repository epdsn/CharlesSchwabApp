import http.server
import socketserver
import urllib.parse
import threading
import time

# Global variable to store the redirect URL
redirect_url = None
redirect_received = threading.Event()

class OAuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global redirect_url
        
        # Parse the URL to get query parameters
        parsed_url = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        
        # Store the full URL
        redirect_url = self.path
        
        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        response = """
        <html>
        <body>
        <h2>OAuth Redirect Received!</h2>
        <p>You can close this window and return to your Python script.</p>
        <p>URL: {}</p>
        </body>
        </html>
        """.format(self.path)
        
        self.wfile.write(response.encode())
        
        # Signal that we received the redirect
        redirect_received.set()
    
    def log_message(self, format, *args):
        # Suppress logging for cleaner output
        pass

def start_server(port=8000):
    with socketserver.TCPServer(("", port), OAuthHandler) as httpd:
        print(f"Server started at http://localhost:{port}")
        httpd.serve_forever()

def get_redirect_url():
    global redirect_received, redirect_url
    redirect_received.wait(timeout=300)  # Wait up to 5 minutes
    return redirect_url

if __name__ == '__main__':
    start_server() 