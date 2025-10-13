import qrcode
URL=input("Enter URL:")
img=qrcode.make(URL)
img.save(qrcode.png)
