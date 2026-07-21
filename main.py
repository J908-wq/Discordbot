import discord
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from dotenv import load_dotenv

load_dotenv()

# 1. Tiny web server for Render's free tier health check
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Handle the root URL "/" or a specific path like "/ping"
        if self.path in ["/", "/ping"]:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Alive")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        return  # Suppress logs to keep Render console clean

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    print(f"📡 Starting web server on port {port}...")
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

# 2. User Account Status Client
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Successfully authenticated account: {self.user}')
        
        # Explicit Custom Activity status
        activity = discord.Activity(
            type=discord.ActivityType.playing,
            name="Arch Linux",
            details="Running 24/7 in the cloud",
            state="Uptime: 100%"
        )
        await self.change_presence(activity=activity)

if __name__ == "__main__":
    # CRITICAL FIX: Start the web server FIRST so Render can bind to the port immediately
    threading.Thread(target=run_web_server, daemon=True).start()

    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("❌ ERROR: DISCORD_TOKEN is missing in environment variables!")
    else:
        # Initialize client with empty intents for user account automation
        client = MyClient(intents=discord.Intents.none())
        client.run(token)
