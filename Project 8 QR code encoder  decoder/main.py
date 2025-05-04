"""Uncomment all the code if you want to change the color of the qr in image"""

""" For encoding the qr code """

# import qrcode

# data = 'Don\'t forget to subscribe!'

# qr = qrcode.QRCode(version = 1 , box_size= 10 , border = 5)

# qr.add_data(data)

# qr.make(fit = True)
# img = qr.make_image(fill_color = 'green' , back_color = 'white')

# # jahan pr img ho gi qr ki wo path mention krna ha phir streamlit ki command run krni ha to color change ho jaya ga
# # img.save('C:/Users/DELL/Downloads/islamic videos/qr code.png') 
# img.save('E:/governor project/python/25_Python_Projects/Project 8 QR code encoder  decoder/qr code.png')


""" For decoding the qr code """
from pyzbar.pyzbar import decode
from PIL import Image

img = Image.open('E:/governor project/python/25_Python_Projects/Project 8 QR code encoder  decoder/qr code.png')

result = decode(img)
 
print(result)