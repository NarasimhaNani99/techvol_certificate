from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

# Load CSV
df = pd.read_csv("data.csv")

# Fonts
font_regular = ImageFont.truetype("arial.ttf", 48)
font_bold = ImageFont.truetype("arialbd.ttf", 52)

# Output folder
os.makedirs("output", exist_ok=True)

def draw_paragraph(draw, segments, x_margin, y_start, max_width, line_height):
    """Draw paragraph with inline bold/regular fonts and wrapping."""
    y = y_start
    x = x_margin
    line = []

    words = []
    for text, style in segments:
        font = font_bold if style == "bold" else font_regular
        for w in text.split(" "):
            words.append((w + " ", font))

    for word, font in words:
        word_width = draw.textlength(word, font=font)

        if x + word_width > max_width:  # wrap
            x_cursor = x_margin
            for part, f in line:
                draw.text((x_cursor, y), part, font=f, fill="#000000")
                x_cursor += draw.textlength(part, font=f)
            y += line_height
            x = x_margin
            line = []

        line.append((word, font))
        x += word_width

    if line:  # last line
        x_cursor = x_margin
        for part, f in line:
            draw.text((x_cursor, y), part, font=f, fill="#000000")
            x_cursor += draw.textlength(part, font=f)

    return y + line_height


for _, row in df.iterrows():
    img = Image.open("template.png").convert("RGB")
    width, height = img.size
    draw = ImageDraw.Draw(img)

    cert_id = str(row["certificate_id"])
    name = row["name"]
    gender = row["gender"].strip().lower()
    start_date = row["training_start_date"]
    end_date = row["training_end_date"]
    college = str(row["college"]) if "college" in row and pd.notna(row["college"]) else ""

    title = "Mr." if gender == "male" else "Miss."
    he_she = "he" if gender == "male" else "she"
    him_her = "him" if gender == "male" else "her"
    his_her = "his" if gender == "male" else "her"

    # --- Issued date as static variable ---
    issued_on = "03 July 2024"

    company = "Techvol Technologies Bharat Pvt. Ltd."
    course = "Python"

    # 🔹 Build first paragraph dynamically
    first_para = [("This is to certify that ", "regular"),
                  (f"{title} {name}", "bold")]
    if college.strip():
        first_para += [(", a student of ", "regular"),
                       (college, "bold")]
    first_para += [(", has successfully completed an internship at ", "regular"),
                   (company, "bold"),
                   (" from ", "regular"),
                   (f"{start_date} to {end_date}", "bold"),
                   (".", "regular")]

    # Paragraphs
    main_paragraphs = [
        first_para,
        [("During this period, ", "regular"),
         (he_she, "regular"),
         (" has worked in ", "regular"),
         (course, "bold"),
         (" and actively participated in various projects and tasks, demonstrating excellent performance and dedication.", "regular")],
        [("We wish ", "regular"),
         (him_her, "regular"),
         (" all the best for ", "regular"),
         (his_her, "regular"),
         (" future endeavours.", "regular")],
    ]

    # Layout
    line_height = 70
    para_spacing = 80
    x_margin = 180
    max_width = width - 180

    # 🔹 Start higher
    y_start = (height // 2) - 730
    y_text = y_start

    # Draw main paragraphs (part-1)
    for i, para in enumerate(main_paragraphs):
        y_text = draw_paragraph(draw, para, x_margin, y_text, max_width, line_height)
        # Add spacing only between paragraphs, not after last paragraph
        if i < len(main_paragraphs) - 1:
            y_text += para_spacing

    # Save PNG
    png_path = f"output/{cert_id}.png"
    pdf_path = f"output/{cert_id}.pdf"
    img.save(png_path)

    # --- Add Verify Block + Footer via ReportLab immediately after part-1 ---
    link = "https://validate.techvol.in"
    c = canvas.Canvas(pdf_path, pagesize=A4)

    # Set PDF title as the certificate holder's name
    c.setTitle(name)

    c.drawImage(ImageReader(png_path), 0, 0, width=A4[0], height=A4[1])

    # Map PNG Y coordinates to PDF coordinates
    pdf_scale = A4[1] / height
    pdf_x_margin = 45
    verify_y = (height - y_text) * pdf_scale - 30  # small gap after part-1
    link_y = verify_y - 22
    footer_y = link_y - 40

    # Verify block
    c.setFont("Helvetica", 13)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(pdf_x_margin, verify_y, "You can verify the certificate on portal using below link")

    # Link (clickable)
    c.setFont("Helvetica-Bold", 13)
    c.setFillColorRGB(0, 0, 1)
    c.drawString(pdf_x_margin, link_y, link)
    c.linkURL(link, (pdf_x_margin, link_y, pdf_x_margin + 400, link_y + 20), relative=0)

    # Certificate ID + Issued Date
    c.setFont("Helvetica", 13)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(pdf_x_margin, footer_y, f"Certificate ID: {cert_id}")
    c.drawString(pdf_x_margin, footer_y - 22, f"Issued On: {issued_on}")

    c.save()
    # Remove intermediate PNG
    os.remove(png_path) 