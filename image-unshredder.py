from random import shuffle
from PIL import Image
import math
import sys


def shred(imagePath, numOfShreds):
    SHREDS = numOfShreds
    image = Image.open(imagePath)
    shredded = Image.new('RGBA', image.size)
    width, height = image.size
    shred_width = int(width/SHREDS)
    print(shred_width)
    sequence = list(range(0, SHREDS))
    shuffle(sequence)
    for i, shred_index in enumerate(sequence):
        shred_x1, shred_y1 = shred_width * shred_index, 0
        shred_x2, shred_y2 = shred_x1 + shred_width, height
        region =image.crop((shred_x1, shred_y1, shred_x2, shred_y2))
        shredded.paste(region, (shred_width * i, 0))
        shredded.save('shredded.png')
    return shred_width

def distance(pixel1, pixel2):
    return math.sqrt((pixel1[0] - pixel2[0])**2 + (pixel1[1] - pixel2[1])**2 + (pixel1[2] - pixel2[2])**2 )

# direction = 0 => attech _image2 to left of _image1
def edgeDistance(_image1, _image2, direction):
    image1 = _image1.getdata()
    image2 = _image2.getdata()
    width, height = image1.size
    if direction == 0:
        return sum([distance(image1[i*width], image2[(width-1) + i*width]) for i in range(height)])
    else:
        return sum([distance(image1[(width-1) + i*width], image2[i*width]) for i in range(height)]) 

def main(imagePath, numOfShreds):
    image = Image.open(imagePath)
    width, height = image.size
    num = numOfShreds
    strips = []
    strip_width = int(width/num)
    for i in range(num):
        strips.append(image.crop((strip_width*i, 0, strip_width*(i+1), height)))
    final_image = [strips[0]]
    strips.pop(0)
    while len(strips) != 0:
        cur_left = final_image[0]
        cur_right = final_image[-1]
        min_left, min_right, left_i, right_i = math.inf, math.inf, None, None
        for i in range(0, len(strips)):
            if min_left > edgeDistance(cur_left, strips[i], 0):
                min_left = edgeDistance(cur_left, strips[i], 0) 
                left_i = i
            if min_right > edgeDistance(cur_right, strips[i], 1):
                min_right = edgeDistance(cur_right, strips[i], 1) 
                right_i = i
        if(min_left < min_right):
            final_image.insert(0, strips.pop(left_i))
        else:
            print(min_right)
            final_image.append(strips.pop(right_i))

    unshredded = Image.new('RGBA', image.size)
    for i in range(numOfShreds):
        unshredded.paste(final_image[i], (i*strip_width, 0))
    unshredded.save('unshredded.png', 'PNG')



if __name__ == "__main__":
    if sys.argv[1] == "s":
        shred(sys.argv[2], int(sys.argv[3]))
    elif sys.argv[1] == "u":
        main(sys.argv[2], int(sys.argv[3]))
    else:
        print("Invalid options")