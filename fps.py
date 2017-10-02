"""
After generating the pngs use ffmpeg to make the video file


"""

import os
import shutil
import sys
import subprocess

from PIL import Image, ImageDraw, ImageFont

WIDTH = 480
HEIGHT = 300

PIC_DIR = 'outfps'
if os.path.exists(PIC_DIR):
    # make sure we don't use images from a previous run
    shutil.rmtree(PIC_DIR)

os.mkdir(PIC_DIR)

# get a font
fnt = ImageFont.truetype('/Library/Fonts/Roboto-Bold.ttf', 100)

y_start = -10
y_inc = 100

# -280 is barely visible from the left
# 450 is barely visible from the right
#x = -280
x_start = 10
f_60_x = x_start
f_30_x = x_start
f_15_x = x_start
x_inc = 8
# +2 makes it loop more smoothly, not sure why
frame_count = (WIDTH // x_inc) + 2
for i in range(frame_count):
    img = Image.new('RGB', (WIDTH, HEIGHT), (0,0,0))
    draw = ImageDraw.Draw(img)

    # start centered
    draw.text((f_60_x, y_start), "60FPS", font=fnt, fill=(255,255,255))
    draw.text((f_30_x, y_start + y_inc), "30FPS", font=fnt, fill=(255,255,255))
    draw.text((f_15_x, y_start + 2 * y_inc), "15FPS", font=fnt, fill=(255,255,255))

    # finish centered
    draw.text((f_60_x - WIDTH, y_start), "60FPS", font=fnt, fill=(255,255,255))
    draw.text((f_30_x - WIDTH, y_start + y_inc), "30FPS", font=fnt, fill=(255,255,255))
    draw.text((f_15_x - WIDTH, y_start + 2 * y_inc), "15FPS", font=fnt, fill=(255,255,255))

    # img.show()
    # exit()
    img.save(os.path.join(PIC_DIR, '%03d.png' % i))
    if i > frame_count / 2:
        sys.stdout.write('%s,' % (f_60_x - WIDTH))
    else:
        sys.stdout.write('%s,' % f_60_x)

    # update positions
    f_60_x += x_inc
    if i % 2 == 1:
        f_30_x += x_inc * 2
    if i % 4 == 3:
        f_15_x += x_inc * 4


print('done generating images')
cmd = 'ffmpeg -y -r 60 -framerate 60 -i {pic_dir}/%03d.png video+3.mp4'.format(pic_dir=PIC_DIR)
print(cmd)
subprocess.check_call(cmd, shell=True)

print('done generating video.mp4')
'''ffmpeg -y -framerate 60 -i outfps/%03d.png -vcodec libx264 -x264-params keyint=1:no-scenecut video.mp4
ffmpeg -y -framerate 60 -i outfps/%03d.png \
    -x264opts no-scenecut -g 1 \
    video.mp4


ffmpeg -y -framerate 60 -i outfps/%03d.png -vcodec mjpeg video.mj.mp4


'''
