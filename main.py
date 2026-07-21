import discord
import os
import asyncio
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from dotenv import load_dotenv

load_dotenv()

# 1. Tiny web server to trick Render's free tier health check
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_web_server():
    # Render automatically tells the app what port to use via an env variable
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    print(f"Web server running on port {port}")
    server.serve_forever()

# 2. Your actual Discord 24/7 Status code
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')
        activity = discord.Activity(
            type=discord.ActivityType.playing,
            name="Arch Linux",
            details="Running 24/7 in the cloud",
            state="Uptime: 100%"
        )
        await self.change_presence(activity=activity)

# Start the web server in a separate thread so it doesn't block Discord
threading.Thread(target=run_web_server, daemon=True).start()

# Start Discord
client = MyClient(intents=discord.Intents.default())
client.run(os.getenv("DISCORD_TOKEN"))
