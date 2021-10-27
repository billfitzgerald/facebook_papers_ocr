import os
from fnmatch import fnmatch
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
	PDFInfoNotInstalledError,
	PDFPageCountError,
	PDFSyntaxError
)
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
# suppress DecompressionBombWarning
# Only allow this if you are 100% confident
# that source documents are safe.
# This can also crash systems with limited memory.
# Beware - thar be dragons here.
Image.MAX_IMAGE_PIXELS = None

source_docs = './fb_docs/'
image_output_dir = 'pdf_image/fb/' # create this dir
text_output_dir = 'text_from_pdf/fb/' #create this dir

count = 0
sc = 0
screwy = 0
file_ext = "*.pdf" # only get pdf files - adjust as needed, set to *.* for all
for path, subdirs, files in os.walk(source_docs):
	for f in files:
		if fnmatch(f,file_ext):
			count += 1
			sc += 1
			if sc == 50:
				print(f'Processed {count} files.')
				sc = 0
			else: 
				pass
			fn = os.path.join(path,f)
			try: 
				images_from_path = convert_from_path(fn)
			except:
				print(f"Check {f} because convert_from_path didn't work.")
				screwy += 1
			for i in range(len(images_from_path)):
				try:
					file_txt = f.replace('.pdf', '')
					if i < 10:
						num = "00" + str(i)
					elif i >= 10 and i < 100:
						num = "0" + str(i)
					else:
						pass
					images_from_path[i].save(image_output_dir + file_txt + '_page_' + num +'.jpg', 'JPEG')
				except:
					print(f"Check {f} for something screwy")
					screwy += 1
		else:
			pass
count = count - screwy
print(f"{count} files converted to jpgs.")
print(f"{screwy} docs need to be reviewed.")

count = 0
screwy = 0
file_group_list = []

file_ext = "*.jpg" 
for path, subdirs, files in os.walk(image_output_dir):
	for f in files:
		if fnmatch(f,file_ext):
			fgl_split = f.split("_page_")
			fgl = fgl_split[0]
			if fgl not in file_group_list:
				file_group_list.append(fgl)
			else:
				pass
		else:
			pass
print(len(file_group_list))

for fgl in file_group_list:
	process_list = []
	text_full = ""
	outputfile = text_output_dir + fgl + '.txt'
	for path, subdirs, files in os.walk(image_output_dir):
		for f in files:
			if f.startswith(fgl):
				process_list.append(f)
			else:
				pass
		process_list.sort()
		for p in process_list:
			fn = os.path.join(path,p)
			im = Image.open(fn)
			#im = im.filter(ImageFilter.MedianFilter())
			#enhancer = ImageEnhance.Contrast(im)
			#im = enhancer.enhance(2)
			#im = im.convert('1')
			text = pytesseract.image_to_string(im, lang='eng')
			text_full = text_full + text
		with open(outputfile,'a') as md:
			md.write(text_full)
		