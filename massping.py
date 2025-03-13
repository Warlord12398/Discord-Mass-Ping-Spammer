import requests
import random
import time

# Load tokens
with open("usertokens.txt", "r") as f:
    tokens = [line.strip() for line in f if line.strip()]

if not tokens:
    print("No tokens found in usertokens.txt!")
    exit()

# User inputs
channel_id = input("Enter the target channel ID: ")
message = input("Enter the spam message: ")
ping_count = int(input("How many users to ping per message? "))
repeat = 300  # Messages to send

headers = [{"Authorization": token} for token in tokens]

# Fetch server members (to get random users for pings)
def get_members(token):
    headers = {"Authorization": token}
    guild_id = input("Enter the server (guild) ID: ")
    response = requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/members?limit=1000", headers=headers)
    if response.status_code == 200:
        return [member["user"]["id"] for member in response.json()]
    else:
        print("Failed to fetch members! Status:", response.status_code)
        return []

# Choose a token to fetch members
random_token = random.choice(tokens)
members = get_members(random_token)
if not members:
    print("No members fetched!")
    exit()

# Spam messages
for i in range(repeat):
    token = random.choice(tokens)
    headers = {"Authorization": token}
    random_pings = " ".join([f"<@{random.choice(members)}>" for _ in range(ping_count)])
    data = {"content": f"{random_pings} {message}"}
    
    response = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", json=data, headers=headers)
    
    if response.status_code == 200:
        print(f"[{i+1}/{repeat}] Sent: {data['content']}")
    else:
        print(f"Failed to send message. Status: {response.status_code}, Response: {response.text}")
    
    time.sleep(1)  # Prevents hitting rate limits too fast
