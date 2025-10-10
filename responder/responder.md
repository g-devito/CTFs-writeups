# 1. Overview
**Target:** `unika.htb`  
**Difficulty:** Very Easy  
**Skills:** RFI, responder, ntlm-relay, winrm  
**Services observed:** Apache (HTTP) on 80/tcp, WinRM on 5985/tcp.  
**HTB Link:** https://app.hackthebox.com/starting-point  
**summary:** Capture NTLM via LLMNR/NetBIOS poisoning and RFI, crack hash via John The Ripper, relay to SMB/WinRM to obtain admin shell.

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
- Listening for LLMNR/NetBIOS name resolution requests, to capture NTLM challenge hash (username:MD4 hash of password).

---

## Initial Access
### Remote File Intrusion (RFI)
- [RFI command](./evidences/remote_file_intrusion.png)
- triggers the LLMNR/NetBIOS Name Resolution Request.  
- We get from responder the [NTLM hash](./evidences/hash.txt)

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
