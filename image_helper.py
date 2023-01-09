from PIL import Image
import server_properties_editor as properties


def get_server_folder(server_id):
    return "servers/" + str(server_id) + "/"

def save_image(img, server_id):
    
    filepath = "servers/" + str(server_id) + "/" + "images/" + str(server_id) + "_" + str(properties.get_turn_count(server_id)) + ".png"
    new_img = img.resize((img.size[0]*2, img.size[1]*2), Image.ANTIALIAS)
    new_img.save(filepath, "PNG")
    return filepath

def save_image_frame(img, server_id):
    filepath = "servers/" + str(server_id) + "/" + "images/" + str(server_id) + "_" + str(properties.get_turn_count(server_id)) + ".png"
    new_img = img.resize((img.size[0]*2, img.size[1]*2), Image.ANTIALIAS)
    new_img.save(filepath, "PNG")
    return new_img


def make_gif(images, filepath):   
    frame_one = images[0]
    frame_one.save(filepath + "move.gif", format="GIF", append_images=images,
               save_all=True, duration=1000, loop=1)    
