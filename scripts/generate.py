import os
import random
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont

# =========================================================
# CONFIGURATION
# =========================================================

WIDTH = 1080
HEIGHT = 1080

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PHOTOS_DIR = os.path.join(BASE_DIR, "photos")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

LOGO_PATH = os.path.join(ASSETS_DIR, "logo.png")

SCHOOL_NAME = "COLUMBUS MODEL HIGH SCHOOL"
TAGLINE = "Admissions Open 2026-27"
LOCATION = "Mayuri Nagar, Miyapur"

CONTACTS = [
    "9000232197",
    "9030474447",
    "040-45200470"
]

PHONE_TEXT = " | ".join(CONTACTS)

CAPTIONS = [
    "Empowering Young Minds for a Better Future",
    "Where Learning Meets Excellence",
    "Inspiring Excellence Since 1997",
    "Quality Education with Strong Values",
    "Admissions Open for 2026-27",
    "Enroll Today for a Bright Future",
    "Learning Today, Leading Tomorrow",
    "Building Confidence and Character",
    "Excellence in Academics and Activities",
    "Shaping Future Leaders"
]

# =========================================================
# CREATE OUTPUT DIRECTORY
# =========================================================

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================================================
# LOAD RANDOM PHOTOS
# =========================================================

photo_files = [
    os.path.join(PHOTOS_DIR, file)
    for file in os.listdir(PHOTOS_DIR)
    if file.lower().endswith((".jpg", ".jpeg", ".png"))
]

if len(photo_files) == 0:
    raise Exception("No photos found inside photos/ folder")

selected_photos = random.sample(
    photo_files,
    min(3, len(photo_files))
)

# =========================================================
# CREATE BASE CANVAS
# =========================================================

canvas = Image.new("RGB", (WIDTH, HEIGHT), "white")

# =========================================================
# PHOTO GRID LAYOUT
# =========================================================

positions = [
    (0, 0, 540, 540),
    (540, 0, 1080, 540),
    (0, 540, 1080, 780)
]

for photo_path, pos in zip(selected_photos, positions):

    img = Image.open(photo_path).convert("RGB")

    target_width = pos[2] - pos[0]
    target_height = pos[3] - pos[1]

    img = img.resize((target_width, target_height))

    canvas.paste(img, (pos[0], pos[1]))

# =========================================================
# DARK OVERLAY
# =========================================================

overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 70))
canvas = Image.alpha_composite(
    canvas.convert("RGBA"),
    overlay
)

draw = ImageDraw.Draw(canvas)

# =========================================================
# LOAD FONTS
# =========================================================

try:
    title_font = ImageFont.truetype("arial.ttf", 60)
    subtitle_font = ImageFont.truetype("arial.ttf", 42)
    small_font = ImageFont.truetype("arial.ttf", 30)
except:
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    small_font = ImageFont.load_default()

# =========================================================
# ADD LOGO
# =========================================================

if os.path.exists(LOGO_PATH):

    logo = Image.open(LOGO_PATH).convert("RGBA")

    logo_size = 180

    logo.thumbnail((logo_size, logo_size))

    logo_x = (WIDTH - logo.width) // 2
    logo_y = 20

    canvas.paste(logo, (logo_x, logo_y), logo)

# =========================================================
# BOTTOM BANNER
# =========================================================

banner_top = 780

draw.rectangle(
    [(0, banner_top), (WIDTH, HEIGHT)],
    fill=(0, 51, 102)
)

# =========================================================
# TITLE
# =========================================================

title_text = "ADMISSIONS OPEN"

bbox = draw.textbbox(
    (0, 0),
    title_text,
    font=title_font
)

title_width = bbox[2] - bbox[0]

draw.text(
    ((WIDTH - title_width) / 2, 810),
    title_text,
    fill="white",
    font=title_font
)

# =========================================================
# SCHOOL NAME
# =========================================================

bbox = draw.textbbox(
    (0, 0),
    SCHOOL_NAME,
    font=subtitle_font
)

school_width = bbox[2] - bbox[0]

draw.text(
    ((WIDTH - school_width) / 2, 885),
    SCHOOL_NAME,
    fill=(255, 215, 0),
    font=subtitle_font
)

# =========================================================
# LOCATION
# =========================================================

bbox = draw.textbbox(
    (0, 0),
    LOCATION,
    font=small_font
)

location_width = bbox[2] - bbox[0]

draw.text(
    ((WIDTH - location_width) / 2, 940),
    LOCATION,
    fill="white",
    font=small_font
)

# =========================================================
# RANDOM CAPTION
# =========================================================

caption = random.choice(CAPTIONS)

bbox = draw.textbbox(
    (0, 0),
    caption,
    font=small_font
)

caption_width = bbox[2] - bbox[0]

draw.text(
    ((WIDTH - caption_width) / 2, 985),
    caption,
    fill="white",
    font=small_font
)

# =========================================================
# CONTACT DETAILS
# =========================================================

bbox = draw.textbbox(
    (0, 0),
    PHONE_TEXT,
    font=small_font
)

phone_width = bbox[2] - bbox[0]

draw.text(
    ((WIDTH - phone_width) / 2, 1030),
    PHONE_TEXT,
    fill=(255, 255, 255),
    font=small_font
)

# =========================================================
# SAVE POSTER
# =========================================================

filename = datetime.now().strftime(
    "cmhs_admissions_%Y%m%d.jpg"
)

output_path = os.path.join(
    OUTPUT_DIR,
    filename
)

canvas.convert("RGB").save(
    output_path,
    quality=95
)

print(f"Poster generated successfully:")
print(output_path)