from typing import Any


"""Standard options for the headers set by bacinet"""
options: dict[str, str | dict[str, Any]] = {
	"X-Frame-Options": "DENY", # DENY or SAMEORIGIN
	"X-Permitted-Cross-Domain-Policies": "none", # none, master-only, by-content-type, all
	"X-DNS-Prefetch-Control": "off", # on, off
	"Cross-Origin-Resource-Policy": "same-origin", # "same-origin", "same-site", "cross-origin"
	"Cross-Origin-Opener-Policy": "same-origin", # "same-origin", "same-origin-allow-popups", "unsafe-none"
	"Cross-Origin-Embedder-Policy": "require-corp", # "require-corp", "credentialless"
	"Referrer-Policy": "no-referrer", # "no-referrer", "no-referrer-when-downgrade", "same-origin", "origin", "strict-origin", "origin-when-cross-origin", "strict-origin-when-cross-origin", "unsafe-url", ""
	"Content-Security-Policy": {
		"default-src": ["'self'"],
		"base-uri": ["'self'"],
		"font-src": ["'self'", "https:", "data:"],
		"form-action": ["'self'"],
		"frame-ancestors": ["'self'"],
		"img-src": ["'self'", "data:"],
		"object-src": ["'none'"],
		"script-src": ["'self'"],
		"script-src-attr": ["'none'"],
		"style-src": ["'self'", "https:", "'unsafe-inline'"],
		"upgrade-insecure-requests": []
	},
	"Strict-Transport-Security": {
		"maxAge": 15552000,
		"includeSubDomains": True,
		"preload": False
	}
}
