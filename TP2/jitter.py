#!/usr/bin/env python3
"""
Implémentation d'un retry avec backoff exponentiel.
Pattern essentiel en systèmes distribués.
"""

import json
import time
import random
import urllib.request
import urllib.error


def fetch_with_retry(url, max_retries=4, base_delay=0.5, timeout=1.5):
    """
    Appelle `url` avec retry + backoff exponentiel.
    """

    for tentative in range(max_retries):
        try:
            print(f"🔄 Tentative {tentative + 1}/{max_retries}...")
            response = urllib.request.urlopen(url, timeout=timeout)
            data = json.loads(response.read().decode("utf-8"))
            print(f"✅ Succès à la tentative {tentative + 1}")
            return data

        except (urllib.error.URLError, urllib.error.HTTPError) as e:
            print(f"⚠️ Échec : {e}")

            if tentative < max_retries - 1:
                delay = base_delay * (2 ** tentative)
                jitter = random.uniform(0, delay * 0.3)
                wait = delay + jitter
                print(f"💤 Attente {wait:.2f}s avant retry...")
                time.sleep(wait)
            else:
                print("❌ Toutes les tentatives ont échoué.")
                return None


if __name__ == "__main__":
    print("📡 Appel avec retry + backoff exponentiel :")
    result = fetch_with_retry("http://127.0.0.1:8000/documents/2")

    if result:
        print(f"\n📄 Document récupéré : {result}")
    else:
        print("\n❌ Impossible de joindre le service.")