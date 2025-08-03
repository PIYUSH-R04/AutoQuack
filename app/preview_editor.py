from PySide6.QtWidgets import (
    QWidget, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFileDialog, QMessageBox, QCheckBox
)
from PySide6.QtCore import Signal
from core.script_gen import build_script
from core.ducky_builder import build_ducky_script

class PreviewEditor(QWidget):
    manual_edit_toggled = Signal(bool)

    def __init__(self, actions, payloads, obfuscation_method, delay_seconds):
        super().__init__()
        self.actions = actions
        self.payloads = payloads
        self.obfuscation_method = obfuscation_method
        self.delay_seconds = delay_seconds

        self.manual_edit_enabled = False

        self.setWindowTitle("📝 Script Preview")
        self.setMinimumSize(900, 600)

        self.script_editor = QTextEdit()
        self.ducky_editor = QTextEdit()
        self.script_editor.setReadOnly(True)
        self.ducky_editor.setReadOnly(True)
        self.ducky_editor.hide()

        self.toggle_button = QPushButton("View: .ps1")
        self.toggle_button.clicked.connect(self.toggle_view)

        self.save_button = QPushButton("💾 Save Script")
        self.save_button.clicked.connect(self.save_script_prompt)

        self.edit_checkbox = QCheckBox("✏ Enable Manual Edit")
        self.edit_checkbox.stateChanged.connect(self.toggle_edit_mode)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Preview of generated script:"))
        layout.addWidget(self.script_editor)
        layout.addWidget(self.ducky_editor)

        controls = QHBoxLayout()
        controls.addWidget(self.toggle_button)
        controls.addWidget(self.edit_checkbox)
        controls.addWidget(self.save_button)

        layout.addLayout(controls)
        self.setLayout(layout)

        self.update_script_view()

    def toggle_edit_mode(self):
        editing = self.edit_checkbox.isChecked()
        self.manual_edit_enabled = editing

        self.script_editor.setReadOnly(not editing)
        self.ducky_editor.setReadOnly(not editing)

        self.manual_edit_toggled.emit(not editing)

        if not editing:
            self.update_script_view()

    def update_script_view(self):
        ps1 = build_script(self.actions, self.payloads, self.obfuscation_method, self.delay_seconds)
        ducky = build_ducky_script(self.actions, self.payloads, self.obfuscation_method, self.delay_seconds)

        self.script_editor.setPlainText(ps1)
        self.ducky_editor.setPlainText(ducky)

    def toggle_view(self):
        if self.script_editor.isVisible():
            self.script_editor.hide()
            self.ducky_editor.show()
            self.toggle_button.setText("View: .ducky")
        else:
            self.ducky_editor.hide()
            self.script_editor.show()
            self.toggle_button.setText("View: .ps1")

    def save_script_prompt(self):
        ps1_path, _ = QFileDialog.getSaveFileName(
            self, "Save PowerShell Script", "", "PowerShell Script (*.ps1)"
        )
        if ps1_path:
            try:
                ps1_final = self.script_editor.toPlainText()
                ducky_final = self.ducky_editor.toPlainText()

                with open(ps1_path, "w", encoding="utf-8") as f:
                    f.write(ps1_final)

                ducky_path = ps1_path.rsplit(".", 1)[0] + ".ducky"
                with open(ducky_path, "w", encoding="utf-8") as f:
                    f.write(ducky_final)

                QMessageBox.information(self, "Success", f"Scripts saved:\n{ps1_path}\n{ducky_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save files: {e}")
