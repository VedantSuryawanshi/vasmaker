import qrcode
from PIL import Image
import os

# Create a directory to save the QR codes
output_dir = "assets"
os.makedirs(output_dir, exist_ok=True)

# Generate QR codes for the range 1435 to 2000
start_number = 1500
end_number = 1700

for number in range(start_number, end_number + 1):
    url = f"https://cars.mekit.in/{number}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert('RGBA')

    # Make the white background transparent
    data = img.getdata()
    new_data = []
    for item in data:
        # Change all white (also shades of whites) to transparent
        if item[0] in list(range(200, 256)):
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    img.putdata(new_data)

    # Resize the image to 66 px width while maintaining aspect ratio
    img = img.resize((66, 66), Image.LANCZOS)

    img_filename = os.path.join(output_dir, f"{number}.png")
    img.save(img_filename)

print(f"Generated QR codes for URLs from {start_number} to {end_number} and saved them in the '{output_dir}' directory.")
