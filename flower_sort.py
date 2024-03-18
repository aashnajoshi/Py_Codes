import cv2
import os
import shutil
import concurrent.futures
from pathlib import Path

def is_image_clear(image_path, threshold=100):
    image = cv2.imread(str(image_path))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F).var()
    return laplacian > threshold

def find_single_flower(image_path):
    image = cv2.imread(str(image_path))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 1:
        return True
    else:
        return False

def select_clear_images(folder_path, num_images):
    clear_images = []
    image_paths = [file for file in Path(folder_path).glob('*.jpg') if file.is_file() or file.suffix in ['.jpeg', '.png', '.bmp']]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = {executor.submit(is_image_clear, path): path for path in image_paths}
        for future in concurrent.futures.as_completed(futures):
            path = futures[future]
            if future.result():
                if find_single_flower(path):
                    clear_images.append(path)
                if len(clear_images) == num_images:
                    break
    return clear_images

def rename_files(folder_path):
    files = sorted(Path(folder_path).iterdir(), key=os.path.getmtime)
    for i, file in enumerate(files):
        if file.is_file():
            new_filename = f"{str(i+1).zfill(2)}{file.suffix}"
            file.rename(file.with_name(new_filename))

def main():
    print("Select an operation:")
    print("1. Select clear images with single flowers")
    print("2. Rename all files")
    
    operation = input("Enter your choice (1 or 2): ")
    folder_path = input("Enter the path to the folder containing images: ")

    if not os.path.exists(folder_path):
        print("Invalid folder path.")
        return

    if operation == "1":
        num_images = int(input("Enter the number of clear images with single flowers you want to select: "))
        clear_images = select_clear_images(folder_path, num_images)
        output_folder = input("Enter the path to the output folder to save clear images: ")

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        for image_path in clear_images:
            shutil.copy(str(image_path), output_folder)
        
        print(f"{len(clear_images)} clear images with single flowers saved in '{output_folder}'.")
        
    elif operation == "2":
        rename_files(folder_path)
        print("Files renamed successfully.")
        
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()