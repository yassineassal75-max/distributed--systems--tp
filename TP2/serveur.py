#!/usr/bin/env python3
"""
Mini serveur HTTP qui renvoie un document JSON.
Utilise uniquement la stdlib Python (http.server + json).
"""

import json
import time
import random
from http.server import HTTPServer, BaseHTTPRequestHandler

DOCUMENTS = {
    "1": {"id": 1, "titre": "Rapport Q3", "auteur": "Alice"},
    "2": {"id": 2, "titre": "Plan stratégique", "auteur": "Bob"},
    "3": {"id": 3, "titre": "Audit sécurité", "auteur": "Charlie"},
}


class DocumentHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        latence = random.uniform(0, 2.0)
        print(f"⏱ Latence simulée : {latence:.2f}s")
        time.sleep(latence)

        path = self.path.strip("/")
        parts = path.split("/")

        if parts[0] == "documents":
            if len(parts) == 1:
                self._send_json(200, list(DOCUMENTS.values()))
            elif len(parts) == 2 and parts[1] in DOCUMENTS:
                self._send_json(200, DOCUMENTS[parts[1]])
            else:
                self._send_json(404, {"error": "Document non trouvé"})
        else:
            self._send_json(404, {"error": "Route inconnue"})

    def _send_json(self, status_code, data):
        response = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)


if __name__ == "__main__":
    serveur = HTTPServer(("127.0.0.1", 8000), DocumentHandler)
    print("🚀 Serveur démarré sur http://127.0.0.1:8000")
    print("Essayez : /documents  ou  /documents/1")
    serveur.serve_forever()