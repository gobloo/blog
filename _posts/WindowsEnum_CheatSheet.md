# Windows Enumeration Cheatsheet

## Complete Windows Enumeration Commands

| **Category** | **Command** | **Purpose** | **Key Options** |
|--------------|-------------|-------------|-----------------|
| **System Info** | `systeminfo` | Full system details (OS, patches, hotfixes) | - |
| | `wmic qfe get Caption,Description` | Installed updates/patches | - |
| | `net start` | Currently running services | - |
| | `wmic product get name,version,vendor` | Installed applications | - |
| **Users** | `whoami` | Current user | - |
| | `whoami /priv` | Current user privileges | - |
| | `whoami /groups` | Current user groups | - |
| | `net user` | List all local users | - |
| | `net localgroup` | List local groups | `net group` (Domain Controller) |
| | `net localgroup administrators` | Members of Administrators group | - |
| | `net accounts` | Password policy settings | `net accounts /domain` (domain settings) |
| **Network** | `ipconfig` | Network configuration | `ipconfig /all` (full details) |
| | `netstat -abno` | Network connections + PIDs | `-a` (all), `-b` (binary), `-n` (numeric), `-o` (PID) |
| | `arp -a` | ARP cache (local network hosts) | - |

## One-Liners for Fast Enumeration

```powershell

REM Quick system overview
systeminfo | findstr /B /C:"OS Name" /C:"OS Version" /C:"Hotfix"
wmic qfe get Caption,Description

REM Users + Privileges
whoami /all
net user
net localgroup administrators

REM Network recon
ipconfig /all
netstat -abno | findstr LISTENING
arp -a

```

## Pro Tips

- **Run as Administrator** for full `netstat -b` and complete process info
- **Filter output**: `netstat -abno | findstr LISTENING`
- **`systeminfo` reveals**: OS version, patches, hotfixes, network cards
- **`whoami /all`** shows everything about current user (privs + groups)
- **`netstat -abno`** shows **exact binaries** listening on ports, then you can catch the pid and use `tasklist` to get the name of the process
- **ARP cache** reveals recent local network communication

## Example Outputs

```

C:\> netstat -abno | findstr LISTENING
TCP    0.0.0.0:22             0.0.0.0:0              LISTENING  2016  sshd.exe
TCP    0.0.0.0:135            0.0.0.0:0              LISTENING  924   RpcSs
TCP    0.0.0.0:445            0.0.0.0:0              LISTENING  4
TCP    0.0.0.0:3389           0.0.0.0:0              LISTENING  416   TermService

C:\> net localgroup administrators
Members
-------------------------------------------------------------------------------
Administrator          michael             peter               strategos

```


## Windows Network Services Enumeration

| **Service** | **Command** | **Purpose** | **Key Options/Notes** |
|-------------|-------------|-------------|----------------------|
| **DNS** | `dig @DNSSERVER DOMAIN AXFR` | DNS Zone Transfer | `-t AXFR` for full zone dump |
| | `nslookup` | DNS queries | `server DNSSERVER`<br>`ls -d DOMAIN` |
| **SMB** | `net share` | List shared folders | Run on Windows target |
| | `net view \\TARGET` | Remote shares | From attacking machine |
| | `smbclient -L \\\\TARGET` | List shares (Linux) | `-U username` |
| **SNMP** | `snmpcheck.rb TARGET -c public` | SNMP enumeration | AttackBox: `/opt/snmpcheck/` |
| | `snmpwalk -v2c -c public TARGET` | SNMP walk | OID: `1.3.6.1.2.1.1.6.0` (location) |


<div align="center">⁂</div>



