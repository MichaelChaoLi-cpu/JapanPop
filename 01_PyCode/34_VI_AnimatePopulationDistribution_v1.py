# -*- coding: utf-8 -*-
"""
make population gif

Created on Fri Jul 22 14:06:14 2022

@author: li.chao.987@s.kyushu-u.ac.jp
"""

import glob
from PIL import Image

figure_location = "C:\\Users\\li.chao.987@s.kyushu-u.ac.jp\\OneDrive - Kyushu University\\17_Article\\03_RStudio\\05_Figure\\"
### total
figure_series = glob.glob(figure_location + "y????_log.jpg")

imgs = (Image.open(f) for f in sorted(figure_series))
img = next(imgs)
img.save(fp=figure_location+"zzz_total_log.gif", format='GIF', append_images=imgs,
         save_all=True, duration=1000, loop=0, quality=100, subsampling=0)

### female
figure_series = glob.glob(figure_location + "y????_female_log.jpg")

imgs = (Image.open(f) for f in sorted(figure_series))
img = next(imgs)
img.save(fp=figure_location+"zzz_female_log.gif", format='GIF', append_images=imgs,
         save_all=True, duration=1000, loop=0, quality=100, subsampling=0)

### male
figure_series = glob.glob(figure_location + "y????_male_log.jpg")

imgs = (Image.open(f) for f in sorted(figure_series))
img = next(imgs)
img.save(fp=figure_location+"zzz_male_log.gif", format='GIF', append_images=imgs,
         save_all=True, duration=1000, loop=0, quality=100, subsampling=0)