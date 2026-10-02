"""Local extractive evidence service. Run: python serve.py --port 8765.

Demo keys map to tenants in trusted server code. They are not production
credentials. Binds only to loopback; no model calls or external writes.
"""

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from labs import search

DEMO_KEYS = {"study-demo-key": "study", "private-demo-key": "private"}


class Handler(BaseHTTPRequestHandler):
    def respond(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            return self.respond(
                200, {"status": "ok", "mode": "extractive_demo"}
            )
        self.respond(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/ask":
            return self.respond(404, {"error": "not found"})
        tenant = DEMO_KEYS.get(self.headers.get("X-Demo-Key", ""))
        if tenant is None:
            return self.respond(401, {"error": "demo key required"})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 4096:
                raise ValueError("request size")
            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict) or set(payload) != {"query"}:
                raise ValueError("only query is accepted")
            query = payload["query"]
            if (
                not isinstance(query, str)
                or not 1 <= len(query.strip()) <= 500
            ):
                raise ValueError("query length/type")
        except (ValueError, json.JSONDecodeError):
            return self.respond(400, {"error": "invalid request"})
        hits = search(query, tenant)
        self.respond(
            200,
            {
                "mode": "extractive_demo",
                "status": "evidence_found" if hits else "no_evidence",
                "evidence": hits,
                "answer": hits[0]["text"] if hits else None,
            },
        )

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=8765)
    args = p.parse_args()
    print(
        f"Local evidence demo at http://127.0.0.1:{args.port}", flush=True
    )
    ThreadingHTTPServer(("127.0.0.1", args.port), Handler).serve_forever()
