import json
import time

import requests
import pandas as pd
from taipy.gui import Gui, notify

API_KEY = "ADD YOUR OPENAI API KEY HERE"
INITIAL_PROMPT = "I am a helpful assistant."

API_ENDPOINT = "https://api.openai.com/v1/chat/completions"


def generate_completion(messages, model="gpt-4", temperature=1):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "I'm sorry, GPT-4 is not available right now."


saved_messages = [
    {"role": "system", "content": INITIAL_PROMPT},
]

user_message = ""


def messages_to_data(messages):
    result = []
    for message in messages:
        result_message = {}
        result_message["Role"] = message["role"]
        result_message["Message"] = message["content"]
        if result_message["Role"] == "system":
            result_message["Role"] = "GPT-4"
        else:
            result_message["Role"] = "You"
        result.append(result_message)
    return pd.DataFrame(result)


def on_send_click(state):
    notify(state, "info", "Generating response...")
    message = state.user_message
    state.saved_messages.append({"role": "user", "content": message})
    state.saved_messages = state.saved_messages
    state.user_message = ""
    time.sleep(0.1)
    response = generate_completion(state.saved_messages)
    state.saved_messages.append({"role": "system", "content": response})
    state.saved_messages = state.saved_messages
    notify(state, "success", "GPT-4 generated a response!")


page = """
# Chat with **GPT-4**{: .color-primary}

<|{messages_to_data(saved_messages)}|table|show_all|width=100%|>

<br/>

<|{user_message}|input|multiline=True|lines_shown=2|label=Your Message|on_action=on_send_click|class_name=fullwidth|>

<|Send|button|on_action=on_send_click|>
"""

Gui(page).run()
