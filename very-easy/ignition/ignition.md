# Overview
**Difficulty:** Very Easy  
**Skills:** port scanning, directory enumeration, password guessing  
**HTB Link:** https://app.hackthebox.com/starting-point  
**Summary:** nmap revealed nginx 1.14.2 on port 80 and gobuster uncovered a Magento /admin panel. Guessed a common Magento password

---

# Steps

## 1. reconnaissance
### port scan
- [nmap scan](./evidences/nmap.txt)
- nginx 1.14.2 web service on port 80/tcp
### directory traversal
- [gobuster traversal](./evidences/gobuster.txt)
- /admin page for magento

## 2. resource development

## 3. initial access
### password guessing
- magento have anti-bruteforce mechanisms so the only way was to guess the password
- searching for most used magento passwords for 2023 helps
- [root flag](./evidences/root_flag.png)

## 4. privilege escalation
