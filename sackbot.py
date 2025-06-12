import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                           QProgressBar, QComboBox, QLineEdit, QMessageBox,
                           QStackedWidget, QScrollArea, QFrame, QSlider)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor
from auth import AuthManager
from video_engine import VideoEngine
import json

class VideoProcessThread(QThread):
    progress = pyqtSignal(int, int)
    finished = pyqtSignal(bool, str)

    def __init__(self, video_engine, job_params):
        super().__init__()
        self.video_engine = video_engine
        self.job_params = job_params

    def run(self):
        try:
            success = self.video_engine.export_video(
                progress_callback=lambda current, total: self.progress.emit(current, total),
                **self.job_params
            )
            self.finished.emit(success, self.job_params['output_path'])
        except Exception as e:
            self.finished.emit(False, str(e))

class LoginWidget(QWidget):
    login_success = pyqtSignal()

    def __init__(self, auth_manager):
        super().__init__()
        self.auth = auth_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Username input
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.username.setStyleSheet("padding: 8px;")
        
        # Password input
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setStyleSheet("padding: 8px;")
        
        # Login button
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.try_login)
        login_btn.setStyleSheet("padding: 10px;")
        
        # Register button
        register_btn = QPushButton("Register")
        register_btn.clicked.connect(self.try_register)
        register_btn.setStyleSheet("padding: 10px;")
        
        layout.addWidget(QLabel("Welcome to Sackbot"))
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(login_btn)
        layout.addWidget(register_btn)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)

    def try_login(self):
        success, msg = self.auth.login(self.username.text(), self.password.text())
        if success:
            self.login_success.emit()
        else:
            QMessageBox.warning(self, "Login Failed", msg)

    def try_register(self):
        success, msg = self.auth.register(self.username.text(), self.password.text())
        QMessageBox.information(self, "Registration", msg)

class MainWidget(QWidget):
    def __init__(self, auth_manager, video_engine):
        super().__init__()
        self.auth = auth_manager
        self.video = video_engine
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Input video selection
        input_layout = QHBoxLayout()
        self.input_path = QLineEdit()
        self.input_path.setPlaceholderText("Select input video...")
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_input)
        input_layout.addWidget(self.input_path)
        input_layout.addWidget(browse_btn)
        
        # Video settings
        settings_layout = QHBoxLayout()
        
        # Resolution dropdown
        self.resolution = QComboBox()
        self.resolution.addItems(['4K', '1440p', '1080p', '720p', '480p'])
        self.resolution.setCurrentText('1080p')
        
        # Format dropdown
        self.format = QComboBox()
        self.format.addItems(['mp4', 'avi'])
        
        # Effects dropdown
        self.effect = QComboBox()
        self.effect.addItems(['None', 'Grayscale', 'Invert'])
        
        # Brightness slider
        self.brightness = QSlider(Qt.Orientation.Horizontal)
        self.brightness.setRange(50, 150)
        self.brightness.setValue(100)
        brightness_label = QLabel("Brightness:")
        
        settings_layout.addWidget(QLabel("Resolution:"))
        settings_layout.addWidget(self.resolution)
        settings_layout.addWidget(QLabel("Format:"))
        settings_layout.addWidget(self.format)
        settings_layout.addWidget(QLabel("Effect:"))
        settings_layout.addWidget(self.effect)
        settings_layout.addWidget(brightness_label)
        settings_layout.addWidget(self.brightness)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setStyleSheet("QProgressBar { border: 2px solid grey; border-radius: 5px; text-align: center; } QProgressBar::chunk { background-color: #3add36; width: 1px; }")
        
        # Export button
        export_btn = QPushButton("Export Video")
        export_btn.clicked.connect(self.export_video)
        export_btn.setStyleSheet("padding: 12px; font-weight: bold;")
        
        # Batch processing button
        batch_btn = QPushButton("Batch Process")
        batch_btn.clicked.connect(self.batch_process)
        
        # Add all widgets to main layout
        layout.addLayout(input_layout)
        layout.addLayout(settings_layout)
        layout.addWidget(self.progress)
        layout.addWidget(export_btn)
        layout.addWidget(batch_btn)
        
        self.setLayout(layout)

    def browse_input(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Video File", "", "Video Files (*.mp4 *.avi *.mov *.mkv)"
        )
        if file_name:
            self.input_path.setText(file_name)

    def export_video(self):
        if not self.input_path.text():
            QMessageBox.warning(self, "Error", "Please select an input video file.")
            return

        output_path, _ = QFileDialog.getSaveFileName(
            self, "Save Video As", "", f"Video Files (*.{self.format.currentText()})"
        )
        
        if not output_path:
            return

        job_params = {
            'input_path': self.input_path.text(),
            'output_path': output_path,
            'resolution': self.resolution.currentText().lower(),
            'fmt': self.format.currentText(),
            'effect': self.effect.currentText().lower() if self.effect.currentText() != 'None' else None,
            'brightness': self.brightness.value() / 100
        }

        self.process_thread = VideoProcessThread(self.video, job_params)
        self.process_thread.progress.connect(self.update_progress)
        self.process_thread.finished.connect(self.export_finished)
        self.process_thread.start()

    def batch_process(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Batch Jobs File", "", "JSON Files (*.json)"
        )
        if file_name:
            try:
                self.video.batch_export_from_json(file_name)
                QMessageBox.information(self, "Success", "Batch processing completed!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Batch processing failed: {str(e)}")

    def update_progress(self, current, total):
        percent = (current / total) * 100 if total else 0
        self.progress.setValue(int(percent))

    def export_finished(self, success, result):
        if success:
            QMessageBox.information(self, "Success", f"Video exported successfully to {result}")
        else:
            QMessageBox.warning(self, "Error", f"Export failed: {result}")
        self.progress.setValue(0)

class SackbotApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.auth = AuthManager()
        self.video = VideoEngine()
        self.init_ui()
        self.set_dark_theme()

    def init_ui(self):
        self.setWindowTitle("Sackbot - Modern Video Creation Tool")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create stacked widget for login/main views
        self.stacked_widget = QStackedWidget()
        
        # Create and add login widget
        self.login_widget = LoginWidget(self.auth)
        self.login_widget.login_success.connect(self.show_main)
        self.stacked_widget.addWidget(self.login_widget)
        
        # Create and add main widget
        self.main_widget = MainWidget(self.auth, self.video)
        self.stacked_widget.addWidget(self.main_widget)
        
        self.setCentralWidget(self.stacked_widget)

    def show_main(self):
        self.stacked_widget.setCurrentWidget(self.main_widget)

    def set_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #181818;
                color: #ffffff;
            }
            QLineEdit, QComboBox, QPushButton {
                background-color: #242424;
                border: 1px solid #3a3a3a;
                border-radius: 4px;
                color: #ffffff;
                padding: 5px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #0078d4;
            }
            QPushButton:hover {
                background-color: #2a2a2a;
            }
            QPushButton:pressed {
                background-color: #1e1e1e;
            }
            QComboBox::drop-down {
                border: 0px;
            }
            QComboBox::down-arrow {
                image: none;
                border-width: 0px;
            }
            QProgressBar {
                text-align: center;
            }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application-wide font
    font = app.font()
    font.setFamily('Segoe UI')
    app.setFont(font)
    
    window = SackbotApp()
    window.show()
    
    sys.exit(app.exec())
