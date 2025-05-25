from math import floor
from pathlib import Path
import queue
import threading
from PIL import Image, ImageDraw, ImageFont
import logging
import os
import sys
from datetime import datetime
from multiprocessing import Pool
from multiprocessing.connection import Listener
import copy

WHITE = (255,255,255)
TRANSPARENT = (0,0,0, 0)
BLACK = (0,0,0)
ORANGE = (255, 92, 00)

DEFAULT_BACKGROUND = WHITE
FONT_SIZE = 14
DEFAULT_DATE = False
DEFAULT_DARK = False

DEFAULT_ASPECT_RATIO = (5/4)
# DEFAULT_ASPECT_RATIO = (1/1)
DEFAULT_PADDING_PERCENT = 1/12



def pad_file(f, outpath):
	# TODO Rewrite
	logging.info(f"File: {f}")
	imgpath = Path(f)
	logging.debug(imgpath.parts)
	logging.debug(imgpath.parts[:-1])
	base_dir = imgpath.parts[:-1]
	file_name = imgpath.parts[-1]
	try:
		with Image.open(f) as img:
			bigger_side = max(img.size)
			smaller_side = min(img.size)
			left = 0
			top = 0
			ar = DEFAULT_ASPECT_RATIO
			width, height = img.size[0], floor(img.size[0] * ar)
			target_width, target_height = floor(width*(1-2*DEFAULT_PADDING_PERCENT)), floor(height*(1-2*DEFAULT_PADDING_PERCENT))
			
			logging.debug("Generating white background")
			result = Image.new(img.mode, (width, height), DEFAULT_BACKGROUND)
			logging.debug("Pasting image over white background")

			resized_image = img.copy()
			resized_image.thumbnail((target_width,target_height))
			
			final_width, final_height = resized_image.size
			# print(width, height)
			top = (height-final_height)//2
			left = (width-final_width)//2
			# print(top, left)
			logging.debug("pasting image")
			result.paste(resized_image, (left, top))
			logging.debug("saving padded image")
		
			result.save(outpath, "JPEG", quality=60)
	except:
		logging.exception('')
