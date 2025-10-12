# Overview
**Difficulty:** Very Easy  
**Skills:** Server-Side Template Injection (SSTI), Template engine fingerprinting and payload crafting, Web proxy and payload delivery  
**HTB Link:** https://app.hackthebox.com/starting-point  
**Summary:** Exploited a Handlebars SSTI using process.mainModule.require to spawn a reverse shell, gain root, and capture the flag.  

---

# Steps

## 1. Reconnaissance
**port scan**
- [nmap scan](./evidences/nmap.txt)  
- `nmap -sV -sS 10.129.84.44 -oN nmap.txt`  
- tcpwrapped server on port `80/tcp`  
- ssh service on port `22/tcp`
  
**server-side template injection**  
- [injection result](./evidences/server-side_template_injection_output.png)
- tried a simple injection `{{7*7}}` and discovered the template engine is [handlebars](https://handlebarsjs.com)


---

## 2. Resource Development
**hacktrick exploit**
- [hacktricks link to exploit](https://book.hacktricks.wiki/en/pentesting-web/ssti-server-side-template-injection/index.html#handlebars-nodejs)
- [burpsuite payload](./evidences/burpsuite_payload.png)
- there's a problem with the exploit provided by hacktricks: the module require is not defined (since is not in global scope)

**fixed hacktrick exploit**
- [fixed burpsuite payload](./evidences/fixed_burpsuite_payload.png)
- changing require with process.mainModule.require

**listening socket for reverse shell**
- `nc -lvnp 9000`

---

## 3. Initial Access
- we run the reverse shell command through burpsuite
- [root access gained](./evidences/root_access.png)
- [retrieve the flat](./evidences/flag.png)

---

## 4. Privilege Escalation
