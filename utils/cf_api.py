import base64
import json
import re
import time

from requests import Session

from utils.constants import CF_ACCOUNT_ID, CF_API_KEY, SAVE_RESPONSE

API_BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run"
headers = {"Authorization": f"Bearer {CF_API_KEY}"}

s = Session()
s.headers = headers


def close_session():
    s.close()


def api_response(model, payload):
    start = time.perf_counter()
    response = s.post(f"{API_BASE_URL}/@cf/{model}", json=payload, timeout=200)
    x = response.json()
    print("api call time", time.perf_counter() - start)
    if SAVE_RESPONSE:
        with open("resp.json", "w") as f:
            json.dump(x, f)
    if x["success"]:
        return x["result"]

    print(response.status_code, x)
    raise IOError


def get_text(model: str, sys_prompt: str, user_prompt: str, json_schema: dict = None) -> str | dict:
    if json_schema:
        sys_prompt += " Only reply as single valid json"
    payload = {
        "messages": [{"role": "system", "content": sys_prompt}, {"role": "user", "content": user_prompt}],
        "temperature": 0.75,
    }
    if json_schema:
        # payload["messages"].append({"role": "assistant", "content": "{"})
        payload["response_format"] = {"type": "json_schema", "json_schema": json_schema}  # noqa
    return api_response(model, payload)["response"]


def generate_image(prompt):
    payload = {"prompt": prompt, "num_steps": 5}
    base64_string = api_response("black-forest-labs/flux-1-schnell", payload=payload)["image"]
    image_data = base64.b64decode(base64_string)
    return image_data


def extract_json(answer: str) -> json:
    if "```" in answer:
        a = answer.find("```")
        b = answer.find("```", a + 5)
        json_text = answer[a + 3: b].strip().lstrip("json").strip()
    else:
        print("no code block in answer")
        json_text = answer
    if "{" in json_text and "}" not in json_text:
        json_text += "}"
    try:
        _json = json.loads(json_text)
    except json.JSONDecodeError as e:
        print("error1", e.doc, e.pos, "\n", e.msg)
        json_text = re.sub(r"\s+", " ", json_text)
        json_text = re.sub(r"'(\w+)':", r'"\1":', json_text)

        try:
            _json = json.loads(json_text)
        except json.JSONDecodeError as e:
            print("error2", e.doc, e.pos, "\n", e.msg)
            raise
    return _json


def remove_quotes(x: str) -> str:
    return re.sub(r"[\"']", "", x)
