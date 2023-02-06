from PIL import Image
import server_properties_editor as p


def save_image(img, server_id):
    filepath = (
        "servers/"
        + str(server_id)
        + "/"
        + "images/"
        + str(server_id)
        + "_"
        + str(p.read_value(server_id, "turn_count"))
        + ".png"
    )
    new_img = img.resize((img.size[0] * 2, img.size[1] * 2), Image.ANTIALIAS)
    new_img.save(filepath, "PNG")
    return filepath


def save_image_frame(img, server_id):
    folderpath = "servers/" + str(server_id) + "/images/"
    filepath = (
        folderpath
        + str(server_id)
        + "_"
        + str(p.read_value(server_id, "turn_count"))
        + ".png"
    )
    new_img = img.resize((img.size[0] * 2, img.size[1] * 2), Image.ANTIALIAS)
    new_img.save(filepath, "PNG")
    return new_img


def make_gif(images, filepath, filename, server_id):
    bar_height = int(
        p.read_value(server_id, "progress_bar_height")
    )
    frame_one = images[0]
    frame_one_width = frame_one.size[0]
    frame_one_height = frame_one.size[1]
    if bar_height != 0:
        for i in range(len(images)):
            progress_bar = Image.new(
                "RGB",
                (int((i + 1) * frame_one_width / (len(images))), bar_height),
                (255, 0, 0),
            )
            images[i].paste(progress_bar, (0, 0))
    frame_one.save(
        filepath + filename,
        format="GIF",
        append_images=images,
        save_all=True,
        duration=900,
        loop=0,
    )
