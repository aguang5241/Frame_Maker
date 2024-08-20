import os
from PIL import Image, ExifTags, ImageFont, ImageDraw

def main(path):
    # Get image information
    img = Image.open(path)
    exif = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS }
    # print(img._getexif().items())
    # exit()
    # Get content created time
    img_format = img.format
    img_mode = img.mode
    img_size = os.path.getsize(path) / (1024 * 1024)
    img_width, img_height = img.size
    img_is_horizontal = img_width > img_height
    img_resolution = img.info['dpi']
    img_make = exif['Make'].split()[0]
    img_model = exif['Model'].rstrip('\x00')
    img_date = exif['DateTimeDigitized'].rstrip('\x00')
    img_shutter = f'1/{int(1/exif["ExposureTime"])}'
    img_aperture = exif['FNumber']
    img_iso = exif['ISOSpeedRatings']
    img_focal_length = f'{int(exif["FocalLength"])}'

    # Create border
    path_new = f"{path.split('/')[-1].split('.')[0]}_new.jpg"
    if not os.path.exists('output'):
        os.makedirs('output')
    path_new = f'output/{path_new}'
    border_width, border_height = img_width, img_height // 10
    ratio = 5568 / border_width
    border = Image.new(img_mode, (border_width, border_height), (255, 255, 255))

    # Add logo to border
    logo = Image.open(logo_path).convert('RGBA')
    logo_width, logo_height = int(border_height * 0.6), int(border_height * 0.6)
    if img_is_horizontal:
        logo_position = (int(border_width * 0.68), int(border_height * 0.2))
    else:
        logo_position = (int(border_width * 0.40), int(border_height * 0.2))
    logo = logo.resize((logo_width, logo_height))
    border.paste(logo, logo_position)
    # Draw vertical line on the right side of the logo
    draw = ImageDraw.Draw(border)
    if img_is_horizontal:
        line_position = (int((logo_position[0] + logo_width) * 1.02), int(border_height * 0.2))
    else:
        line_position = (int((logo_position[0] + logo_width) * 1.03), int(border_height * 0.2))
    draw.line([(line_position[0], line_position[1]), (line_position[0], line_position[1] + logo_height)], fill=(200, 200, 200), width=int(10/ratio))
    # Add model information to border
    if img_is_horizontal:
        img_model_font = ImageFont.truetype('Arial Bold.ttf', int(100/ratio))
        img_model_position = (int(border_width * 0.05), int(border_height * 0.20))
    else:
        img_model_font = ImageFont.truetype('Arial Bold.ttf', int(200/ratio))
        img_model_position = (int(border_width * 0.05), int(border_height * 0.25))
    draw.text(img_model_position, f'{img_model}', (0, 0, 0), font=img_model_font)
    # Add date information to border
    if img_is_horizontal:
        img_date_font = ImageFont.truetype('Arial.ttf', int(80/ratio))
        img_date_position = (int(border_width * 0.05), int(border_height * 0.60))
    else:
        img_date_font = ImageFont.truetype('Arial.ttf', int(150/ratio))
        img_date_position = (int(border_width * 0.05), int(border_height * 0.60))
    draw.text(img_date_position, f'{img_date}', (120, 120, 120), font=img_date_font)
    # Add shot information to border
    if img_is_horizontal:
        shot_font = ImageFont.truetype('Arial Bold.ttf', int(90/ratio))
        shot_position = (int((logo_position[0] + logo_width) * 1.04), int(border_height*0.35))
    else:
        shot_font = ImageFont.truetype('Arial Bold.ttf', int(180/ratio))
        shot_position = (int((logo_position[0] + logo_width) * 1.06), int(border_height*0.40))
    shot_text = f'{img_focal_length}mm  f/{img_aperture}  {img_shutter}  ISO{img_iso}'
    draw.text(shot_position, shot_text, (0, 0, 0), font=shot_font)

    # Add border to image
    img_new = Image.new(img_mode, (img_width, img_height + border_height), (255, 255, 255))
    img_new.paste(img, (0, 0))
    img_new.paste(border, (0, img_height))
    img_new.save(path_new, img_format, quality=100, exif=img.info['exif'], dpi=img_resolution)

    # Get new image information
    img_new = Image.open(path_new)
    exif_new = { ExifTags.TAGS[k]: v for k, v in Image.open(path_new)._getexif().items() if k in ExifTags.TAGS }
    img_new_format = img_new.format
    img_new_mode = img_new.mode
    img_new_size = os.path.getsize(path_new) / (1024 * 1024)
    img_new_width, img_new_height = img_new.size
    img_new_resolution = img_new.info['dpi']
    img_new_make = exif_new['Make'].split()[0]
    img_new_model = exif_new['Model']
    img_new_date = exif_new['DateTimeDigitized']
    img_new_shutter = f'1/{int(1/exif_new["ExposureTime"])}'
    img_new_aperture = exif_new['FNumber']
    img_new_iso = exif_new['ISOSpeedRatings']
    img_new_focal_length = f'{int(exif_new["FocalLength"])}'

    # Display original and new image information
    print('\n\t\t\t Before \t\t After')
    print(f'Image:\t\t\t {path}\t\t {path_new}')
    print(f'Format:\t\t\t {img_format}\t\t\t {img_new_format}')
    print(f'Mode:\t\t\t {img_mode}\t\t\t {img_new_mode}')
    print(f'Size:\t\t\t {img_size:.2f}MB\t\t\t {img_new_size:.2f}MB')
    print(f'Width:\t\t\t {img_width}\t\t\t {img_new_width}')
    print(f'Height:\t\t\t {img_height}\t\t\t {img_new_height}')
    print(f'Resolution:\t\t {img_resolution}\t\t {img_new_resolution}')
    print(f'Make:\t\t\t {img_make}\t\t\t {img_new_make}')
    print(f'Model:\t\t\t {img_model}\t\t {img_new_model}')
    print(f'Date:\t\t\t {img_date}\t {img_new_date}')
    print(f'Shutter:\t\t {img_shutter}\t\t\t {img_new_shutter}')
    print(f'Aperture:\t\t {img_aperture}\t\t\t {img_new_aperture}')
    print(f'ISO:\t\t\t {img_iso}\t\t\t {img_new_iso}')
    print(f'FocalLength:\t\t {img_focal_length}\t\t\t {img_new_focal_length}')

if __name__ == '__main__':
    # Get all the images in the input folder
    input_folder = 'input'
    logo_path = 'res/logo_Nikon.png'
    img_paths = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
    for img_path in img_paths:
        main(f'{input_folder}/{img_path}')
        print(f'{img_path} is processed successfully.')
        exit()