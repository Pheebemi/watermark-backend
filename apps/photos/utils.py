from PIL import Image, ImageOps


def add_church_watermark(photo_path: str, logo_path: str, output_path: str) -> None:
    photo = ImageOps.exif_transpose(Image.open(photo_path)).convert("RGBA")
    logo = Image.open(logo_path).convert("RGBA")

    # Resize logo to 40% of photo width, preserve aspect ratio
    logo_width = photo.width * 2 // 5
    ratio = logo_width / logo.width
    logo = logo.resize((logo_width, int(logo.height * ratio)), Image.LANCZOS)

    # Center bottom with 20px padding
    x = (photo.width - logo.width) // 2
    y = photo.height - logo.height - 20

    photo.paste(logo, (x, y), logo)  # logo alpha acts as mask
    photo.convert("RGB").save(output_path, "JPEG", quality=90)
