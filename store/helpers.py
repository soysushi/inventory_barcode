from barcode import EAN13
from barcode.writer import ImageWriter
from io import BytesIO

from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os
import PIL
import glob


import fitz
import json

from fitz import Rect
from django.core.files.base import ContentFile

def generate_label(barcode, product):
    # create a png file

# file that has all the item variants
    original_image = EAN13(str(barcode), writer=ImageWriter())
    i = original_image.render()
    fixed_height = 150
    file = (str(barcode)+'.png')
    height_percent = (fixed_height / float(i.size[1]))
    width_size = int((float(i.size[0]) * float(height_percent)))
    image = i.resize((width_size * 2, fixed_height),
            PIL.Image.NEAREST)
    # here turning PILLOW IMG file into BytesIO
    image_io = BytesIO()
    image.save(image_io, format='PNG')
    image_name = str(barcode)+'.png'
    # preparing barcode to paste to template
    img_main = Image.open('static/images/Cycling_Template.png')
    position = (int((img_main.width - image.width)/2),
    (img_main.height - image.height))
    back_im = img_main.copy()
    back_im.paste(image, position)
    # back_im.save(file, quality=100)
    back_im_io = BytesIO()
    back_im.save(back_im_io, format='PNG')
    back_im_name = str(barcode)+'.png'
    # adding Product information onto the label
    font = ImageFont.truetype(font='static/assets/fonts/Zachery.otf', size=12)
    print(font)
    print("HELLO FROM INSIDE")
    product.label.save(back_im_name, content=ContentFile(back_im_io.getvalue()), save=False)

    product.save()

    return
