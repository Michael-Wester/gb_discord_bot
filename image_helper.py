from PIL import Image
import server_properties_editor as properties


def get_server_folder(server_id):
    return "servers/" + str(server_id) + "/"

def save_image(img, server_id):
    
    filepath = "servers/" + str(server_id) + "/" + "images/" + str(server_id) + "_" + str(properties.read_server_property_value(server_id, "turn_count")) + ".png"
    new_img = img.resize((img.size[0]*2, img.size[1]*2), Image.ANTIALIAS)
    new_img.save(filepath, "PNG")
    return filepath

def save_image_frame(img, server_id):
    filepath = "servers/" + str(server_id) + "/" + "images/" + str(server_id) + "_" + str(properties.read_server_property_value(server_id, "turn_count")) + ".png"
    new_img = img.resize((img.size[0]*2, img.size[1]*2), Image.ANTIALIAS)
    new_img.save(filepath, "PNG")
    return new_img


def make_gif(images, filepath, filename):   
    frame_one = images[0]
    frame_one.save(filepath + filename, format="GIF", append_images=images,
               save_all=True, duration=1000, loop=1)    
