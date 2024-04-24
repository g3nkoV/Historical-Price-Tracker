from pathlib import Path


tesseract_cmd_path=r"D:\\Program Files (x86)\\Tesseract_OCR\\tesseract.exe"

#Obecny folder
current_folder = Path(__file__).resolve()
#Katalog główny
project_directory = current_folder.parent.parent.parent
#Katalog z danymi surówymi
raw_data_folder = project_directory / 'Data' / 'surowka'
#Katalog z obrobionymi danymi
procesed_data_folder = project_directory / 'Data' / 'processed'

