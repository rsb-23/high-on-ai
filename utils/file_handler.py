import json
from dataclasses import dataclass

from utils.constants import DATA_PATH


@dataclass
class ImageDetails:
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

    output_file = DATA_PATH / f"{filename}.png"
    output_file.parent.mkdir(exist_ok=True)  # creates parent dir if not present

    with open(output_file, "wb") as file:
        file.write(content)
    print(f"Image saved as {output_file}")


def save_details(image_key: str, image_details: ImageDetails):
    """Save image details to the data.json file."""

    data_file = DATA_PATH / "data.json"
    with open(data_file, "r") as f:
        data = json.load(f) or {}

    data[image_key] = vars(image_details)
    with open(data_file, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)
