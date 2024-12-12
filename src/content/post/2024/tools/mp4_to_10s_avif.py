import os
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QFileDialog, QSpacerItem, QSizePolicy
from datetime import datetime

class VideoEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.main_video_path = None
        self.jdt_video_path = '/Users/macm2/Documents/vuepress/src/diary/2024/tools/jdt.mp4'
        self.set_config = 1
        self.trim_hour = '00'
        self.trim_minute = '00'
        self.trim_second = '00'
        self.crf = '24'
        self.output_file_name = None
        # 创建GUI元素
        self.btn_select_main = QPushButton('选择主视频', self)
        self.lbl_main_video = QLabel("主视频未选择!", self)
        self.btn_select_jdt = QPushButton('选择进度条视频', self)

        self.lbl_jdt_video = QLabel("进度条视频未选择!", self)
        if self.jdt_video_path:
            self.lbl_jdt_video.setText(f"已选择：{self.jdt_video_path}")
        self.set_config = QLabel("参数设置: ", self)
        self.lbl_trim_hour = QLabel("时: ", self)
        self.txt_trim_hour = QLineEdit(self)
        self.txt_trim_hour.setFixedWidth(60)
        self.txt_trim_hour.setPlaceholderText(f"时：{self.trim_hour}")
        self.lbl_trim_minute = QLabel("分: ", self)
        self.txt_trim_minute = QLineEdit(self)
        self.txt_trim_minute.setFixedWidth(60)
        self.txt_trim_minute.setPlaceholderText(f"分：{self.trim_minute}")
        self.lbl_trim_second = QLabel("秒: ", self)
        self.txt_trim_second = QLineEdit(self)
        self.txt_trim_second.setFixedWidth(60)
        self.txt_trim_second.setPlaceholderText(f"秒：{self.trim_second}")
        self.lbl_crf = QLabel("crf:", self)
        self.txt_crf = QLineEdit(self)
        self.txt_crf.setPlaceholderText("默认24（0-63, 越低质量越好）")
        self.lbl_output_name = QLabel("输出文件名:", self)        
        self.txt_output_name = QLineEdit(self)
        self.txt_output_name.setPlaceholderText("输入输出文件名（例如：output）")
        self.btn_process = QPushButton('处理视频', self)
        
        # 布局设置
        layout = QVBoxLayout()
        layout.addWidget(self.btn_select_main)
        layout.addWidget(self.lbl_main_video)
        layout.addWidget(self.btn_select_jdt)
        layout.addWidget(self.lbl_jdt_video)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(self.set_config)
        layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        time_layout = QHBoxLayout()
        time_layout.addWidget(self.lbl_trim_hour)
        time_layout.addWidget(self.txt_trim_hour)
        time_layout.addWidget(self.lbl_trim_minute)
        time_layout.addWidget(self.txt_trim_minute)
        time_layout.addWidget(self.lbl_trim_second)
        time_layout.addWidget(self.txt_trim_second)
        layout.addLayout(time_layout)
        crf_layout = QHBoxLayout()
        crf_layout.addWidget(self.lbl_crf)
        crf_layout.addWidget(self.txt_crf)
        layout.addLayout(crf_layout)
        output_name_layout = QHBoxLayout()
        output_name_layout.addWidget(self.lbl_output_name)
        output_name_layout.addWidget(self.txt_output_name)
        layout.addLayout(output_name_layout)
        layout.addWidget(self.btn_process)
        self.setLayout(layout)
        # 连接信号和槽函数
        self.btn_select_main.clicked.connect(self.select_main_video)
        self.btn_select_jdt.clicked.connect(self.select_jdt_video)
        self.btn_process.clicked.connect(self.process_videos)
    def select_main_video(self):
        file_dialog = QFileDialog()
        self.main_video_path, _ = file_dialog.getOpenFileName(self, '选择视频文件', '', 'Video Files (*.mp4 *.avi *.mov)')
        if self.main_video_path:
            self.lbl_main_video.setText(f"已选择：{self.main_video_path}")
    def select_jdt_video(self):
        file_dialog = QFileDialog()
        self.jdt_video_path, _ = file_dialog.getOpenFileName(self, '选择进度条视频文件', '', 'Video Files (*.mp4 *.avi *.mov )')
        if self.jdt_video_path:
            self.lbl_jdt_video.setText(f"已选择：{self.jdt_video_path}")
    def process_videos(self):
        now = datetime.now()
        formatted_time = now.strftime("%m%d_%H%M")
        self.trim_hour = self.txt_trim_hour.text() or self.trim_hour
        self.trim_minute = self.txt_trim_minute.text() or self.trim_minute
        self.trim_second = self.txt_trim_second.text() or self.trim_second
        self.crf = self.txt_crf.text() or self.crf  
        self.output_file_name = self.txt_output_name.text() or formatted_time
        if not (self.main_video_path and self.jdt_video_path and self.trim_hour     and self.trim_minute and self.trim_second and self.crf and self.output_file_name):
            print("请确保所有字段都已填写")
            return
        output_dir = os.path.dirname(self.main_video_path)
        main_video_trimmed = os.path.join(output_dir, "main_video.mp4")
        # 构建时间字符串
        trim_time = f"{self.trim_hour}:{self.trim_minute}:{self.trim_second}"
        # 获取视频分辨率
        probe_cmd = ["ffprobe", "-v", "error", "-select_streams", "v:0",    "-show_entries", "stream=width,height", "-of", "csv=p=0", self.    main_video_path]
        probe_result = subprocess.check_output(probe_cmd).decode('utf-8').strip().  split(',')
        video_width, video_height = map(int, probe_result)
        # 根据视频分辨率调整裁剪命令
        if video_width != 1920 or video_height != 1080:
            trim_cmd = [
                "ffmpeg",
                "-ss", trim_time,
                "-i", self.main_video_path,
                "-t", "10",
                "-vf", "scale=1920:1080",
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "12",
                "-c:a", "copy",
                main_video_trimmed
            ]
        else:
            trim_cmd = [
                "ffmpeg",
                "-ss", trim_time,
                "-i", self.main_video_path,
                "-t", "10",
                "-c", "copy",
                main_video_trimmed
            ]
        subprocess.run(trim_cmd)
        # 合并两个视频
        merge_cmd = [
            "ffmpeg",
            "-i", main_video_trimmed,
            "-i", self.jdt_video_path,
            "-filter_complex",
            "[1:v] crop=in_w:10:0:1080-10 [jdt];"
            "[jdt] setpts=PTS-STARTPTS [jdt_sync];"
            "[0:v][jdt_sync] overlay=(W-w)/2:H-h [outv]",
            "-map", "[outv]",
            "-map", "0:a",
            "-c:v", "libsvtav1",
            "-crf", self.crf,
            "-pix_fmt", "yuv420p",
            "-an",
            "-f", "avif",
            os.path.join(output_dir, f"{self.output_file_name}.avif")
        ]
        subprocess.run(merge_cmd)
        # 删除临时文件
        try:
            os.remove(main_video_trimmed)
        except OSError as e:
            print(f"删除文件时出现错误: {e}")
        print("视频处理完成")
if __name__ == '__main__':
    app = QApplication([])
    editor = VideoEditor()
    editor.show()
    app.exec_()