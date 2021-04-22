import qrcode
from PIL import Image

logo_display = Image.open('../resources/images/logo.png')
logo_display.thumbnail((60, 60))

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=8,
)

# test
qr.add_data('test')
qr.make(fit=True)
#img = qrcode.make('test')
img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
logo_pos = ((img.size[0] - logo_display.size[0]) // 2, (img.size[1] - logo_display.size[1]) // 2)
img.paste(logo_display, logo_pos)
img.save("../qr_codes/qr_test.png")