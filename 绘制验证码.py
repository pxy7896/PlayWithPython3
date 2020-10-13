from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

def get_random_char():
    return chr(random.randint(65, 90))

def get_random_color(low, high):
    return (random.randint(low, high), random.randint(low, high), random.randint(low, high))

def draw_yanzhengma(file_name):
    height = 60;
    width = 60 * 4;
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # need path. 
    font = ImageFont.truetype("C:/Windows/Fonts/Arial.ttf", 36)
    draw = ImageDraw.Draw(image)
    # each pixel
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=get_random_color(64, 255))
    # text
    for t in range(4):
        draw.text((60*t+10, 10), get_random_char(), font=font, fill=get_random_color(32, 127))
    #image = image.filter(ImageFilter.BLUR)
    image.save(file_name)

if __name__ == '__main__':
    draw_yanzhengma('yanzhengma.jpg')