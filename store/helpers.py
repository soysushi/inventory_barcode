from barcode import EAN13
from barcode.writer import ImageWriter
from io import BytesIO

from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os
import PIL
import glob
import qrcode

import fitz
import json

from fitz import Rect
from django.core.files.base import ContentFile

def generate_label(barcode, product, names):
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
    # adding Sport information onto the label
    if (len(product.sport) > 14):
        font = ImageFont.truetype(font='static/assets/fonts/Zachery.otf', size=48)
    else:
        font = ImageFont.truetype(font='static/assets/fonts/Zachery.otf', size=60)
    draw = ImageDraw.Draw(im=back_im)
    text = product.sport
    draw.text(xy=(36,143), text=text, font=font, fill='#000000')
    # adding Product information onto the label
    if (len(product.name) > 34):
        n_font = ImageFont.truetype(font='static/assets/fonts/Zachery.otf', size=38)
    else:
        n_font = ImageFont.truetype(font='static/assets/fonts/Zachery.otf', size=48)
    draw = ImageDraw.Draw(im=back_im)
    text = product.name
    draw.text(xy=(36,201), text=text, font=n_font, fill='#000000')
    # adding the first 4 Product Variants onto the label
    variants = names[:5]
    spacing = 255
    for variant in variants:
        v_font = ImageFont.truetype(font='static/assets/fonts/Zachery.otf', size=38)
        draw.text(xy=(36,spacing), text=variant, font=v_font, fill='#000000') #290
        spacing += 45
    # generating QR CODE
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=0,
    )
    qr.add_data('https://www.champ-sys.ca/collections/cycling-jackets/products/custom-windguard-jacket')
    qr.make(fit=True)

    qr_test = qr.make_image(fill_color="black", back_color="white")
    qr_test.show()
    back_im.paste(qr_test,(488, 389))
    back_im.show()
    # saving the image to the model
    product.label.save(back_im_name, content=ContentFile(back_im_io.getvalue()), save=False)

    product.save()

    return
