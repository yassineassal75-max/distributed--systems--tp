import time
import random
from client import api_request   # ✅ IMPORTANT : import du client


def request_with_retry(
    func,                       # fonction appelant l'API
    max_retries=4,              # nombre max de tentatives
    base_delay=1.0,             # délai initial (secondes)
    max_delay=30.0,             # délai maximum
    retryable_statuses=(500, 502, 503, 504)
):
    """
    Appelle func() avec retry + backoff exponentiel + jitter.

    func() doit retourner (status_code, response_body).
    """

    for attempt in range(max_retries + 1):

        status, body = func()

        # ── Succès → retourner immédiatement ──
        if status is not None and status < 500 and status != 429:
            return status, body

        # ── Gestion rate limit (429) ──
        if status == 429:
            wait = 30.0   # valeur simple (peut venir du serveur)
            print(f"  ⏳ Rate limited. Attente {wait}s…")
            time.sleep(wait)
            continue

        # ── Dernière tentative → abandon ──
        if attempt == max_retries:
            print(f"  💀 Abandon après {max_retries + 1} tentatives")
            return status, body

        # ── Calcul backoff exponentiel ──
        delay = min(base_delay * (2 ** attempt), max_delay)

        # ── Jitter (randomisation pour éviter surcharge serveur) ──
        jittered_delay = random.uniform(0, delay)

        print(
            f"  🔄 Tentative {attempt+1}/{max_retries} échouée "
            f"(status={status}). Retry dans {jittered_delay:.1f}s…"
        )

        time.sleep(jittered_delay)

    return status, body


# ── EXÉCUTION TEST ──
if __name__ == "__main__":

    BASE = "http://127.0.0.1:8080"
    TOKEN = "secret-token-abc123"

    # ── Test 1 : endpoint /health (GET) ──
    def call_health():
        return api_request(
            "GET",
            f"{BASE}/health",
            timeout=5
        )

    print("\n=== Test GET /health ===")
    status, body = request_with_retry(call_health)
    print(f"Résultat final : {status} → {body}")

    # ── Test 2 : création document (POST) ──
    def call_create_doc():
        return api_request(
            "POST",
            f"{BASE}/documents",
            data={
                "title": "Doc avec retry",
                "content": "Test backoff"
            },
            token=TOKEN,
            timeout=5
        )

    print("\n=== Test POST /documents ===")
    status, body = request_with_retry(call_create_doc)
    print(f"Résultat final : {status} → {body}")