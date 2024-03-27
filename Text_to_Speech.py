import pyttsx3
import fitz
import easygui
from pathlib import Path
from tqdm import tqdm

def convert_pdf_to_audio():
    book_path = easygui.fileopenbox(title="Select PDF File", filetypes=[["*.pdf", "PDF files"]])
    if book_path is None:
        return
    book_title = Path(book_path).stem

    try:
        doc = fitz.open(book_path)
        total_pages = doc.page_count
        full_text = ""

        with tqdm(total=total_pages, desc="Converting pages") as pbar:
            for page_num in range(total_pages):
                page = doc.load_page(page_num)
                text = page.get_text()
                full_text += text
                pbar.update(1)

        if not full_text.strip():
            print("No text extracted from the PDF.")
            return

        audio_file_name = f"{book_title}_audio.mp3"
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)  # Speed of speech
        engine.setProperty("volume", 0.9)  # Volume (0.0 to 1.0)
        engine.save_to_file(full_text, audio_file_name)
        engine.runAndWait()
        print("Converted Successfully")

    except Exception as e:
        print("An error occurred:", e)
if __name__ == "__main__":
    convert_pdf_to_audio()