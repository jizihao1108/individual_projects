from PIL import Image
import os
from resizeimage import resizeimage

# get current directory and image directory
main_dir = os.getcwd()
pic_dir =  os.getcwd() + '\\img_orginal_source'

# change directory to image folder
os.chdir(pic_dir)

# check what is current directory
os.getcwd()

# Loop the image in current directory
for f in os.listdir('.'):
    pic = Image.open(f)
    fn, fext = os.path.splitext(f)
    print(fn, fext)    

# Example of open one image and resize it into optimal size for analysis
# open image and get its size and height
pic = Image.open('53403181_p0.png')
width, height = pic.size
print(width, height)

# first convert the smallest value (either width or height) into 300px
if (height < width):
    pic = resizeimage.resize_height(pic, 300)
#    pic.save('300/{}_300{}'.format('52261027_p0', '.png'))
else:
    pic = resizeimage.resize_width(pic, 300)
#    pic.save('300/{}_300{}'.format('52261027_p0', '.png'))

# Get the width, height and print them to check
width, height = pic.size
print(width, height)

# Crop the image from the centre to get 300*300 pixels images
pic = resizeimage.resize_crop(pic, [300, 300])

width, height = pic.size
print(width, height)

# Save image in the '300' folder
pic.save('300/{}_300{}'.format('52261027_p0', '.png'))
