from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QCheckBox, QGroupBox, QComboBox, QLineEdit,
    QFormLayout, QSpinBox, QPushButton, QFileDialog, QScrollArea
)
from PySide6.QtCore import Signal, Qt

class Sidebar(QWidget):
    payloads_updated = Signal(dict, str, int)
    simulate_requested = Signal()
    save_requested = Signal()
    about_requested = Signal()

    def __init__(self):
        super().__init__()
        self.enabled_payloads = {}
        self.obfuscation = "None"
        self.delay_seconds = 0
        self.msf_file_path = None
        self.editing_enabled = False

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignTop)

        self.obf_dropdown = QComboBox()
        self.obf_dropdown.addItems(["None", "Base64", "SplitConcat", "ASTInject", "TokenSwap"])
        self.obf_dropdown.currentTextChanged.connect(self.update)
        layout.addWidget(QLabel("Obfuscation:"))
        layout.addWidget(self.obf_dropdown)

        self.reverse_shell_checkbox = QCheckBox("Enable Reverse Shell")
        self.reverse_shell_checkbox.stateChanged.connect(self.update)
        layout.addWidget(self.reverse_shell_checkbox)

        self.shell_group = QGroupBox("Reverse Shell Options")
        shell_form = QFormLayout()
        self.shell_type_dropdown = QComboBox()
        self.shell_type_dropdown.addItems(["PowerShell TCP", "PowerShell HTTP", "Netcat"])
        self.shell_type_dropdown.currentTextChanged.connect(self.update)
        self.ip_input = QLineEdit("127.0.0.1")
        self.ip_input.textChanged.connect(self.update)
        self.port_input = QLineEdit("4444")
        self.port_input.textChanged.connect(self.update)
        shell_form.addRow("Shell Type:", self.shell_type_dropdown)
        shell_form.addRow("LHOST (IP):", self.ip_input)
        shell_form.addRow("LPORT:", self.port_input)
        self.shell_group.setLayout(shell_form)
        layout.addWidget(self.shell_group)

        layout.addWidget(QLabel("Delay (s) between actions:"))
        self.delay_spin = QSpinBox()
        self.delay_spin.setRange(0, 10)
        self.delay_spin.valueChanged.connect(self.update)
        layout.addWidget(self.delay_spin)

        self.payload_checks = {}
        self.payload_fields = {}

        def add_payload(name, label, fields=None):
            checkbox = QCheckBox(label)
            checkbox.stateChanged.connect(self.update)
            layout.addWidget(checkbox)
            self.payload_checks[name] = checkbox

            if fields:
                group = QGroupBox()
                group.setVisible(False)
                form = QFormLayout()
                group.setLayout(form)
                self.payload_fields[name] = (group, {})

                for field_name, default, validator in fields:
                    input_field = QLineEdit(default)
                    input_field.textChanged.connect(self.update)
                    form.addRow(field_name + ":", input_field)
                    self.payload_fields[name][1][field_name] = (input_field, validator)

                layout.addWidget(group)

        add_payload("uac_bypass", "UAC Bypass")
        add_payload("defender_bypass", "Disable Windows Defender", [
            ("Exclusion Path", "C:\\Users\\Public", lambda v: v.startswith("C:"))
        ])
        add_payload("firewall_disable", "Disable Windows Firewall")
        add_payload("recon", "Recon (System Info, Wi-Fi, etc.)", [
            ("Output Directory", "C:\\Users\\Public", lambda v: v.startswith("C:"))
        ])
        add_payload("cred_dump", "Dump SAM/LSASS/NTDS", [
            ("Dump Path", "C:\\Users\\Public", lambda v: v.startswith("C:")),
            ("Use Procdump", "false", lambda v: v.lower() in ["true", "false"])
        ])
        add_payload("persistence", "Persistence (Startup)", [
            ("Script Path", "C:\\Users\\Public\\script.ps1", lambda v: v.endswith(".ps1"))
        ])
        add_payload("msf_shellcode", "Inject MSFvenom Payload")

        self.msf_upload_btn = QPushButton("📂 Upload MSFvenom Shellcode")
        self.msf_upload_btn.setVisible(False)
        self.msf_upload_btn.clicked.connect(self.open_msf_file_picker)
        layout.addWidget(self.msf_upload_btn)

        layout.addSpacing(20)
        simulate_btn = QPushButton("🎬 Simulate Actions")
        simulate_btn.clicked.connect(self.simulate_requested.emit)
        layout.addWidget(simulate_btn)

        save_btn = QPushButton("💾 Save Script")
        save_btn.clicked.connect(self.save_requested.emit)
        layout.addWidget(save_btn)

        about_btn = QPushButton("ℹ About / License")
        about_btn.clicked.connect(self.about_requested.emit)
        layout.addWidget(about_btn)

        scroll_area.setWidget(container)
        scroll_layout = QVBoxLayout(self)
        scroll_layout.addWidget(scroll_area)
        self.setLayout(scroll_layout)

    def open_msf_file_picker(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select MSFvenom Shellcode", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            self.msf_file_path = file_path
            self.update()

    def update(self):
        self.enabled_payloads = {}

        if self.reverse_shell_checkbox.isChecked():
            self.enabled_payloads['reverse_shell'] = {
                "type": self.shell_type_dropdown.currentText(),
                "ip": self.ip_input.text(),
                "port": self.port_input.text()
            }

        for key, cb in self.payload_checks.items():
            is_checked = cb.isChecked()

            if key in self.payload_fields:
                group, fields = self.payload_fields[key]
                group.setVisible(is_checked)

            if is_checked:
                if key == "msf_shellcode":
                    self.msf_upload_btn.setVisible(True)
                    if self.msf_file_path:
                        try:
                            with open(self.msf_file_path, "r", encoding="utf-8") as f:
                                content = f.read().strip()
                                if content:
                                    self.enabled_payloads[key] = content
                        except Exception as e:
                            print(f"[ERROR] MSF read failed: {e}")
                elif key in self.payload_fields:
                    _, fieldset = self.payload_fields[key]
                    values = {}
                    for field, (widget, validate) in fieldset.items():
                        val = widget.text().strip()
                        if not validate(val):
                            print(f"[WARN] Invalid input for {key}: {field}={val}")
                            continue
                        if val.lower() in ["true", "false"]:
                            values[field.lower().replace(" ", "_")] = val.lower() == "true"
                        else:
                            values[field.lower().replace(" ", "_")] = val
                    self.enabled_payloads[key] = values
                else:
                    self.enabled_payloads[key] = True
            else:
                if key == "msf_shellcode":
                    self.msf_upload_btn.setVisible(False)
                    self.msf_file_path = None

        self.obfuscation = self.obf_dropdown.currentText()
        self.delay_seconds = self.delay_spin.value()
        self.payloads_updated.emit(self.enabled_payloads, self.obfuscation, self.delay_seconds)

    def set_enabled(self, manual_edit_enabled: bool):
        is_enabled = not manual_edit_enabled

        for group, fieldset in self.payload_fields.values():
            for widget, _ in fieldset.values():
                widget.setEnabled(is_enabled)

        self.shell_type_dropdown.setEnabled(is_enabled)
        self.ip_input.setEnabled(is_enabled)
        self.port_input.setEnabled(is_enabled)
        self.delay_spin.setEnabled(is_enabled)
        self.obf_dropdown.setEnabled(is_enabled)
        self.msf_upload_btn.setEnabled(is_enabled and self.payload_checks["msf_shellcode"].isChecked())

