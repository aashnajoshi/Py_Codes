import pyttsx3
import PyPDF2
import easygui
from pathlib import Path
from tqdm import tqdm

book_path = easygui.fileopenbox(
    title="Select PDF File", filetypes=[["*.pdf", "PDF files"]]
)
if book_path is None:
    exit()

book_title = Path(book_path).stem

read = PyPDF2.PdfReader(open(book_path, "rb"))
conv = pyttsx3.init()

full_text = ""
total_pages = len(read.pages)

with tqdm(total=total_pages, desc="Converting pages") as pbar:
    for page_num in range(total_pages):
        text = read.pages[page_num].extract_text()
        clean_text = text.strip().replace("\n", " ")
        full_text += clean_text
        pbar.update(1)

audio_file_name = f"{book_title}_audio.mp3"
conv.save_to_file(full_text, audio_file_name)
conv.runAndWait()
print("Converted Successfully")
