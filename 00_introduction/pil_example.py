from PIL import Image, ImageDraw

image = Image.new("RGB", (320, 320), (0, 0, 0, 0))

draw = ImageDraw.Draw(image)

draw.ellipse((10, 10, 300, 300), fill="red", outline="red")

del draw
image.save("test.png", "PNG")
