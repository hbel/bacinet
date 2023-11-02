
from fastapi import FastAPI
from fastapi.testclient import TestClient

from bacinet import BacinetMiddleware


app = FastAPI()


app.add_middleware(BacinetMiddleware)

@app.get("/ping", status_code=200)
async def ping() -> str:
    return "PING"

client = TestClient(app)

def test_ping():
    response = client.get("/ping") 
    assert response.status_code == 200
    headers = response.headers 
    assert headers["X-Frame-Options"] == "DENY"
    assert headers["X-Permitted-Cross-Domain-Policies"] == "none"
    assert headers["X-DNS-Prefetch-Control"] == "off"
    assert headers["Cross-Origin-Resource-Policy"] == "same-origin"
    assert headers["Cross-Origin-Opener-Policy"] == "same-origin"
    assert headers["Cross-Origin-Embedder-Policy"] == "require-corp"
    assert headers["Referrer-Policy"] == "no-referrer"
    assert headers["Strict-Transport-Security"] == "maxAge=15552000;includeSubDomains"
    assert headers["Content-Security-Policy"] == "default-src 'self';base-uri 'self';font-src 'self' https: data:;form-action 'self';frame-ancestors 'self';img-src 'self' data:;object-src 'none';script-src 'self';script-src-attr 'none';style-src 'self' https: 'unsafe-inline';upgrade-insecure-requests"

