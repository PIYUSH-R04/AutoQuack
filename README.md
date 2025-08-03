<!-- <p align="center">
  <img src="assets/logo-autoquack-light.png" alt="AutoQuack Logo" width="200"/>
</p> -->

<h1 align="center">AutoQuack</h1>
<p align="center"><i>Automated Payload Generator & Rubber Ducky Script Builder</i></p>

<br/>

<pre align="center"><code>                                                                                                                                                                        
                                                                                                                                                                                   
               AAA                                     tttt                                QQQQQQQQQ                                                            kkkkkkkk           
              A:::A                                 ttt:::t                              QQ:::::::::QQ                                                          k::::::k           
             A:::::A                                t:::::t                            QQ:::::::::::::QQ                                                        k::::::k           
            A:::::::A                               t:::::t                           Q:::::::QQQ:::::::Q                                                       k::::::k           
           A:::::::::A        uuuuuu    uuuuuuttttttt:::::ttttttt       ooooooooooo   Q::::::O   Q::::::Quuuuuu    uuuuuu    aaaaaaaaaaaaa      cccccccccccccccc k:::::k    kkkkkkk
          A:::::A:::::A       u::::u    u::::ut:::::::::::::::::t     oo:::::::::::oo Q:::::O     Q:::::Qu::::u    u::::u    a::::::::::::a   cc:::::::::::::::c k:::::k   k:::::k 
         A:::::A A:::::A      u::::u    u::::ut:::::::::::::::::t    o:::::::::::::::oQ:::::O     Q:::::Qu::::u    u::::u    aaaaaaaaa:::::a c:::::::::::::::::c k:::::k  k:::::k  
        A:::::A   A:::::A     u::::u    u::::utttttt:::::::tttttt    o:::::ooooo:::::oQ:::::O     Q:::::Qu::::u    u::::u             a::::ac:::::::cccccc:::::c k:::::k k:::::k   
       A:::::A     A:::::A    u::::u    u::::u      t:::::t          o::::o     o::::oQ:::::O     Q:::::Qu::::u    u::::u      aaaaaaa:::::ac::::::c     ccccccc k::::::k:::::k    
      A:::::AAAAAAAAA:::::A   u::::u    u::::u      t:::::t          o::::o     o::::oQ:::::O     Q:::::Qu::::u    u::::u    aa::::::::::::ac:::::c              k:::::::::::k     
     A:::::::::::::::::::::A  u::::u    u::::u      t:::::t          o::::o     o::::oQ:::::O  QQQQ:::::Qu::::u    u::::u   a::::aaaa::::::ac:::::c              k:::::::::::k     
    A:::::AAAAAAAAAAAAA:::::A u:::::uuuu:::::u      t:::::t    tttttto::::o     o::::oQ::::::O Q::::::::Qu:::::uuuu:::::u  a::::a    a:::::ac::::::c     ccccccc k::::::k:::::k    
   A:::::A             A:::::Au:::::::::::::::uu    t::::::tttt:::::to:::::ooooo:::::oQ:::::::QQ::::::::Qu:::::::::::::::uua::::a    a:::::ac:::::::cccccc:::::ck::::::k k:::::k   
  A:::::A               A:::::Au:::::::::::::::u    tt::::::::::::::to:::::::::::::::o QQ::::::::::::::Q  u:::::::::::::::ua:::::aaaa::::::a c:::::::::::::::::ck::::::k  k:::::k  
 A:::::A                 A:::::Auu::::::::uu:::u      tt:::::::::::tt oo:::::::::::oo    QQ:::::::::::Q    uu::::::::uu:::u a::::::::::aa:::a cc:::::::::::::::ck::::::k   k:::::k 
AAAAAAA                   AAAAAAA uuuuuuuu  uuuu        ttttttttttt     ooooooooooo        QQQQQQQQ::::QQ    uuuuuuuu  uuuu  aaaaaaaaaa  aaaa   cccccccccccccccckkkkkkkk    kkkkkkk
                                                                                                   Q:::::Q                                                                         
                                                                                                    QQQQQQ                                                                                                                                                                                                                                                
</code></pre>

---

# AutoQuack

**AutoQuack** is a desktop application that implements user-driven OS interaction recording, dynamic PowerShell payload generation, and Rubber Ducky script construction for crafting and exporting simulated attack scripts/payloads in both `.ps1` and `.ducky` formats.

---

## 🔧 Installation

### Requirements

* Python 3.9+
* Windows OS (for native simulation features)
* Recommended: Run inside a virtual environment

### Setup Steps

```bash
# Clone the repository
https://github.com/PIYUSH-R04/AutoQuack.git
cd AutoQuack

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

---

## 🧩 Features

### 🖱️ Action Recorder

* Capture real-time user actions: keyboard strokes and shell commands.
* Translate captured actions into structured PowerShell or Ducky-compatible syntax.

### 🧠 Payload Generator

* Configure, generate and combine different payloads:

  * **UAC Bypass**
  * **Disable Windows Defender**
  * **Disable Firewall**
  * **System Reconnaissance**
  * **Credential Dumping (SAM/LSASS/NTDS)**
  * **Persistence Setup (Startup scripts)**
  * **Reverse Shells**
  * **Custom MSFvenom Shellcode Injection**

### 📦 Obfuscation Engine

* Support for multiple script obfuscation strategies:

  * `Base64` (UTF-16LE encoded PowerShell)
  * `SplitConcat` (line-split + `Invoke-Expression`)
  * `ASTInject` (simulated randomized variables)
  * `TokenSwap` (PowerShell command token mangling)

### 🕸 Reverse Shell Options

* PowerShell TCP Reverse Shell
* PowerShell HTTP Reverse Shell
* Netcat-compatible output
* Configurable LHOST / LPORT per session

### 🧑‍💻 Manual + Sidebar Scripting

* Switch between structured form-based configuration and full manual script editing.
* Automatically disable conflicting sidebar inputs during manual edit mode.
* Reapply sidebar changes if manual editing is disabled.

### 🖥️ Dual Output Format

* Output both PowerShell (`.ps1`) and Rubber Ducky (`.ducky`) scripts.
* Toggle between script views.

---

## 📘 User Guide

### Step 1: Launch

Run the app using:

```bash
python main.py
```

### Step 2: Configure Payloads

Use the left sidebar to:

* Enable specific payloads
* Configure parameters (file paths, booleans, shell types, etc.)
* Choose obfuscation method and execution delay

### Step 3: Record Actions (Optional)

Click **"Simulate Actions"** to launch the floating recorder window:

* Perform desired keystrokes or application actions (via keystrokes).
* When finished, click **Stop Recording**.

### Step 4: Preview Script

In the right editor:

* View the generated script
* Toggle between `.ps1` and `.ducky` formats
* Enable manual edit mode if needed

### Step 5: Save Script

Click **"Save Script"** to export both formats.

---

## 📸 Screenshot

![screenshot1](assets/view-ps1.png)
![screenshot2](assets/view-ducky.png)
---

## 📄 License

This project is licensed under the **MIT License**. See `LICENSE` file for full details.

---

## ⚠ Disclaimer

* AutoQuack is intended strictly for educational and authorized testing environments.
* Misuse of this tool may violate local or international laws.
* The author is not responsible for any misuse or damage caused.

---

## 👤 Author

Developed by \Piyush R.

---

## 📬 Contributions

Pull requests are welcome. Please ensure code is clean, well-documented, and consistent with the project architecture.
