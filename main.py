from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QMessageBox
from app.sidebar import Sidebar
from app.preview_editor import PreviewEditor
from app.recorder import ActionRecorder
from app.floating_control import FloatingControl
import sys

from payloads.defender_bypass import get_payload as get_defender_bypass
from payloads.reverse_shell import generate_shell
from payloads.uac_bypass import get_payload as get_uac_bypass
from payloads.firewall_disable import get_payload as get_firewall_disable
from payloads.recon import get_payload as get_recon
from payloads.cred_dump import get_payload as get_cred_dump
from payloads.persistence import get_payload as get_persistence

class ShadowSimMain(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AutoQuack — Automated Payload Generator")
        self.setMinimumSize(1200, 700)

        self.sidebar = Sidebar()
        self.editor = PreviewEditor([], {}, "None", 0)

        self.sidebar.payloads_updated.connect(self.on_payloads_changed)
        self.sidebar.simulate_requested.connect(self.start_recording)
        self.sidebar.save_requested.connect(self.editor.save_script_prompt)
        self.sidebar.about_requested.connect(self.show_about)
        self.editor.manual_edit_toggled.connect(self.on_manual_edit_toggled)

        layout = QHBoxLayout()
        layout.addWidget(self.sidebar, 2)
        layout.addWidget(self.editor, 6)
        self.setLayout(layout)

    def start_recording(self):
        self.recorder = ActionRecorder()
        self.float_control = FloatingControl(self.recorder)
        self.float_control.recording_finished.connect(self.on_recording_finished)
        self.float_control.show()

    def on_recording_finished(self, actions):
        print("[DEBUG] Actions received:", actions)
        for act in actions:
            print(act)
        self.editor.actions = actions
        self.editor.update_script_view()

    def on_payloads_changed(self, payload_dict, obf_method, delay_seconds):
        self._apply_payloads(payload_dict, obf_method, delay_seconds)

    def on_manual_edit_toggled(self, editing: bool):
        self.sidebar.set_enabled(not editing)
        if not editing:
            self.sidebar.update()

    def _apply_payloads(self, payload_dict, obf_method, delay_seconds):
        mapped = {}

        if "defender_bypass" in payload_dict:
            mapped["defender_bypass"] = lambda: get_defender_bypass(payload_dict["defender_bypass"])

        if "firewall_disable" in payload_dict:
            mapped["firewall_disable"] = get_firewall_disable

        if "uac_bypass" in payload_dict:
            mapped["uac_bypass"] = get_uac_bypass

        if "reverse_shell" in payload_dict:
            shell_config = payload_dict["reverse_shell"]
            if isinstance(shell_config, dict):
                mapped["reverse_shell"] = lambda: generate_shell(
                    shell_config.get("type", "PowerShell TCP"),
                    shell_config.get("ip", "127.0.0.1"),
                    shell_config.get("port", "4444")
                )
            else:
                print("[ERROR] reverse_shell payload malformed:", shell_config)

        if "recon" in payload_dict:
            recon_config = payload_dict["recon"]
            mapped["recon"] = lambda: get_recon(recon_config)

        if "cred_dump" in payload_dict:
            cred_config = payload_dict["cred_dump"]
            mapped["cred_dump"] = lambda: get_cred_dump(cred_config)

        if "persistence" in payload_dict:
            persist_config = payload_dict["persistence"]
            mapped["persistence"] = lambda: get_persistence(persist_config)

        if "msf_shellcode" in payload_dict:
            mapped["msf_shellcode"] = payload_dict["msf_shellcode"]

        self.editor.payloads = mapped
        self.editor.obfuscation_method = obf_method
        self.editor.delay_seconds = delay_seconds

        self.editor.update_script_view()

    def show_about(self):
        QMessageBox.information(self, "About / License",
            "AutoQuack - Automated Payload Generator\n\n"
            "Developed by: Piyush R.\n"
            "License: MIT\n\n"
            "This tool automatespayload generation and execution scripts.\n"
            "Use responsibly for educational or authorized testing only."
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShadowSimMain()
    window.show()
    sys.exit(app.exec())
