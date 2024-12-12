import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QMessageBox, QVBoxLayout
import subprocess
import os

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'MP4 to AVIF Converter & Torrent Creator'
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        
        layout = QVBoxLayout()
        
        # MP4 to AVIF Converter
        self.converter_button = QPushButton('选择avi编码的.mp4文件', self)
        self.converter_button.clicked.connect(self.convert_to_avif)
        layout.addWidget(self.converter_button)
        
        # Transmission Torrent Creator
        self.torrent_button = QPushButton('选择文件或目录生成.torrent', self)
        self.torrent_button.clicked.connect(self.create_torrent)
        layout.addWidget(self.torrent_button)

        self.setLayout(layout)
        
        self.setGeometry(100, 100, 400, 150)
        self.show()
        
    def convert_to_avif(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        input_files, _ = QFileDialog.getOpenFileNames(self, "选择多个文件", "", "MP4 Files (*.mp4);;All Files (*)", options=options)
        if input_files:
            success_files = []
            failed_files = []
            skipped_files = []
            
            for input_file in input_files:
                input_path, input_filename = os.path.split(input_file)
                output_filename = os.path.splitext(input_filename)[0] + '.avif'
                output_file = os.path.join(input_path, output_filename)
                
                # 检查是否已经存在目标文件
                if os.path.exists(output_file):
                    skipped_files.append(output_file)
                    continue
                
                # 调用ffmpeg命令
                command = ["ffmpeg", "-i", input_file, "-c", "copy", "-f", "avif", output_file]
                try:
                    subprocess.run(command, check=True)
                    success_files.append(output_file)
                except subprocess.CalledProcessError as e:
                    failed_files.append((input_filename, str(e)))
            
            # 汇总报告
            report = "转换完成。\n\n"
            if success_files:
                report += "成功文件:\n" + "\n".join(success_files) + "\n\n"
            if failed_files:
                report += "失败文件:\n" + "\n".join([f"{file}: {error}" for file, error in failed_files]) + "\n\n"
            if skipped_files:
                report += "跳过文件（已存在）:\n" + "\n".join(skipped_files) + "\n\n"
            
            QMessageBox.information(self, "汇总报告", report)

    def create_torrent(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        input_items, _ = QFileDialog.getOpenFileNames(self, "选择文件或目录", "", "All Files (*)", options=options)
        if input_items:
            success_items = []
            failed_items = []
            comment = "sanqiz"
            
            for input_item in input_items:
                input_path, input_name = os.path.split(input_item)
                output_file = os.path.join(input_path, input_name + '.torrent')
                
                # 调用transmission-create命令
                command = ["transmission-create", "-o", output_file, "-c", comment, "-t", "www.baidu.com", input_item]
                try:
                    subprocess.run(command, check=True)
                    success_items.append(output_file)
                except subprocess.CalledProcessError as e:
                    failed_items.append((input_name, str(e)))
            
            # 汇总报告
            report = "Torrent 文件创建完成。\n\n"
            if success_items:
                report += "成功创建:\n" + "\n".join(success_items) + "\n\n"
            if failed_items:
                report += "失败创建:\n" + "\n".join([f"{item}: {error}" for item, error in failed_items]) + "\n\n"
            
            QMessageBox.information(self, "汇总报告", report)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
