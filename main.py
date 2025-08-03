from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout,
    QMessageBox, QLabel
)
from PySide6.QtGui import QPixmap, QIcon
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

BANNER = r"""                                                                                                                                                                             
                                                                                                                                                                                   
               AAA                                     tttt                                QQQQQQQQQ                                                            kkkkkkkk           
              A:::A                                 ttt:::t                              QQ:::::::::QQ                                                          k::::::k           
             A:::::A                                t:::::t                            QQ:::::::::::::QQ                                                        k::::::k           
            A:::::::A                               t:::::t                           Q:::::::QQQ:::::::Q                                                       k::::::k           
           A:::::::::A        uuuuuu    uuuuuuttttttt:::::ttttttt       ooooooooooo   Q::::::O   Q::::::Quuuuuu    uuuuuu    aaaaaaaaaaaaa      cccccccccccccccc k:::::k    kkkkkkk
          A:::::A:::::A       u::::u    u::::ut:::::::::::::::::t     oo:::::::::::oo Q:::::O     Q:::::Qu::::u    u::::u    a::::::::::::a   cc:::::::::::::::c k:::::k   k:::::k 
         A:::::A A:::::A      u::::u    u::::ut:::::::::::::::::t    o:::::::::::::::oQ:::::O     Q:::::Qu::::u    u::::u    aaaaaaaaa:::::a c:::::::::::::::::c k:::::k  k:::::k  
        A:::::A   A:::::A     u::::u    u::::utttttt:::::::tttttt    o:::::ooooo:::::oQ:::::O     Q:::::Qu::::u    u::::u             a::::ac:::::::cccccc:::::c k:::::k k:::::k   
       A:::::A     A:::::A    u::::u    u::::u      t:::::t          o::::o     o::::oQ:::::O     Q:::::Qu::::u    u::::u      aaaaaaa:::::ac::::::c     ccccccc k::::::k:::::k    
      A:::::AAAAAAAAA:::::A   u::::u    u::::u      t:::::t          o::::o     o::::oQ:::::O     Q:::::Qu::::u    u::::u    aa::::::::::::ac:::::c              k:::::::::::k     
     A:::::::::::::::::::::A  u::::u    u::::u      t:::::t          o::::o     o::::oQ:::::O  QQQQ:::::Qu::::u    u::::u   a::::aaaa::::::ac:::::c              k:::::::::::k     
    A:::::AAAAAAAAAAAAA:::::A u:::::uuuu:::::u      t:::::t    tttttto::::o     o::::oQ::::::O Q::::::::Qu:::::uuuu:::::u  a::::a    a:::::ac::::::c     ccccccc k::::::k:::::k    
   A:::::A             A:::::Au:::::::::::::::uu    t::::::tttt:::::to:::::ooooo:::::oQ:::::::QQ::::::::Qu:::::::::::::::uua::::a    a:::::ac:::::::cccccc:::::ck::::::k k:::::k   
  A:::::A               A:::::Au:::::::::::::::u    tt::::::::::::::to:::::::::::::::o QQ::::::::::::::Q  u:::::::::::::::ua:::::aaaa::::::a c:::::::::::::::::ck::::::k  k:::::k  
 A:::::A                 A:::::Auu::::::::uu:::u      tt:::::::::::tt oo:::::::::::oo    QQ:::::::::::Q    uu::::::::uu:::u a::::::::::aa:::a cc:::::::::::::::ck::::::k   k:::::k 
AAAAAAA                   AAAAAAA uuuuuuuu  uuuu        ttttttttttt     ooooooooooo        QQQQQQQQ::::QQ    uuuuuuuu  uuuu  aaaaaaaaaa  aaaa   cccccccccccccccckkkkkkkk    kkkkkkk
                                                                                                   Q:::::Q                                                                         
                                                                                                    QQQQQQ                                                                                                                                                                                                                                                       
     AutoQuack - Automated Payload Generator
     Version 1.0.0 | Developed by Piyush R.
     https://github.com/PIYUSH-R04/AutoQuack.git
     License: MIT                                     
"""

print(BANNER)
class ShadowSimMain(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AutoQuack — Automated Payload Generator")
        self.setMinimumSize(1200, 700)

        from PySide6.QtGui import QIcon
        self.setWindowIcon(QIcon("assets/logo-autoquack-light.ico"))


        self.sidebar = Sidebar()
        self.editor = PreviewEditor([], {}, "None", 0)

        self.sidebar.payloads_updated.connect(self.on_payloads_changed)
        self.sidebar.simulate_requested.connect(self.start_recording)
        self.sidebar.save_requested.connect(self.editor.save_script_prompt)
        self.sidebar.about_requested.connect(self.show_about)
        self.editor.manual_edit_toggled.connect(self.on_manual_edit_toggled)

        main_layout = QVBoxLayout()

        content_layout = QHBoxLayout()
        content_layout.addWidget(self.sidebar, 2)
        content_layout.addWidget(self.editor, 6)

        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

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
            "This tool automates payload generation and execution scripts.\n"
            "Use responsibly for educational or authorized testing only."
        )


if __name__ == "__main__":
    from PySide6.QtCore import Qt
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("assets/logo-autoquack-light.png"))

    window = ShadowSimMain()
    window.setWindowIcon(QIcon("assets/logo-autoquack-light.png"))
    window.show()
    sys.exit(app.exec())

