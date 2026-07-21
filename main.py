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
        self.wfile.write(b"Alive")

    def log_message(self, format, *args):
        return

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

# 2. User Account Status Client
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Successfully authenticated account: {self.user}')
        
        # User presence structures use CustomActivity or explicit Activity objects
        activity = discord.Activity(
            type=discord.ActivityType.playing,
            name="Arch Linux",
            details="Running 24/7 in the cloud",
            state="Uptime: 100%"
        )
        await self.change_presence(activity=activity)

# Start background web server
threading.Thread(target=run_web_server, daemon=True).start()

# Initialize the client without intents (required for user automation)
token = os.getenv("DISCORD_TOKEN")

if not token:
    print("❌ ERROR: DISCORD_TOKEN is missing on Render settings!")
else:
    client = MyClient()
    # User tokens are initialized directly without prefixes via the self fork
    client.run(token)
s