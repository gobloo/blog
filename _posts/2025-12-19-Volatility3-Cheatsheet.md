---
layout: post
title: Volatility3 CheatSheet
date: 18-12-2025
categories: [CheatSheet]
tag: [Blue Team, Memory Analysis, DFIR]
---

# Volatility 3 Complete Cheat Sheet - Full Plugin Details

## Installation & Setup

```bash
# Pip install
pip3 install volatility3

# Git clone (latest)
git clone https://github.com/volatilityfoundation/volatility3.git
cd volatility3
pip3 install -r requirements.txt

# Verify installation
vol --version
```


## Profile Detection (Always First!)

```bash
# Auto-detect OS/profile
vol -f memory.dmp imageinfo

# Windows-specific
vol -f memory.dmp windows.info

# Linux-specific  
vol -f memory.dmp linux.info

# macOS-specific
vol -f memory.dmp mac.info
```


## 🔍 **WINDOWS PLUGINS - COMPLETE REFERENCE**

### **1. Process Analysis**

```bash
# List all processes
vol -f mem.dmp windows.pslist

# Process tree (parent-child relationships)
vol -f mem.dmp windows.pstree

# Scan for hidden processes
vol -f mem.dmp windows.psscan

# Filter by PID
vol -f mem.dmp windows.pslist --pid 1234

# Filter by process name
vol -f mem.dmp windows.pslist --name "explorer.exe"

# Command line arguments
vol -f mem.dmp windows.cmdline --pid 1234

# Process environment variables
vol -f mem.dmp windows.environment --pid 1234

# Dump process memory
vol -f mem.dmp windows.memdump --pid 1234 --dump-dir ./dumps/
```


### **2. DLL \& Module Analysis**

```bash
# List DLLs for specific process
vol -f mem.dmp windows.dlllist --pid 1234

# List DLLs for all processes
vol -f mem.dmp windows.dlllist

# Dump specific DLL
vol -f mem.dmp windows.dlllist --pid 1234 --dump-dir ./dlls/
```


### **3. Memory Forensics**

```bash
# Detect code injection/malware
vol -f mem.dmp windows.malfind

# VAD (Virtual Address Descriptor) regions
vol -f mem.dmp windows.vadinfo --pid 1234

# Memory maps
vol -f mem.dmp windows.memmap --pid 1234

# Heap analysis
vol -f mem.dmp windows.heapscan --pid 1234
```


### **4. Network Analysis**

```bash
# Network connections (TCP/UDP)
vol -f mem.dmp windows.netscan

# Network sockets
vol -f mem.dmp windows.sockets

# Listening ports
vol -f mem.dmp windows.listeners

# Network statistics
vol -f mem.dmp windows.netstat
```


### **5. Handles \& Objects**

```bash
# Open handles for process
vol -f mem.dmp windows.handles --pid 1234

# Filter by handle type
vol -f mem.dmp windows.handles --pid 1234 --object-type Mutant

# Mutex scan
vol -f mem.dmp windows.mutant_scan

# Open files
vol -f mem.dmp windows.filescan --pid 1234
```


### **6. Credentials \& Secrets**

```bash
# SAM hashes
vol -f mem.dmp windows.hashdump

# LSA secrets
vol -f mem.dmp windows.lsadump

# Cached domain credentials
vol -f mem.dmp windows.cachedump

# DPAPI blobs
vol -f mem.dmp windows.dpapi
```


### **7. Registry Analysis**

```bash
# List registry hives
vol -f mem.dmp windows.registry.hivelist

# Dump specific registry key
vol -f mem.dmp windows.registry.printkey --key "Software\Microsoft\Windows\CurrentVersion\Run"

# Export registry hive
vol -f mem.dmp windows.registry.export --base "0x12345678" --dump-dir ./hives/

# Profile list (user SIDs)
vol -f mem.dmp windows.registry.printkey --key "Software\Microsoft\Windows NT\CurrentVersion\ProfileList"
```


### **8. File System**

```bash
# Dump files from memory
vol -f mem.dmp windows.dumpfiles --pid 1234 --dump-dir ./files/

# File scan (deleted/open files)
vol -f mem.dmp windows.filescan
```


## 🐧 **LINUX PLUGINS**

```bash
linux.pslist                # Process list
linux.pstree                # Process tree
linux.cmdline               # Command line
linux.netstat               # Network connections
linux.bash                  # Bash history
linux.lsof                  # Open files
linux.lsmod                 # Kernel modules
linux.elf_info              # ELF analysis
linux.mutant_scan           # Mutexes
linux.memmap                # Memory maps
linux.heap                  # Heap analysis
```


## 🍎 **macOS PLUGINS**

```bash
mac.pslist
mac.pstree
mac.cmdline
mac.netstat
mac.files
mac.launchd_info
```


## 📤 **DUMPING ARTIFACTS**

### Dump Process Memory

```bash
vol -f mem.dmp windows.memdump --pid 1234 --dump-dir ./processes/
```


### Dump All Processes

```bash
vol -f mem.dmp windows.pslist --dump-dir ./all_processes/
```


### Dump Specific DLL

```bash
vol -f mem.dmp windows.dlllist --pid 1234 --dump-dir ./dlls/
```


### Dump Registry Hive

```bash
vol -f mem.dmp windows.registry.export --base "0x12345678" --dump-dir ./registry/
```


## 🎛️ **OUTPUT FORMATS**

```bash
# JSON
vol -f mem.dmp windows.pslist --output json --output-file pslist.json

# CSV
vol -f mem.dmp windows.pslist --output csv --output-file pslist.csv

# Table (default)
vol -f mem.dmp windows.pslist --output table
```


## 🔍 **FILTERING OPTIONS**

```bash
# By PID
--pid 1234

# By process name
--name "lsass.exe"

# By parent PID
--ppid 456

# By object type (handles)
--object-type Mutant

# Multiple filters
vol -f mem.dmp windows.handles --pid 1234 --object-type File
```


## 🚀 **QUICK REFERENCE COMMANDS**

| **Task** | **Command** |
| :-- | :-- |
| Auto-detect profile | `vol -f mem.dmp imageinfo` |
| Process list | `windows.pslist` |
| Network connections | `windows.netscan` |
| Dump LSASS | `windows.memdump --pid <lsass_pid>` |
| Hashdump | `windows.hashdump` |
| Command history | `windows.cmdscan` |
| Injected code | `windows.malfind` |
| Registry hives | `windows.registry.hivelist` |
| Dump all processes | `windows.pslist --dump-dir ./` |

## 💡 **PRO TIPS**

1. **Always run `imageinfo` first** to get correct profile
2. **Use `--dump-dir`** to save all artifacts automatically
3. **Combine filters**: `--pid 1234 --name lsass.exe`
4. **Pipe output**: `vol ... | grep -i suspicious`
5. **JSON for scripting**: `--output json`
6. **LSASS analysis flow**:

```
windows.pslist --name lsass.exe
windows.memdump --pid <lsass_pid>
windows.handles --pid <lsass_pid> --object-type Key
```


## 🛠️ **COMMON WORKFLOWS**

### Malware Investigation

```bash
vol -f mem.dmp imageinfo
vol -f mem.dmp windows.pslist
vol -f mem.dmp windows.malfind
vol -f mem.dmp windows.netscan
vol -f mem.dmp windows.cmdscan
```


### Credential Harvesting

```bash
vol -f mem.dmp windows.hashdump
vol -f mem.dmp windows.lsadump
vol -f mem.dmp windows.cachedump
vol -f mem.dmp windows.registry.printkey --key "Software\Microsoft\Windows\CurrentVersion\Run"
```

**Replace `mem.dmp` with your memory dump filename!**


