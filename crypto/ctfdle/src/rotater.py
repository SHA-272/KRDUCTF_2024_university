import random
from PIL import Image

image_files =['1.webp', '2.webp', '3.webp', '4.webp', '5.webp', '6.webp', '7.webp', '8.webp', '9.webp', '10.webp', '11.webp', '12.webp', '13.webp', '14.webp', '15.webp', '16.webp', '17.webp', '18.webp', '19.webp', '20.webp', '21.webp', '22.webp', '23.webp', '24.webp', '25.webp', '26.webp', '27.webp', '28.webp', '29.webp', '30.webp']

for image_path in image_files:
    image = Image.open(image_path)

image = image.convert('L')

angle = random.choice([90,180,270, 360])
image = image.rotate(angle)


for image_path in image_files:
    image.save(f'output_{image.split("/")[-1]}')