import json
from websocket import create_connection, WebSocketConnectionClosedException
from curl_cffi import requests
# @hprideh / https://discord.gg/8P6ysxAq
infv = input("invite link: ")
fingerheaders = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.8',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Brave";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
}


def get_session_id(token):
    ws = create_connection("wss://gateway.discord.gg/?encoding=json&v=9")
    
    payload = {
        "op": 2,
        "d": {
            "token": token,
            "capabilities": 61,
            "properties": {
                "$os": "windows",
                "$browser": "my_library",
                "$device": "my_library"
            },
            "presence": {
                "status": "online",
                "since": 0,
                "activities": [],
                "afk": False,
            },
            "compress": False,
            "client_state": {}
        }
    }
    ws.send(json.dumps(payload))
    
    ws.send(json.dumps({
        "op": 4,
        "d": {
            "guild_id": None,
            "channel_id": None,
            "self_mute": False,
            "self_deaf": False,
            "self_video": False,
            "flags": 2,
        }
    }))
    
    session_id = None
    while True:
        try:
            response = json.loads(ws.recv())
        except WebSocketConnectionClosedException:
            print("Connection closed.")
            break

        if response.get("op") == 9:
            print("Invalid token.")
            break

        if response.get("t") == "READY":
            session_id = response["d"]["session_id"]
            break

    ws.close()
    return session_id

if __name__ == "__main__":
    token = input("Enter your token: ")
    session = get_session_id(token)
    if session:
        print("Session ID:", session)
        finger_response = requests.get('https://discord.com/api/v10/experiments', headers=fingerheaders)
        fingerprint = finger_response.json()['fingerprint']

        vcookie = f"locale=en; __dcfduid={finger_response.cookies.get('__dcfduid')}; __sdcfduid={finger_response.cookies.get('__sdcfduid')}; __cfruid={finger_response.cookies.get('__cfruid')}"
        json_data = {
            'session_id': session,
        }
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.8',
            'authorization': token,
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Brave";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'cookie': vcookie,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en-US',
            'x-discord-timezone': 'America/Los_Angeles',
            'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiaGFzX2NsaWVudF9tb2RzIjpmYWxzZSwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEzMy4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTMzLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiJodHRwczovL3NlYXJjaC5icmF2ZS5jb20vIiwicmVmZXJyaW5nX2RvbWFpbiI6InNlYXJjaC5icmF2ZS5jb20iLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MzcwNTMzLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
            'fingerprint': fingerprint
        }
        response = requests.post(f'https://discord.com/api/v9/invites/{infv}', headers=headers, json=json_data)
        print(response.text)
        
    else:
        print("Failed to get Session ID.")
