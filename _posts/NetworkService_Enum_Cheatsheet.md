# Network Services Windows Enumeration Cheatsheet

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

## Quick One-Liners

```powershell

# DNS Zone Transfer

dig @10.10.10.10 thm.com AXFR

# SMB Shares (Windows target)

net share

# SNMP Enum (AttackBox)

cd /opt/snmpcheck
./snmpcheck.rb 10.82.129.224 -c public

```

## Service Breakdown

### **DNS Enumeration**
```powershell

dig @DNSSERVER DOMAIN AXFR

```
**Goal:** Dump **all DNS records** (A, CNAME, MX, TXT) → Discover hidden hosts

### **SMB Enumeration**
```powershell

net share
Share name     Resource           Remark
----------------------------------------------------------------
C\$             C\$                 Default share
IPC\$           Remote IPC
ADMIN\$         C\$                 Remote Admin
Internal       C:\Files           Internal Documents
Users          C:\Users

```
**Goal:** Find **readable shares** → File access, credentials, configs

### **SNMP Enumeration**

**Reveals:** Device location, software versions, configs, users 

```bash
./snmpcheck-1.9.rb <IP>
# or we can use msfconsole
msf auxiliary(scanner/snmp/snmp_enum) 
```

## Pro Tips

| **Service** | **Default Creds** | **Pentest Value** |
|-------------|------------------|-------------------|
| **DNS** | Open resolver | Hidden subdomains/hosts |
| **SMB** | Guest/Null session | File shares, configs |
| **SNMP** | `public`/`private` | Physical locations, system info |

**Attack Chain:**
1. `nmap -sU -p161 TARGET` → Find SNMP
2. `snmpcheck TARGET -c public` → Extract info
3. `net share` → Access files
4. `dig AXFR` → Map network



