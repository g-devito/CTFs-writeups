# Overview
**Difficulty:** Very Easy  
**Skills:** FTP (anonymous access), Hydra (SSH brute-force), SSH tunneling, linpeas enumeration, PostgreSQL enumeration  
**HTB Link:** https://app.hackthebox.com/starting-point  
**Summary:** Gained user access by exploiting anonymous FTP and a default password (Hydra against SSH), tunneled to a localhost PostgreSQL instance and extracted the flag from the database    

---

# Steps

## 1. Reconnaissance
**port scan**
- [nmap scan](./evidences/nmap.txt)  
- `nmap -sV 10.129.228.195 -oN nmap.txt`  
- 21/tcp open  ftp     vsftpd 3.0.3
- 22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)

**ftp connection**
- [ftp anonymous access](./evidences/ftp_access.png)
- we connect to the ftp server in anonymous mode (no password required, read only)

**documentation analysis**
- we retrieve the [password policy doc](./evidences/password_policy.pdf)
- and notice that the dafult password is set to: funnel123#!#
- and also get the list of users via the emails of the receivers

---

## 2. Resource Development
- we create a [userlist file](./evidences/users.txt) to use with hydra

---

## 3. Initial Access
**brute force attack**
- [hydra attack](./evidences/hydra_attack.png)
- the hydra attack with list of users and default password get us a match

**ssh access**
- [user ssh connection](./evidences/user_ssh_access.png)

---

## 4. Privilege Escalation
**linpeas enumeration**
- we install linpeas to the target machine and run it
- we find a local socket listening on port 5432 (postgreSQL): [container](./evidences/linpeas.png)

**reverse tunneling**
- since the postgreSQL server is listening only on localhost and the user dont have the psql cmd, we do a tunneling to access it remotly
- `ssh -L 1234:localhots:5432 christine@$ip`
- now we can access the server from our host: [nmap of postgreSQL](./evidences/postgresql_nmap.png)

**postgresql**
- [postgresql access](./evidences/postgresql_access.png)
- we access the database using username and password of the user
- [postgresql enumeration](./evidences/postgresql_enumeration.png)
- enumerating the DB we find the database secrets, which have the table flag
