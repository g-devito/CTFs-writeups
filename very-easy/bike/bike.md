# Overview
**Difficulty:** Very Easy  
**Skills:** server-side template injection, 
**HTB Link:** https://app.hackthebox.com/starting-point  
**Summary:** 

---

# Steps

## 1. Reconnaissance
**port scan**
- [nmap scan](./evidences/nmap.txt)  
- `nmap -sV -sS 10.129.84.44 -oN nmap.txt`  
- tcpwrapped server on port `80/tcp`  
- ssh service on port `22/tcp`
**server-side template injection**
- [injection input](./evidences/server-side_template_injection_input.png)
- [injection output](./evidences/server-side_template_injection_output.png)
- discovered the template engine [handlebars](https://handlebarsjs.com)

---

## 2. Resource Development
**exploit handlebars server-side template injection**
- [hacktricks link to exploit](https://book.hacktricks.wiki/en/pentesting-web/ssti-server-side-template-injection/index.html#handlebars-nodejs)
- [burpsuite payload](./evidences/burpsuite_payload.png)
- there's a problem with the exploit provided by hacktricks: the module require is not defined (since is not in global scope
- we have modify the script and go instead for: process.mainModule.require
- [fixed burpsuite payload](./evidences/fixed_burpsuite_payload.png)
- we start a listening socket for a reverse shell: nc -lvnp 9000

---

## 3. Initial Access
- we run the reverse shell command through burpsuite
- [we got inside as root](./root_access.png)
- [retrieve the flat](./flag.png)

---

## 4. Privilege Escalation
