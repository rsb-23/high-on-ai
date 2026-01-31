from PIL import Image


# convert png file to webp
def convert(png_file):
    img = Image.open(png_file)
    img.save(png_file[:-4] + ".webp", "webp")


if __name__ == "__main__":
    convert("iotd/defau_lt.png")
