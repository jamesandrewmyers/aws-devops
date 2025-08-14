#!/usr/bin/env python3
# scripts/decode_jwt.py
# Usage: python3 scripts/decode_jwt.py /path/to/token.jwt
import sys, json, base64

def decode_payload(token):
    parts = token.split('.')
    if len(parts) < 2:
        raise SystemExit("token format unexpected")
    b = parts[1]
    # base64url -> base64
    b += '=' * (-len(b) % 4)
    try:
        data = base64.urlsafe_b64decode(b)
        return json.loads(data)
    except Exception as e:
        raise SystemExit(f"decode failed: {e}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: decode_jwt.py /tmp/id_token.jwt", file=sys.stderr); sys.exit(2)
    p = sys.argv[1]
    with open(p, 'r') as f:
        token = f.read().strip()
    payload = decode_payload(token)
    print(json.dumps(payload, indent=2))
