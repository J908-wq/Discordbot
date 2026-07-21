import discord
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from dotenv import load_dotenv

load_dotenv()

# 1. Tiny web server for Render's free tier health check
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

    # Silences logs in the console to keep output clean
    def log_message(self, format, *args):
        return

def run_web_server():
    # Render binds to 0.0.0.0. Using 10000 as a fallback if PORT isn't set.
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    print(f"Web server running on port {port}")
    server.serve_forever()

# 2. Your actual Discord 24/7 Status code
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')
        
        # Defining the rich presence activity
        activity = discord.Activity(
            type=discord.ActivityType.playing,
            name="Arch Linux",
            details="Running 24/7 in the cloud",
            state="Uptime: 100%"
        )
        await self.change_presence(activity=activity)

# Start the web server in a separate thread so it doesn't block Discord
threading.Thread(target=run_web_server, daemon=True).start()

# Start Discord with the required Presence Intent enabled
intents = discord.Intents.default()
intents.presences = True  # Required to update or change presence status

client = MyClient(intents=intents)
# Fetch the token from environment variables
token = os.getenv("DISCORD_TOKEN")

# Verify the token exists before passing it to discord.py
if not token:
    print("❌ ERROR: DISCORD_TOKEN environment variable is missing or empty on Render!")
elif len(token) < 50:
    print(f"❌ ERROR: The token found seems too short ({len(token)} chars). Check for typos.")
else:
    # Start Discord safely
    client = MyClient(intents=intents)
    client.run(token)

