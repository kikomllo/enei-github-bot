from fastapi import FastAPI, Request
import httpx

app = FastAPI()

# Replace with your actual webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1550512590864523364/tkY3diyOX17fY5T5brPIBTKnPoub0KGEIRpTcvgV0k7PyFUdX9NbVSFBO6JmbIqOlPti"

@app.post("/webhooks/github")
async def github_listener(request: Request):
    payload = await request.json()
    
    # Anti-Spam: Only trigger when a PR is strictly 'opened'
    if payload.get("action") != "opened":
        return {"status": "Ignored. Not a new PR."}
        
    # Extract PR details safely
    pr = payload.get("pull_request", {})
    title = pr.get("title", "No Title")
    author = pr.get("user", {}).get("login", "Unknown User")
    pr_url = pr.get("html_url", "")
    
    # Format the Discord message (Using @here to ping the tech team)
    discord_message = {
        "content": f"@here **New Pull Request!**\n**{author}** wants to merge: *{title}*\n🔗 {pr_url}"
    }
    
    # Send the HTTP POST request to Discord
    async with httpx.AsyncClient() as client:
        response = await client.post(DISCORD_WEBHOOK_URL, json=discord_message)
        
    return {"status": "Success", "discord_status": response.status_code}