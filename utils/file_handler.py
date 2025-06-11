import json
from io import BytesIO

from PIL import Image
from pydantic import BaseModel

from utils.constants import DATA_PATH


class ImageDetails(BaseModel):
    description: str = ""
    style: str = ""
    title: str = ""
    topic: str = ""

    def to_dict(self):
        return vars(self)

    def to_json_str(self):
        return json.dumps(self.to_dict())


def save_image(filename: str, content: bytes) -> None:
    """Save an image to the data directory."""

    output_file = DATA_PATH / f"{filename}.webp"
    output_file.parent.mkdir(exist_ok=True)  # creates parent dir if not present

    Image.open(BytesIO(content)).save(output_file, "webp")
    print(f"Image saved as {output_file}")


def save_details(image_key: str, image_details: ImageDetails):
    """Save image details to the data.json file."""

    data_file = DATA_PATH / "data.json"
    with open(data_file, "r") as f:
        data = json.load(f) or {}

    data[image_key] = vars(image_details)
    with open(data_file, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")  # linter checks for trailing newlines


def save_response_dev(x):
    """Save response to the resp.json file in debug mode."""
    with open("resp.json", "w") as f:
        json.dump(x, f)
