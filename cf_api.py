import base64
import json
import re
import time
from datetime import datetime, timedelta
from pathlib import Path

from requests import Session

from env_values import CF_ACCOUNT_ID, CF_API_KEY, SAVE_RESPONSE

API_BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run"
headers = {"Authorization": f"Bearer {CF_API_KEY}"}

data_path = Path("iotd")
s = Session()
s.headers = headers


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


def get_text(model: str, sys_prompt: str, user_prompt: str) -> str:
    payload = {
        "messages": [{"role": "system", "content": sys_prompt}, {"role": "user", "content": user_prompt}],
        "temperature": 0.8,
    }
    return api_response(model, payload)["response"]


def save_image(img_data):
    output_file = data_path / f"{TOMORROW}.png"
    output_file.parent.mkdir(exist_ok=True)  # creates parent dir if not present

    with open(output_file, "wb") as file:
        file.write(img_data)
    print(f"Image saved as {output_file}")


def save_details():
    data_file = data_path / "data.json"
    with open(data_file, "r") as f:
        data = json.load(f) or {}
    data[TOMORROW] = {
        "title": dream["imageTitle"],
        "description": dream["imageDescription"],
        "randomDrug": dream["randomDrug"],
        "randomTopic": dream["randomTopic"],
    }
    with open(data_file, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)


def generate_image(prompt):
    payload = {"prompt": prompt, "num_steps": 5}
    base64_string = api_response("black-forest-labs/flux-1-schnell", payload=payload)["image"]
    image_data = base64.b64decode(base64_string)
    save_image(image_data)
    save_details()


def extract_json(answer: str) -> json:
    a = answer.find("```")
    b = answer.find("```", a + 5)
    json_text = answer[a + 3 : b].strip().lstrip("json")
    try:
        _json = json.loads(json_text)
    except json.JSONDecodeError as e:
        error = e.args[0]
        print(error)
        json_text = re.sub(r"\s+", " ", json_text)
        json_text = re.sub(r"'(\w+)':", r'"\1":', json_text)

        _json = json.loads(json_text)
    return _json


def remove_quotes(x: str) -> str:
    return re.sub(r"[\"']", "", x)


def hallucinator() -> json:
    model = "meta/llama-3.1-8b-instruct"
    drug_n_topic = get_text(
        model,
        sys_prompt="You are a helpful assistant with knowledge of various random and interesting fields",
        user_prompt="just name 1 random Hallucinogen and 1 unrelated topic in a csv format with only name",
    )
    drug, topic = remove_quotes(drug_n_topic).split(",", 1)
    print(f"{drug=} | {topic=}")
    output_pattern = {"imageDescription": "", "imageTitle": "", "randomDrug": "", "randomTopic": ""}
    output = get_text(
        model,
        sys_prompt="You are a drug researcher who is a creative and imaginative artist too.",
        user_prompt=f"Describe an image about {topic} as described by some person under the influence {drug}. "
        f"this is part of json file added to your research. json format should be {output_pattern},"
        f" imageTitle should be description summary in less than 10 words",
    )
    return extract_json(output)


if __name__ == "__main__":
    TOMORROW = (datetime.now() + timedelta(1)).strftime("%Y-%m/%d")

    dream = hallucinator()
    print(dream)
    generate_image(prompt=dream["imageDescription"])
    print("end..")
    s.close()
