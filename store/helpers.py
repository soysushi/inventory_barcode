from barcode import EAN13
from barcode.writer import ImageWriter
from io import BytesIO

from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os
import PIL
import glob
import qrcode
import os

import fitz
import json

from fitz import Rect
from django.core.files.base import ContentFile

from .models import Product

import cv2
from pyzbar import pyzbar

# 2000000000000 is the barcode
# 100000000000 is the drop code
def generate_label(barcode, product, names, link):
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
    #image_io = BytesIO()
    #image.save(image_io, format='PNG')
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
    qr.add_data(link)
    qr.make(fit=True)
    s_font = ImageFont.truetype(font='static/assets/fonts/Zachery.otf', size=32)
    draw.text(xy=(528,314), text="info", font=s_font, fill='#000000')
    qr_test = qr.make_image(fill_color="black", back_color="white")
    back_im.paste(qr_test,(488, 349))
    back_im_io = BytesIO()
    back_im.save(back_im_io, format='PNG')
    # saving the image to the model
    product.label.save(back_im_name, content=ContentFile(back_im_io.getvalue()), save=False)
    product.save()
    return

def print_label(items):
    x = 0
    counter = 0
    # use the barcode to get the products

    for item in items:
        product = Product.objects.get(sortno=item)
        input_file = 'static/images/AveryPresta94104SquareLabels.pdf'
        label_limit = 9
        # setting unique file name
        file_name = 'product_labels'
        # open up tag
        # retrieve the first page of the PDF
        file_handle = fitz.open(input_file)
        first_page = file_handle[0]
        # add the image
        # first image location 1
        if counter == 0:
            tag_file = str(product.label)
            image_rectangle = Rect(27,72,206,251)
            first_page.insertImage(image_rectangle, filename=tag_file)
            output_file = str(file_name + str(x) + '.pdf')
            file_handle.save(output_file)

        # second+ image locations
        if counter != 0 and counter < 9:
            tag_file = str(product.label)
            input_file = str(file_name + str(x) + '.pdf')
            file_handle = fitz.open(input_file)
            first_page = file_handle[0]
            if counter == 1:
                image_rectangle = Rect(215,72,395,251)
            if counter == 2:
                image_rectangle = Rect(405,72,585,251)
            if counter == 3:
                image_rectangle = Rect(27,306,206,485)
            if counter == 4:
                image_rectangle = Rect(215,306,395,485)
            if counter == 5:
                image_rectangle = Rect(405,306,585,485)
            if counter == 6:
                image_rectangle = Rect(27,540,206,720)
            if counter == 7:
                image_rectangle = Rect(215,540,395,720)
            if counter == 8:
                image_rectangle = Rect(405,540,585,720)
            first_page.insertImage(image_rectangle, filename=tag_file)
            output_file = str(file_name + str(x) + '.pdf')
            file_handle.saveIncr()
            os.system("open " + output_file)


        # third image location 3
        if counter == 9:
            x += 1
            counter = 0
            tag_file = str(product.label)
            image_rectangle = Rect(27,72,206,251)
            first_page.insertImage(image_rectangle, filename=tag_file)
            output_file = str(file_name + str(x) + '.pdf')
            file_handle.save(output_file)
            os.system("open " + output_file)

        counter += 1
    return

def generate_dropcode(dropcode, drop):
    # create a png file using the new dropcode
    print(dropcode)
    original_image = EAN13(str(dropcode), writer=ImageWriter())
    i = original_image.render()
    fixed_height = 150
    file = (str(dropcode)+'.png')
    height_percent = (fixed_height / float(i.size[1]))
    width_size = int((float(i.size[0]) * float(height_percent)))
    image = i.resize((width_size * 2, fixed_height),
            PIL.Image.NEAREST)
    image.show()
    # here turning PILLOW IMG file into BytesIO
    #image_io = BytesIO()
    #image.save(image_io, format='PNG')
    image_name = str(dropcode)+'.png'
    # preparing barcode to paste to template
    img_main = Image.open('static/images/Cycling_Template.png')
    position = (int((img_main.width - image.width)/2),
    (img_main.height - image.height))
    back_im = img_main.copy()
    back_im.paste(image, position)
    # Drawing text
    font = ImageFont.truetype(font='static/assets/fonts/Zachery.otf', size=140)
    draw = ImageDraw.Draw(im=back_im)
    text = drop.name
    draw.text(xy=(310,305), text=text, font=font, fill='#000000')
    # back_im.save(file, quality=100)
    back_im_io = BytesIO()
    back_im.save(back_im_io, format='PNG')
    back_im_name = str(dropcode)+'.png'
    # Save
    drop.label.save(back_im_name, content=ContentFile(back_im_io.getvalue()), save=False)
    drop.save()

def read_barcodes(frame):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y , w, h = barcode.rect
        #1
        barcode_info = barcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)

        #2
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)
        #3
        with open("barcode_result.txt", mode ='w') as file:
            file.write("Recognized Barcode:" + barcode_info)
    return frame
