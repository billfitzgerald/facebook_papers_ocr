import os
from fnmatch import fnmatch
import ocrmypdf

#######################################################
# Only process pdfs where you trust the source docs!! #
# PDFs are a mess, and have a well worn history of    #
# delivering malware (and ugly charts and graphs).    #
#######################################################

source_docs = './fb_docs/'
text_output_dir = 'processed_text/' #create this dir

count = 0
sc = 0
screwy = 0
screwylist = []

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
            outputfiletxt = f.replace(".pdf", ".txt")
            outputfiletxt = text_output_dir + outputfiletxt
            print(fn)
            try: 
                # Experiment with different output and cleanup options
                # Depending on the source doc, one approach might be more effective
                # ocrmypdf.ocr(fn, text_output_dir + f, deskew=True, sidecar=outputfiletxt, remove_background=True)
                # ocrmypdf.ocr(fn, text_output_dir + f, deskew=True, sidecar=outputfiletxt)
                ocrmypdf.ocr(fn, text_output_dir + f, deskew=True, sidecar=outputfiletxt, remove_background=True, pdfa_image_compression="jpeg")
            except:
                print(f"Check {f} because the scan didn't work.")
                screwy += 1
                screwylist.append(f)
        else:
            pass
count = count - screwy
print(f"{count} files converted to jpgs.")
print(f"{screwy} docs need to be reviewed. See:")
for s in screwylist:
    print(s)