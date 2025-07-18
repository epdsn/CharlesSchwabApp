# Schwab OAuth Demo Application

This is a simple Python application that demonstrates OAuth 2.0 authentication with the Schwab API. The application authenticates with Schwab, obtains access tokens, and makes API calls to retrieve account information.

## Prerequisites

### 1. Python Installation
- **Python 3.9+** (recommended: Python 3.12)
- **pyenv** (optional but recommended for Python version management)

### 2. Required Python Packages
```bash
pip install requests
```

### 3. ngrok Installation
Install ngrok for creating secure tunnels for OAuth redirects:
```bash
# macOS (using Homebrew)
brew install ngrok

# Or download from https://ngrok.com/download
```

### 4. Schwab API Credentials
You need to register your application with Schwab to get:
- **App Key** (Client ID)
- **App Secret** (Client Secret)

## Setup Instructions

### 1. Clone or Download the Project
```bash
git clone <repository-url>
cd CSTradeAppSimpleDemo
```

### 2. Configure Your Credentials
Edit `main.py` and replace the placeholder credentials:
```python
appKey = "your_app_key_here"
appSecret = "your_app_secret_here"
```

### 3. Start ngrok Tunnel
Open a new terminal window and run:
```bash
ngrok http 8000
```

This will create a secure tunnel and display a URL like:
```
Forwarding    https://abc123.ngrok-free.app -> http://localhost:8000
```

### 4. Update Redirect URI
Copy the ngrok URL and update it in `main.py`:
```python
# Replace the redirect_uri in both places:
auhthUrl = f'https://api.schwabapi.com/v1/oauth/authorize?client_id={appKey}&redirect_uri=https://YOUR_NGROK_URL.ngrok-free.app&state=12345'

data = {
    'grant_type': 'authorization_code', 
    'code': code, 
    'redirect_uri': 'https://YOUR_NGROK_URL.ngrok-free.app'
}
```

## Running the Application

### 1. Execute the Script
```bash
python3 main.py
```

### 2. Complete OAuth Flow
1. **Click the authorization URL** that appears in the terminal
2. **Log in to your Schwab account** in the browser
3. **Authorize the application** when prompted
4. **Copy the redirect URL** from your browser's address bar
5. **Paste it back into the terminal** and press Enter

### 3. View Results
The script will:
- Exchange the authorization code for access tokens
- Display the token response
- Make an API call to retrieve account information
- Show the API response

## Expected Output

```
Click to authenticate: https://api.schwabapi.com/v1/oauth/authorize?client_id=...
Paste the redirect URL here and press Enter: https://your-ngrok-url.ngrok-free.app/?code=...
Token response status: 200
Token response: {"expires_in":1800,"token_type":"Bearer",...}
Account API response status: 200
Account API response: {...}
```

## Troubleshooting

### Common Issues

1. **"Authorization code expired"**
   - Complete the OAuth flow more quickly
   - Authorization codes typically expire in 5-10 minutes

2. **"ngrok tunnel offline"**
   - Restart ngrok: `ngrok http 8000`
   - Update the redirect URI in the script with the new ngrok URL

3. **"404 Not Found" on API calls**
   - Check if the API endpoint is correct
   - Verify your app has the required permissions
   - Consult Schwab API documentation

4. **"Invalid redirect URI"**
   - Ensure the redirect URI in your script matches exactly what's registered with Schwab
   - Check for typos in the ngrok URL

### Python Version Issues

If you encounter Python version issues:
```bash
# Check your Python version
python3 --version

# Use pyenv to manage Python versions
pyenv install 3.12.2
pyenv local 3.12.2
```

## Security Notes

- **Never commit credentials** to version control
- **Use environment variables** for production applications
- **Keep ngrok URLs private** - they provide access to your local machine
- **Tokens expire** - implement refresh token logic for production use

## File Structure

```
CSTradeAppSimpleDemo/
├── main.py              # Main OAuth application
├── README.md           # This file
├── oauth_server.py     # Optional OAuth server (if needed)
└── simple_oauth_server.py  # Simple server implementation
```

## Next Steps

For production applications, consider:
- Implementing token refresh logic
- Adding error handling and retry mechanisms
- Using environment variables for credentials
- Implementing proper logging
- Adding unit tests

## Support

For issues related to:
- **Schwab API**: Contact Schwab developer support
- **OAuth flow**: Check OAuth 2.0 documentation
- **ngrok**: Visit https://ngrok.com/docs
- **Python**: Check Python documentation at https://docs.python.org 