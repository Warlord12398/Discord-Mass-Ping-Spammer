import requests
import time
import random
import threading

# Load tokens from file
with open("usertokens.txt", "r") as f:
    tokens = [line.strip() for line in f if line.strip()]

if not tokens:
    print("No tokens found in usertokens.txt")
    exit()

# User input
channel_id = input("Enter the Channel ID to spam: ")
message = input("Enter the message to spam: ")
ping_count = int(input("How many users to ping per message? "))

def get_random_users(channel_id, token):
    headers = {"Authorization": token}
    response = requests.get(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=headers)
    
    if response.status_code == 200:
        users = set()
        messages = response.json()
        for msg in messages:
            if "author" in msg:
                users.add(msg["author"]["id"])
        return list(users)
    else:
        return []

def send_spam(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    
    users = get_random_users(channel_id, token)
    if not users:
        print("Failed to fetch users. Using default mentions.")
        users = ["@everyone"]

    for _ in range(300):  # Spam 300 messages
        random.shuffle(users)
        mentions = " ".join([f"<@{user}>" for user in users[:ping_count]])
        final_message = f"{mentions} {message}"
        
        # Simulate typing
        typing_url = f"https://discord.com/api/v9/channels/{channel_id}/typing"
        requests.post(typing_url, headers=headers)
        time.sleep(random.uniform(2, 4))  # Random delay for typing effect
        
        # Send message
        json_data = {"content": final_message}
        response = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=headers, json=json_data)
        
        if response.status_code == 200:
            print(f"Message sent: {final_message}")
        elif response.status_code == 429:
            retry_after = response.json().get("retry_after", 5)
            print(f"Rate limited! Retrying after {retry_after} seconds...")
            time.sleep(retry_after)
        else:
            print(f"Failed to send message: {response.text}")
        
        time.sleep(random.uniform(3, 6))  # Random delay between messages

# Start spam threads
threads = []
for token in tokens:
    thread = threading.Thread(target=send_spam, args=(token,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
