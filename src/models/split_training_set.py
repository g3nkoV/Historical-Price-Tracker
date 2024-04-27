import os
import random
import pathlib
import subprocess
import pytesseract

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__),'../../'))
#training_text_file = os.path.abspath(os.path.join(project_root,'Data/tesseract_train_pol/pol.training.text'))
training_text_file = '../../Data/tesseract_train_pol/pol.training_text'

print(pytesseract.get_tesseract_version())

text2image_path = r'D:\Program Files (x86)\Tesseract_OCR\text2image.exe'

#font_dir = os.path.abspath(os.path.join(project_root,'Data/tesseract_train_pol/font'))
unicharset_dir=os.path.abspath(os.path.join(project_root,'Data/tesseract_train_pol/pol.unicharset'))

lines=[]

with open(training_text_file,'r',encoding='utf-8') as input_file:
    for line in input_file.readlines():
        lines.append(line.strip())

#output_dir = os.path.abspath(os.path.join(project_root,'Data/tesseract_train_pol/Sometype-ground-truth'))
output_dir = os.path.abspath(os.path.join(project_root,'tesstrain/data/Sometype-ground-truth'))

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

random.shuffle(lines)

count = 200

lines = lines[:count]
line_count = 0

for line in lines:
    training_text_file_name = pathlib.Path(training_text_file).stem
    line_training_text = os.path.join(output_dir,f"{training_text_file_name}_{line_count}.gt.txt")
    with open(line_training_text,'w',encoding='utf-8') as output_file:
        output_file.writelines(line+ '\n')
        #output_file.writelines([line])

    file_base_name = f"pol_{line_count}"

    subprocess.run([
        text2image_path,
        '--font=Sometype Mono Regular',
        f'--text={line_training_text}',
        f'--outputbase={output_dir}/{file_base_name}',
        '--max_pages=1',
        '--strip_unrenderable_words',
        '--leading=32',
        '--xsize=3600',
        '--ysize=250',
        '--char_spacing=1.0',
        '--exposure=0',
        f'--unicharset_file={unicharset_dir}'
    ],check=True)

    line_count+=1