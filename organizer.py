import sys
import os
import shutil
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel, QMessageBox

# Default file type mapping
FILE_TYPES = {
    "Images": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
    "Documents": ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx'],
    "Videos": ['.mp4', '.avi', '.mkv', '.mov', '.wmv'],
    "Music": ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
    "Archives": ['.zip', '.rar', '.tar', '.gz', '.7z']}

class FileOrganizer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Organizer")
        self.resize(700, 200) 
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.label = QLabel("Select a directory to organize:")
        self.layout.addWidget(self.label)
        button_layout = QHBoxLayout()
        self.button_browse = QPushButton("Browse")
        self.button_browse.clicked.connect(self.browse_folder)
        button_layout.addWidget(self.button_browse)
        self.button_sort = QPushButton("Sort Files")
        self.button_sort.clicked.connect(self.sort_files)
        self.button_sort.setEnabled(False)
        button_layout.addWidget(self.button_sort)
        self.layout.addLayout(button_layout)
        self.target_directory = ""

    def browse_folder(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Folder")
        if directory:
            self.target_directory = directory
            self.label.setText(f"Selected Directory:\n{directory}")
            self.button_sort.setEnabled(True)

    def sort_files(self):
        if not self.target_directory:
            QMessageBox.warning(self, "No Directory", "Please select a directory first.")
            return

        for file in os.listdir(self.target_directory):
            file_path = os.path.join(self.target_directory, file)
            if os.path.isfile(file_path):
                file_ext = os.path.splitext(file)[1].lower()
                moved = False
                for category, extensions in FILE_TYPES.items():
                    if file_ext in extensions:
                        self.move_file(file_path, category)
                        moved = True
                        break
                if not moved:
                    self.move_file(file_path, "Others")
        QMessageBox.information(self, "Done", "Files have been sorted successfully!")

    def move_file(self, file_path, folder_name):
        folder_path = os.path.join(self.target_directory, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        shutil.move(file_path, os.path.join(folder_path, os.path.basename(file_path)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileOrganizer()
    window.show()
    sys.exit(app.exec_())
