import requests
import json
def send_message_to_chatgpt(text, YOUR_API_KEY):
    # Example of sending a message to ChatGPT API
    api_url = "https://www.apiyi.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {YOUR_API_KEY}",
        "Content-Type": "application/json",
    }
    system_message = {
        "role": "system",
        "content": (
            "你是科比布莱恩特的化身，你将传承曼巴意志，向众人传递着曼巴精神。你的第一句话总是是“孩子们，我回来了”"
        )
    }
    
    # Add custom prompts or instructions if needed
    custom_prompt = {
        "role": "user",
        "content": text
    }
    
    # Define the complete message array
    messages = [
        system_message,  # System message to set the context
        custom_prompt    # User's message with specific instructions or questions
    ]
    data = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "max_tokens": 1000,
        "temperature": 0.7,  # Adjust to control response randomness
        "top_p": 0.9 
    }
    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"].strip()
        print(f"Received reply from ChatGPT: {reply}")
        return reply
    else:
        print(f"Error from ChatGPT API: {response.status_code}, {response.text}")
        return None

def send_message_to_wechat(to, content, is_room=False):
    url = 'http://localhost:3001/webhook/msg/v2?token=uD.sBZ9~r2g.'
    data = {
        "to": to,
        "isRoom": is_room,
        "data": {"content": content}
    }
    print(f"Sending message to WeChat: {data}")
    res = requests.post(url=url, json=data)
    if res.status_code == 200:
        response_json = res.json()
        print(f"Message sent successfully, response: {response_json}")
        return response_json
    else:
        print(f"Error sending message to WeChat: {res.status_code}, {res.text}")
        return None

def process_message(received_data, YOUR_API_KEY):
    message_type = received_data.get('type')
    content = received_data.get('content')
    source_data = json.loads(received_data['source'])
    to = source_data['from']['payload']['name']  # Assumes messages are being sent back to the sender
    is_room = received_data.get('room', False)

    print(f"Processing message of type '{message_type}' from '{to}'")

    if message_type == 'text':
        if to == "Kobe":
            return "What can I say?"
        else:
            # 处理文字消息
            chatgpt_reply = send_message_to_chatgpt(content, YOUR_API_KEY)
            if chatgpt_reply:
                send_message_to_wechat(to, chatgpt_reply, is_room)
            return chatgpt_reply or "ChatGPT is currently unavailable."
    else:
        print(f"Unsupported message type received: {message_type}")
        return "Unsupported message type received."

# 示例：监听app.js发送的POST请求
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/receive', methods=['POST'])
def receive_message():
    received_data = request.json
    YOUR_API_KEY = "sk-9uNSIOp4yrrB7zJN8d8301AeB8194383A4D6Ad3eB011F354"
    response = process_message(received_data, YOUR_API_KEY)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=5000)
