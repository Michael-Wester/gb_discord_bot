from PIL import Image
import constants as c

def double_size(img):
    new_img = img.resize((img.size[0]*2, img.size[1]*2), Image.ANTIALIAS)
    return new_img

def make_gif(images, filepath):   
    frame_one = images[0]
    frame_one.save(filepath + "move.gif", format="GIF", append_images=images,
               save_all=True, duration=1000, loop=1)    
