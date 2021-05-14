import qrcode
from PIL import Image

logo_display = Image.open('../resources/images/logo.png')
logo_display.thumbnail((60, 60))



# test
qr_list = ['nawak', 'hihihi', 'essaye_encore',
           'mortdelol', 'fauxqr', 'qrcoude', 'enigme_map']
for i in range (2,18):
    qr_list.append('log_'+str(i))

for elt in qr_list:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=8,
    )
    qr.add_data(elt)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    logo_pos = ((img.size[0] - logo_display.size[0]) // 2, (img.size[1] - logo_display.size[1]) // 2)
    img.paste(logo_display, logo_pos)
    img.save("../qr_codes/" + elt + ".png")