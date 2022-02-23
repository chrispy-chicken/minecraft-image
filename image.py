from PIL import Image
import os, csv

# set image path
# remove 'path/' if file is in current directory
file = "path/filename.jpg"

# set height and with of image
h = 64
w = 64

size = h, w
# max hex color (#ffffff)
current_difference = 16777215

# optional counter to track progress of this script
counter = 0

# creates resized image
with Image.open(file) as im:
    fn, _ = os.path.splitext(file)
    im.resize(size).save(fn + ".r.jpg")
    file_r = fn + ".r.jpg"


with open("fill.mcfunction", "w") as func:
    with Image.open(file_r) as im:
        rgb_im = im.convert('RGB')
        for i in range(h):
            for j in range(w):

                # for every pixel check the csv for the most likely block using the difference 
                # of color hex to decimal values
                rgb = rgb_im.getpixel((j, i))
                value = int('0x' + ''.join(f'{i:02X}' for i in rgb), 16)
                with open('names.csv', 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:                     
                        diff = abs(value - int(row['color']))
                        if diff < current_difference:
                            current_difference = diff                          
                            current_block = row['blockid']
                func.write(f"execute as @p run setblock ~{j} ~ ~{i} {current_block}\n")

                # this counter will run until h * w is reached
                # remove next 2 comments for the counter 
                # counter += 1
                # print(counter)
                current_difference = 16777215
