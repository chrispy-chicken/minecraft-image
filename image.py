from PIL import Image
import os, csv

file = "mcimage/dd.jpg"

h = 64
w = 64

size = h, w
current_difference = 16777215
n = 0

with Image.open(file) as im:
    fn, _ = os.path.splitext(file)
    im.resize(size).save(fn + ".r.jpg")
    file_r = fn + ".r.jpg"

with open("mcimage/fill.mcfunction", "w") as func:
    with Image.open(file_r) as im:
        rgb_im = im.convert('RGB')
        for i in range(h):
            for j in range(w):
                rgb = rgb_im.getpixel((j, i))
                value = int('0x' + ''.join(f'{i:02X}' for i in rgb), 16)
                with open('mcimage/names.csv', 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:                     
                        diff = abs(value - int(row['color']))
                        if diff < current_difference:
                            current_difference = diff                          
                            current_block = row['blockid']
                func.write(f"execute as @p run setblock ~{j} ~ ~{i} {current_block}\n")
                # n += 1
                # print(n)
                print(j, i)
                current_difference = 16777215