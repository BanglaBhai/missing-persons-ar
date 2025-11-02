from PIL import Image, ImageDraw, ImageFont
import os
from io import BytesIO


def generate_flyer_image(person):
    """Generate a professional flyer image for a missing person"""
    
    # Canvas size
    width, height = 1080, 1920
    img = Image.new('RGB', (width, height), color='#1a1a1a')
    draw = ImageDraw.Draw(img)
    
    # Colors
    red = '#e74c3c'
    white = '#ffffff'
    gray = '#aaaaaa'
    dark_gray = '#333333'
    
    # Load and place photo
    if person.photo:
        try:
            photo = Image.open(person.photo.path)
            photo = photo.resize((900, 900), Image.Resampling.LANCZOS)
            img.paste(photo, (90, 100))
        except Exception as e:
            print(f"Error loading photo: {e}")
    
    # Load fonts
    try:
        font_tag = ImageFont.truetype("arial.ttf", 35)
        font_name = ImageFont.truetype("arialbd.ttf", 90)
        font_label = ImageFont.truetype("arial.ttf", 35)
        font_value = ImageFont.truetype("arial.ttf", 45)
    except:
        try:
            font_tag = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 35)
            font_name = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 90)
            font_label = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 35)
            font_value = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 45)
        except:
            font_tag = ImageFont.load_default()
            font_name = ImageFont.load_default()
            font_label = ImageFont.load_default()
            font_value = ImageFont.load_default()
    
    # "MISSING PERSON" tag
    draw.rounded_rectangle([(90, 30), (400, 85)], radius=25, fill=red)
    draw.text((110, 42), "MISSING PERSON", fill=white, font=font_tag)
    
    # Name
    y_pos = 1050
    draw.text((90, y_pos), person.name.upper(), fill=white, font=font_name)
    
    # Physical Description
    y_pos += 150
    draw.text((90, y_pos), "PHYSICAL DESCRIPTION", fill=gray, font=font_label)
    y_pos += 55
    desc = person.get_physical_description()
    if len(desc) > 50:
        desc = desc[:50] + "..."
    draw.text((90, y_pos), desc, fill=white, font=font_value)
    
    # Line separator
    y_pos += 100
    draw.rectangle([(90, y_pos), (width - 90, y_pos + 2)], fill=dark_gray)
    
    # Last Seen
    y_pos += 30
    draw.text((90, y_pos), "LAST SEEN", fill=gray, font=font_label)
    y_pos += 55
    draw.text((90, y_pos), f"Date: {person.last_seen_date.strftime('%B %d, %Y')}", fill=white, font=font_value)
    y_pos += 65
    location = person.last_seen_location[:45] + "..." if len(person.last_seen_location) > 45 else person.last_seen_location
    draw.text((90, y_pos), f"Location: {location}", fill=white, font=font_value)
    
    # Line separator
    y_pos += 100
    draw.rectangle([(90, y_pos), (width - 90, y_pos + 2)], fill=dark_gray)
    
    # Circumstances
    y_pos += 30
    draw.text((90, y_pos), "CIRCUMSTANCES", fill=gray, font=font_label)
    y_pos += 55
    circumstances = person.circumstances[:90] + "..." if len(person.circumstances) > 90 else person.circumstances
    if len(circumstances) > 45:
        line1 = circumstances[:45]
        line2 = circumstances[45:]
        draw.text((90, y_pos), line1, fill=white, font=font_value)
        y_pos += 65
        draw.text((90, y_pos), line2, fill=white, font=font_value)
    else:
        draw.text((90, y_pos), circumstances, fill=white, font=font_value)
    
    # Line separator
    y_pos += 100
    draw.rectangle([(90, y_pos), (width - 90, y_pos + 2)], fill=dark_gray)
    
    # Contact Information
    y_pos += 30
    draw.text((90, y_pos), "IF YOU HAVE INFORMATION", fill=gray, font=font_label)
    y_pos += 55
    draw.text((90, y_pos), f"Contact: {person.contact_name}", fill=white, font=font_value)
    y_pos += 65
    draw.text((90, y_pos), f"Phone: {person.contact_phone}", fill=white, font=font_value)
    
    if person.police_case_number:
        y_pos += 65
        draw.text((90, y_pos), f"Case #: {person.police_case_number}", fill=white, font=font_value)
    
    # Save to BytesIO
    buffer = BytesIO()
    img.save(buffer, format='PNG', quality=95)
    buffer.seek(0)
    
    return buffer