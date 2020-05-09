from PIL import Image  

def resize_image(file):
    im = Image.open(file)
    newsize = (300, 300) 
    im = im.resize(newsize)
    return im