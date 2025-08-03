from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Signal, Qt

class FloatingControl(QWidget):
    recording_finished = Signal(list)

    def __init__(self, recorder):
        super().__init__()
        self.setWindowTitle("🎬 ShadowSim Recorder")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setFixedSize(200, 150)
        self.recorder = recorder

        layout = QVBoxLayout()
        self.start_btn = QPushButton("▶ Start Recording")
        self.stop_btn = QPushButton("⏹ Stop")
        self.cancel_btn = QPushButton("❌ Cancel")

        self.start_btn.clicked.connect(self.start_recording)
        self.stop_btn.clicked.connect(self.stop_recording)
        self.cancel_btn.clicked.connect(self.cancel_recording)

        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)
        layout.addWidget(self.cancel_btn)

        self.setLayout(layout)

    def start_recording(self):
        self.recorder.start()
        self.start_btn.setEnabled(False)

    def stop_recording(self):
        self.recorder.stop()
        self.recording_finished.emit(self.recorder.actions)
        self.close()

    def cancel_recording(self):
        self.recorder.stop()
        self.close()
