import requests
from typing import Dict

class Input:
    def __init__(self, to: str, content: str, isRoom: bool):
        self.to = to
        self.content = content
        self.isRoom = isRoom

class Args:
    def __init__(self, input_data: Input):
        self.input = input_data

def handler(args: Args) -> Dict:
    to = args.input.to
    content = args.input.content
    isRoom = args.input.isRoom
    url = 'http://localhost:3001/webhook/msg/v2?token=uD.sBZ9~r2g.'

    data = {
        "to": to,
        "isRoom": isRoom,
        "data": {"content": content}
    }

    res = requests.post(url=url, json=data)

    return res.json()

# Example usage:
input_data = Input(to="微信团队", content="Hello, World!", isRoom=False)
args = Args(input_data=input_data)
response_json = handler(args=args)
print(response_json)
