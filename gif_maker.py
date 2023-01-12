import os
from PIL import Image


def make_gif(folder, filepath):
    images = []
    for file in os.listdir(folder):
        if file.endswith(".png"):
            img = Image.open(folder + file)
            images.append(img)

    frame_one = images[0]
    frame_one_width = frame_one.size[0]
    for i in range(len(images)):
        progress_bar = Image.new(
            "RGB", (int((i + 1) * frame_one_width / (len(images))), 10), "yellow"
        )
        images[i].paste(progress_bar, (0, 0))
    frame_one.save(
        filepath + "games.gif",
        format="GIF",
        append_images=images,
        save_all=True,
        duration=1000,
        loop=0,
    )


make_gif("boxart/", "boxart/")
