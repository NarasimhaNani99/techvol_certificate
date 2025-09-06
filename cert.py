# importing packages & modules
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os
import qrcode
import base64

# def generate_qr_code(data, file_name, qr_size=(200, 200)):
#     # Generate QR code
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=10,
#         border=4,
#     )
#     qr.add_data(data)
#     qr.make(fit=True)

#     qr_img = qr.make_image(fill_color="black", back_color="white")
    
#     # Resize QR code to fixed size
#     qr_img = qr_img.resize(qr_size, Image.LANCZOS)

#     img = Image.open(file_name)
#     # Paste QR code on the certificate
#     img.paste(qr_img, (189, 1566))
#     img.save(file_name)

# String Encode 
def str_enc(string):
    # Encode the string using Base64
    encoded_bytes = base64.b64encode(str(string).encode("utf-8"))
    # Convert bytes to a string for display (optional)
    encoded_string = encoded_bytes.decode("utf-8")
    return encoded_string

# Implementation to generate certificate
df = pd.read_csv('data.csv')
font_path = "GreatVibes-Regular.ttf"

font_path2 ="OpenSans-Regular.ttf"

font = ImageFont.truetype(font_path, 200)
font_small = ImageFont.truetype(font_path2, 60)  # Smaller font for dates

# Static duration dates
static_start_date = "09-12-2024"
static_end_date = "10-03-2025"

for index, j in df.iterrows():
    img = Image.open('template.png')
    width = 3508
    draw = ImageDraw.Draw(img)
    
    # Draw name
    text = format(j['name'])
    text_width = draw.textlength(text, font=font)
    x_text = (width - text_width) // 2
    draw.text(xy=(x_text, 1050), text=text, fill=("#1F2B5B"), font=font)

    # Draw static duration dates
    start_date_text = f"{static_start_date}"
    end_date_text = f"{static_end_date}"
    
    # Adjust positions for dates
    start_date_position = (width // 1.93, 1560)  # Centered horizontally, adjust vertically
    end_date_position = (width // 1.53, 1560)

    # 1574 for aws and fsd 1560

    draw.text(start_date_position, start_date_text, fill=("#1F2B5B"), font=font_small, anchor="mm")
    draw.text(end_date_position, end_date_text, fill=("#1F2B5B"), font=font_small, anchor="mm")

    # Save certificate with name
    img.save(f'output/{j["name"]}.png')
    
    # Generate QR code
    # userID = str_enc(j['id'])
    # data_to_encode = f"https://certify.criativo.ai/?userID={userID}"
    # generate_qr_code(data_to_encode, f'output/{j["name"]}.png', qr_size=(370, 370))


    
