import base64
import random

def apply_obfuscation(script_text, method, arch="64"):
    """
    Applies the selected obfuscation technique to the PowerShell script.
    
    Parameters:
        script_text (str): The raw PowerShell script.
        method (str): One of ["None", "Base64", "SplitConcat", "ASTInject", "TokenSwap"].

    Returns:
        str: Obfuscated PowerShell script ready for execution.
    """
    if method == "Base64":
        encoded = base64.b64encode(script_text.encode("utf-16le")).decode()
        powershell_cmd = r"C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe" if arch == "32" else "powershell"
        return f"{powershell_cmd} -EncodedCommand {encoded}"

    elif method == "SplitConcat":
        lines = script_text.splitlines()
        joined = ";\n".join([f'"{line}"' for line in lines if line.strip()])
        return f'$script = {joined}\nInvoke-Expression $script'

    elif method == "ASTInject":
        def random_var(length=8):
            return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=length))

        transformed = script_text
        seen_vars = set()
        for line in script_text.splitlines():
            tokens = line.strip().split()
            for tok in tokens:
                if tok.startswith('$') and len(tok) > 1 and tok[1:].isalnum():
                    seen_vars.add(tok)

        replacements = {var: f"${random_var()}" for var in seen_vars}
        for old, new in replacements.items():
            transformed = transformed.replace(old, new)
        
        return f"# AST-like randomized vars injected\n{transformed}"

    elif method == "TokenSwap":
        transformed = script_text.replace("powershell", "po`wer`shell")
        transformed = transformed.replace("Start-Process", "Sta`rt-Pro`cess")
        transformed = transformed.replace("Invoke-Expression", "Inv`oke-Expr`ession")
        return f"# Token-swapped PowerShell\n{transformed}"

    else:
        return script_text
