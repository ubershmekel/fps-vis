"""
After generating the pngs use ffmpeg to make the video file


"""

import os
import shutil
import sys
import subprocess

from PIL import Image, ImageDraw, ImageFont

fps_levels = [120, 60, 30, 15]
max_fps = max(fps_levels)
width = 480
height = len(fps_levels) * 100

pic_dir = 'outfps'
if os.path.exists(pic_dir):
    # make sure we don't use images from a previous run
    shutil.rmtree(pic_dir)

os.mkdir(pic_dir)

# get a font
fnt = ImageFont.truetype('/Library/Fonts/Roboto-Bold.ttf', 100)

y_start = -10
y_inc = 100

# -280 is barely visible from the left
# 450 is barely visible from the right
#x = -280
x_start = 10
x_inc = 4
f_x = [x_start] * len(fps_levels)


# +2 makes it loop more smoothly, not sure why
frame_count = (width // x_inc) + 1
for frame in range(frame_count):
    img = Image.new('RGB', (width, height), (0,0,0))
    draw = ImageDraw.Draw(img)

    for i, fps in enumerate(fps_levels):
        # start centered
        draw.text((f_x[i], y_start + y_inc * i), "%sFPS" % fps, font=fnt, fill=(255,255,255))
        # finish centered
        draw.text((f_x[i] - width, y_start + y_inc * i), "%sFPS" % fps, font=fnt, fill=(255,255,255))
        # update positions
        skip_frames = max_fps // fps
        if frame % skip_frames == skip_frames - 1:
            f_x[i] += x_inc * skip_frames

    # img.show()
    # exit()
    img.save(os.path.join(pic_dir, '%03d.png' % frame))
    sys.stdout.write('.')


print('done generating images')
cmd = 'ffmpeg -y -framerate {max_fps} -i {pic_dir}/%03d.png video.mp4'.format(pic_dir=pic_dir, max_fps=max_fps)
print(cmd)
subprocess.check_call(cmd, shell=True)

print('done generating video.mp4')
