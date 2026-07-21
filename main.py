import discord
import os
import asyncio
import uvicorn
from fastapi import FastAPI, Header, HTTPException
from dotenv import load_dotenv

load_dotenv()

# Initialize FastAPI and Discord Client
app = FastAPI()
client = discord.Client(intents=discord.Intents.none())

# Secure your endpoint with a secret token
CRON_SECRET = os.getenv("CRON_SECRET", "super-secret-key")

@app.get("/")
def health_check():
    return {"status": "Alive"}

@app.get("/trigger-task")
async def trigger_task(authorization: str = Header(None)):
    # 1. Security Check
    if not authorization or authorization != f"Bearer {CRON_SECRET}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # 2. Trigger your Discord logic safely inside the async loop
    if client.is_ready():
        # Example task: Update presence or send a message
        print("⏰ Cron-job.org triggered the task!")
        
        activity = discord.Activity(
            type=discord.ActivityType.playing,
            name="Arch Linux",
            details="Triggered by Cron Job",
            state="Status: Active"
        )
        asyncio.create_task(client.change_presence(activity=activity))
        return {"status": "Task executed successfully"}
    
    return {"status": "Bot not ready yet"}

@client.event
async def on_ready():
    print(f'Successfully authenticated account: {self.user}')

# Start both FastAPI and Discord simultaneously inside the same event loop
async def main():
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("❌ ERROR: DISCORD_TOKEN is missing!")
        return

    port = int(os.environ.get("PORT", 10000))
    
    # Run Uvicorn config without block
    config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="warning")
    server = uvicorn.Server(config)
    
    # Run both tasks concurrently
    await asyncio.gather(
        server.serve(),
        client.start(token)
    )

if __name__ == "__main__":
    asyncio.run(main())
