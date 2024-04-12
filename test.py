import subprocess

# Add your Ngrok auth token
ngrok_auth_token = ""

# Specify the full path to the Ngrok executable
ngrok_path = r"C:\Users\Debarghya Kundu\Desktop\dream project\video calling applications\ngrok.exe"

# Start Ngrok tunnel
ngrok_process = subprocess.Popen([ngrok_path, 'authtoken', ngrok_auth_token])
ngrok_process.wait()  # Wait for the authentication to complete
ngrok_process = subprocess.Popen([ngrok_path, 'http', '5500'])
