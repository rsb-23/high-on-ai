import json
import time
from datetime import datetime, timedelta

from utils.cf_api import close_session, generate_image, get_text, remove_quotes
from utils.file_handler import ImageDetails, save_details, save_image

TOMORROW = (datetime.now() + timedelta(1)).strftime("%Y-%m/%d")


def hallucinator() -> ImageDetails:
    model = "meta/llama-3.1-8b-instruct"
    drug_n_topic, retries = "", 5
    while not drug_n_topic and retries:
        drug_n_topic = get_text(
            model,
            sys_prompt="You are a helpful assistant with knowledge of various random and interesting fields",
            user_prompt="just name 1 random Hallucinogen and 1 unrelated pokemon in a csv format with only name",
        )
        time.sleep(0.8 * retries)
        retries -= 1
    print(f"{drug_n_topic=}")
    drug, topic = remove_quotes(drug_n_topic).split(",", 1)
    # output_json = ImageDetails(style=drug)
    output = get_text(
        model,
        sys_prompt="You are a drug researcher who is a creative and imaginative artist too.",
        user_prompt=f"Describe an image about {topic} as described by some person under the influence {drug}. "
        # f"json format should be {output_json.to_json_str()},"
        f" imageTitle should be description summary in less than 10 words",
        json_schema=ImageDetails.model_json_schema(),
    )
    # return extract_json(output)
    try:
        return ImageDetails(**output)
    # TODO: extract_json can be removed if json mode doesn't fail
    except json.JSONDecodeError as e:
        print(f"JSON mode failed for - {e.msg}")
        print(output)
        raise json.JSONDecodeError


def artist() -> ImageDetails:
    model = "meta/llama-3.1-8b-instruct"
    style_n_topic = get_text(
        model,
        sys_prompt="You are a helpful assistant with knowledge of various art techniques and all special days",
        user_prompt=f"just name 1 random art technique and what's special about date {TOMORROW} in a csv "
        "format with only name",
    )
    print(f"{style_n_topic=}")
    style, topic = remove_quotes(style_n_topic).split(",", 1)
    output = get_text(
        model,
        sys_prompt="You are a famous artist who has great imagination and knows intricacies of all styles.",
        user_prompt=f"Describe an image about {topic} drawn in {style} style."
        f" summarize a long description in less than 6 words for 'title'",
        json_schema=ImageDetails.model_json_schema(),
    )
    return ImageDetails(**output)


def gen_and_save_image(prompt, image_details: ImageDetails):
    image_data = generate_image(prompt)
    save_image(filename=TOMORROW, content=image_data)
    save_details(image_key=TOMORROW, image_details=image_details)


if __name__ == "__main__":
    imagination = artist()
    print(f"topic={imagination.topic}, style={imagination.style}, title={imagination.title}")
    print(imagination.description)
    gen_and_save_image(prompt=imagination.description, image_details=imagination)

    print("end..")
    close_session()
