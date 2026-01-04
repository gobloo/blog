# Linux Enumeration Cheatsheet

## Quick Reference Table

| **Category** | **Command** | **Purpose** | **Key Options** |
|--------------|-------------|-------------|-----------------|
| **System Info** | `ls /etc/*-release` | Find OS version | `cat /etc/os-release` |
| | `hostname` | System hostname | - |
| | `cat /etc/passwd` | List all users | - |
| | `cat /etc/group` | List groups | - |
| | `sudo cat /etc/shadow` | Password hashes (root only) | - |
| | `ls -lh /var/mail` | User mail files | - |
| | `rpm -qa` | Installed packages (RPM) | `dpkg -l` (Debian) |
| **Users** | `who` | Currently logged in users | - |
| | `w` | Users + what they're doing | - |
| | `whoami` | Current user | - |
| | `id` | User/Group IDs | - |
| | `last` | Recent logins | - |
| | `sudo -l` | Sudo permissions | - |
| **Network** | `ip a` or `ip addr show` | IP addresses | `ip a s` (short) |
| | `cat /etc/resolv.conf` | DNS servers | - |
| | `sudo netstat -plt` | Listening TCP ports + PIDs | `-atupn` (all connections) |
| | `sudo lsof -i` | Open network connections | `lsof -i :25` (specific port) |
| **Processes** | `ps -ef` | All processes (full format) | `ps aux` (BSD style) |
| | `ps axjf` | Process tree | - |
| | `ps -ef \| grep <user>` | Filter by user/process | - |
| **Files/Dirs** | `ls -lh /usr/bin` | Installed binaries | `ls -lh /sbin` |
| | `find / -perm -4000 2>/dev/null` | SUID binaries | `find / -perm -u=s` |
