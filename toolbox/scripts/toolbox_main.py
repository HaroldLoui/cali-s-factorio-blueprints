import sys

import winsound

import pyperclip

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap

from toolbox_ui.ui_main import Ui_MainWindow
from my_factorio_funcs import *


class MainWindow(QMainWindow):
	def __init__(self):
		__version__ = '0.0.1'
		
		super(MainWindow, self).__init__()
		
		# 使用生成的UI文件创建UI
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		
		self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)  # 禁用最大化按钮
		self.setWindowTitle("Cali's Factorio Toolbox" + " Ver" + __version__)  # 设置软件标题
		
		self.setFont(QFont("微软雅黑"))
		self.set_additional_css()  # 设置额外的css
		self.init_signals()  # 初始化信号
		
		# 变量
		self.image_file_path = ''
	
	def set_additional_css(self) -> None:
		"""设置额外的css"""
		additional_css = ''
		
		# additional_css += """
		# 	QMainWindow{
		# 		background-color: black;
		# 	}
		# """
		
		self.setStyleSheet(self.styleSheet() + additional_css)
	
	def init_signals(self) -> None:
		"""初始化信号"""
		# 显示屏
		self.ui.pushButton_screen_generate.clicked.connect(self.on_screen_generate_button_clicked)
		self.ui.pushButton_screen_copy.clicked.connect(self.on_screen_copy_button_clicked)
		# 图片
		self.ui.pushButton_image_select.clicked.connect(self.on_image_select_button_clicked)
		self.ui.pushButton_image_generate.clicked.connect(self.on_image_generate_button_clicked)
		self.ui.pushButton_image_copy.clicked.connect(self.on_image_copy_button_clicked)
	
	"""显示屏生成相关"""
	
	def on_screen_generate_button_clicked(self) -> None:
		"""生成显示屏蓝图按钮按下时触发"""
		
		# 检查像素总数是否合法
		pix_count = self.ui.spinBox_screen_width.value() * self.ui.spinBox_screen_height.value()
		if pix_count <= 0 or pix_count > 2985:
			QMessageBox.critical(self, "错误", "请确保像素数量在1~2985之间", QMessageBox.Ok)
			return
		
		# 将结果输出到右侧textEdit中
		wires_type_list = []
		if self.ui.checkBox_screen_red_wire.checkState():
			wires_type_list.append(1)
		if self.ui.checkBox_screen_green_wire.checkState():
			wires_type_list.append(2)
		
		bp = generate_screen_blueprint(
			self.ui.spinBox_screen_width.value(),
			self.ui.spinBox_screen_height.value(),
			wires_type_list,
			bool(self.ui.checkBox_screen_always_on.checkState())
		)
		
		self.ui.plainTextEdit_screen_output.setPlainText(bp)
	
	def on_screen_copy_button_clicked(self) -> None:
		"""复制显示屏蓝图按钮按下时触发"""
		
		pyperclip.copy(self.ui.plainTextEdit_screen_output.toPlainText())
		winsound.MessageBeep()
	
	"""图片蓝图生成相关"""
	
	def on_image_select_button_clicked(self) -> None:
		"""选择图片按钮按下时触发"""
		
		file_path, _ = QFileDialog.getOpenFileName(self, "选择图片文件", "", "Image Files (*.jpg *.jpeg *.png)")
		if file_path:
			self.image_file_path = file_path
			print(file_path)
		self.ui.label_image.setPixmap(QPixmap(file_path))
		self.ui.label_image.setScaledContents(True)
	
	def on_image_generate_button_clicked(self) -> None:
		"""生成图片蓝图按钮按下时触发"""
		if not self.image_file_path:
			QMessageBox.critical(self, "错误", "尚未选择图片", QMessageBox.Ok)
			return
		
		pix_count = self.ui.spinBox_image_width.value() * self.ui.spinBox_image_height.value()
		if pix_count <= 0 or pix_count > 2985:
			QMessageBox.critical(self, "错误", "请确保像素数量在1~2985之间", QMessageBox.Ok)
			return
		
		if self.image_file_path:
			self.ui.plainTextEdit_image_output.setPlainText(
				generate_image_blueprint(
					self.image_file_path,
					self.ui.spinBox_image_width.value(),
					self.ui.spinBox_image_height.value()
				)
			)
	
	def on_image_copy_button_clicked(self) -> None:
		"""复制图片蓝图按钮按下时触发"""
		
		pyperclip.copy(self.ui.plainTextEdit_image_output.toPlainText())
		winsound.MessageBeep()


if __name__ == '__main__':
	QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # 启用HD缩放
	
	app = QApplication(sys.argv)
	main_window = MainWindow()
	main_window.show()
	sys.exit(app.exec_())
