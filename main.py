import discord
import os
import asyncio
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
client = discord.Client(intents=discord.Intents.none())

# This matches the endpoint cron-job.org will look for
@app.get("/")
@app.get("/ping")
def health_check():
    print("⏰ Cron-job.org ping received! Keeping the bot alive...")
    return {"status": "Alive and running"}

@client.event
async def on_ready():
    print(f'🤖 Successfully authenticated account: {client.user}')
    activity = discord.Activity(
        type=discord.ActivityType.playing,
        name="Arch Linux",
        details="Running 24/7 in the cloud",
        state="Uptime: 100%"
    )
    await client.change_presence(activity=activity)

async def main():
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("❌ ERROR: DISCORD_TOKEN is missing!")
        return

    port = int(os.environ.get("PORT", 10000))
    config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="warning")
    server = uvicorn.Server(config)
    
    # Run both the web server and the Discord client concurrently
    await asyncio.gather(
        server.serve(),
        client.start(token)
    )

if __name__ == "__main__":
    asyncio.run(main())
