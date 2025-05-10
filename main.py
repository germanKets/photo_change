import os
from PIL import Image, ImageOps, ImageFilter
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QRadioButton, QHBoxLayout, QMessageBox, QGroupBox, QButtonGroup, QListWidget, QLineEdit, QTextEdit, QInputDialog, QFileDialog, QMessageBox

workdir = ''

class ImageProcessor():
    def __init__(self):
        self.filename = None
        self.image = None
        self.dir = None
        self.save_dir = 'Modified/'

    def loadImage(self, filename):
        self.filename = filename
        self.dir = workdir
        image_path = os.path.join(self.dir, self.filename)
        self.image = Image.open(image_path)

    def showImage(self, path):
        pixmapimage = QPixmap(path)
        label_width = picture.width()
        label_height = picture.height()
        scaled_pixmap = pixmapimage.scaled(label_width,
                                           label_height,
                                           Qt.KeepAspectRatio)
        picture.setPixmap(scaled_pixmap)
        picture.setVisible(True)

    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def do_bw(self):
        if file_list.selectedItems():
            self.image = ImageOps.grayscale(self.image)
            self.saveImage()
            image_path = os.path.join(
                self.dir, self.save_dir, self.filename
            )
            self.showImage(image_path)
        else:
            error_win = QMessageBox()
            error_win.setText('Выберите картинку для редактирования')
            error_win.exec()

    def do_left(self):
        if file_list.selectedItems():
            self.image = self.image.rotate(90)
            self.saveImage()
            image_path = os.path.join(
                self.dir, self.save_dir, self.filename
            )
            self.showImage(image_path)
        else:
            error_win = QMessageBox()
            error_win.setText('Выберите картинку для редактирования')
            error_win.exec()

    def do_right(self):
        if file_list.selectedItems():
            self.image = self.image.rotate(-90)
            self.saveImage()
            image_path = os.path.join(
                self.dir, self.save_dir, self.filename
            )
            self.showImage(image_path)
        else:
            error_win = QMessageBox()
            error_win.setText('Выберите картинку для редактирования')
            error_win.exec()

    def do_mirror(self):
        if file_list.selectedItems():
            self.image = ImageOps.mirror(self.image)
            self.saveImage()
            image_path = os.path.join(
                self.dir, self.save_dir, self.filename
            )
            self.showImage(image_path)
        else:
            error_win = QMessageBox()
            error_win.setText('Выберите картинку для редактирования')
            error_win.exec()

    def do_sharpen(self):
        if file_list.selectedItems():
            try:
                self.image = self.image.filter(ImageFilter.SHARPEN)
            except:
                error_win = QMessageBox
                error_win.setText('С такими не работаем, переделай')
                error_win.exec()
                
            self.saveImage()
            image_path = os.path.join(
                self.dir, self.save_dir, self.filename
            )
            self.showImage(image_path)
        else:
            error_win = QMessageBox()
            error_win.setText('Выберите картинку для редактирования')
            error_win.exec()


workimage = ImageProcessor()

def showChosenImage():
    if file_list.currentRow() >=0:
        filename = file_list.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(workimage.dir,
                                  filename)
        workimage.showImage(image_path)


def chooseWorkDir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
    result = []
    for filename in files:
        for extension in extensions:
            if filename.endswith(extension):
                result.append(filename)
    return result

def showFilenamesList():
    chooseWorkDir()
    extensions = ['.jpg', '.png', '.jpeg', '.gif']
    files = os.listdir(workdir)
    files = filter(files, extensions)
    file_list.clear()
    file_list.addItems(files)







#главное окно
app = QApplication([])
window = QWidget()
window.setWindowTitle('Easy Editor')
window.resize(700, 500)

#виджеты
btn1 = QPushButton('Лево')
btn2 = QPushButton('Право')
btn3 = QPushButton('Зеркало')
btn4 = QPushButton('Резкость')
btn5 = QPushButton('Ч/Б')
btn6 = QPushButton('Папка')
file_list = QListWidget()
picture = QLabel('картинка')

#лейауты
v_line1 = QVBoxLayout()
v_line2 = QVBoxLayout()
h_line1 = QHBoxLayout()
h_line2 = QHBoxLayout()

#подключение виджетов к лэйаутам
h_line2.addWidget(btn1)
h_line2.addWidget(btn2)
h_line2.addWidget(btn3)
h_line2.addWidget(btn4)
h_line2.addWidget(btn5)
v_line1.addWidget(btn6)
v_line1.addWidget(file_list)
v_line2.addWidget(picture)
v_line2.addLayout(h_line2)
h_line1.addLayout(v_line1)
h_line1.addLayout(v_line2)
window.setLayout(h_line1)


btn6.clicked.connect(showFilenamesList)
file_list.currentRowChanged.connect(showChosenImage)
btn5.clicked.connect(workimage.do_bw)
btn1.clicked.connect(workimage.do_left)
btn2.clicked.connect(workimage.do_right)
btn3.clicked.connect(workimage.do_mirror)
btn4.clicked.connect(workimage.do_sharpen)


window.show()
app.exec()