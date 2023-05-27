import requests
import json

import pandas as pd
from taipy.gui import Gui

API_KEY = "ADD YOUR API KEY HERE"
API_ENDPOINT = "https://api.openai.com/v1/chat/completions"


def generate_chat_completion(messages, model="gpt-4", temperature=1, max_tokens=None):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    if max_tokens is not None:
        data["max_tokens"] = max_tokens

    response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")


messages = [
    {"role": "system", "content": "I am a helpful assistant."},
]


def generate_chat_response(message, max_tokens=None):
    response = generate_chat_completion(messages, model="gpt-4", max_tokens=max_tokens)
    return response


def messages_to_text(messages):
    return pd.DataFrame(messages)


message = ""


def on_send_click(state):
    message = state.message
    state.messages.append({"role": "user", "content": message})
    state.messages = state.messages
    state.message = ""
    response = generate_chat_response(message)
    state.messages.append({"role": "system", "content": response})
    state.messages = state.messages


# Create the page
page = """
# Chat with GPT-4 App coded in 70 lines of Python
<|{messages_to_text(messages)}|table|show_all|>
<|{message}|input|label=Message|on_action=on_send_click|>
<|Send|button|on_action=on_send_click|>
"""

# Create the app
Gui(page).run(use_reloader=True)
