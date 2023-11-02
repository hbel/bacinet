
from typing import Any, cast
from fastapi import Response

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

class HeaderOptionError(Exception):
	def __init__(self, option: str, header_name: str) -> None:
		super().__init__(f"Unknown option {option} for {header_name} header")

def apply(response: Response) -> Response:
	strict_transport_security(response)
	content_security_policy(response)
	referrer_policy(response)
	cross_origin_embedder_policy(response)
	cross_origin_opener_policy(response)
	cross_origin_resource_policy(response)
	origin_agent_cluster(response)
	x_permitted_cross_domain_policies(response)
	x_frame_options(response)
	x_dns_prefetch_control(response)
	x_download_options(response)
	x_powered_by(response)
	x_xss_protection(response)
	x_content_type_options(response)
	return response;

def strict_transport_security(response: Response) -> Response:
	option: dict[str, Any] = cast(dict[str, Any], options["Strict-Transport-Security"])
	directives: list[str] = []
	for dir in option.keys():
		match dir:
			case "maxAge": directives.append(f"maxAge={option['maxAge']}")
			case "includeSubDomains" if option["includeSubDomains"] == True : directives.append("includeSubDomains")																		   
			case "preload" if option["preload"] == True : directives.append("preload")
			case _: raise HeaderOptionError(dir, "Strict-Transport-Security")
		directives.append(f"{dir} {' '.join(option[dir])}")
	response.headers["Strict-Transport-Security"] = ";".join(directives)
	return response

def content_security_policy(response: Response) -> Response:
	option: dict[str, list[str]] = cast(dict[str, list[str]], options["Content-Security-Policy"])
	directives: list[str] = []
	for dir in option.keys():
		directives.append(f"{dir} {' '.join(option[dir])}")
	response.headers["Content-Security-Policy"] = ";".join(directives)
	return response

def referrer_policy(response: Response) -> Response:
	# TODO It should be allowed to set more than one referrer policy (array option)
	allowed = ["no-referrer", "no-referrer-when-downgrade", "same-origin", "origin", "strict-origin", "origin-when-cross-origin", "strict-origin-when-cross-origin", "unsafe-url", ""]
	option: str = cast(str, options["Referrer-Policy"])
	if option not in allowed:
		raise HeaderOptionError(option, "Referrer-Policy")	
	response.headers["Referrer-Policy"] = ""
	return response

def cross_origin_embedder_policy(response: Response) -> Response:
	option: str = cast(str, options["Cross-Origin-Embedder-Policy"])
	if option not in ["require-corp", "credentialless"]:
		raise HeaderOptionError(option, "Cross-Origin-Embedder-Policy")	
	response.headers["Cross-Origin-Embedder-Policy"] = ""
	return response

def x_permitted_cross_domain_policies(response: Response) -> Response:
	option: str = cast(str, options["X-Permitted-Cross-Domain-Policies"])
	if option not in ["none","master-only","by-content-type","all"]:
		raise HeaderOptionError(option, "X-Permitted-Cross-Domain-Policies")	
	response.headers["X-Permitted-Cross-Domain-Policies"] = ""
	return response

def cross_origin_opener_policy(response: Response) -> Response:
	option: str = cast(str, options["Cross-Origin-Opener-Policy"])
	if option not in ["same-origin", "same-origin-allow-popups", "unsafe-none"]:
		raise HeaderOptionError(option, "Cross-Origin-Opener-Policy")	
	response.headers["Cross-Origin-Opener-Policy"] = ""
	return response

def x_frame_options(response: Response) -> Response:
	option: str = cast(str, options["X-Frame-Options"])
	if option not in ["DENY", "SAMEORIGIN", "SAME-ORIGIN"]:
		raise HeaderOptionError(option, "X-Frame-Options")
	if option == "SAME-ORIGIN":
		option = "SAMEORIGIN"
	response.headers["X-Frame-Options"] = option
	return response

def cross_origin_resource_policy(response: Response) -> Response:
	option: str = cast(str, options["Cross-Origin-Resource-Policy"])
	if option not in ["same-origin", "same-site", "cross-origin"]:
		raise HeaderOptionError(option, "Cross-Origin-Resource-Policy")
	response.headers["Cross-Origin-Resource-Policy"] = option
	return response

def x_dns_prefetch_control(response: Response) -> Response:
	option: str = cast(str, options["X-DNS-Prefetch-Control"])
	if option not in ["off", "on"]:
		raise HeaderOptionError(option, "X-DNS-Prefetch-Control")
	response.headers["X-DNS-Prefetch-Control"] = option
	return response

def x_download_options(response: Response) -> Response:
	response.headers["X-Download-Options"] = "noopen"
	return response

def x_powered_by(response: Response) -> Response:
	del response.headers["X-Powered-By"]
	return response

def x_xss_protection(response: Response) -> Response:
	response.headers["X-XSS-Protection"] = "0"
	return response

def x_content_type_options(response: Response) -> Response:
	response.headers["X-Content-Type-Options"] = "nosniff"
	return response

def origin_agent_cluster(response: Response) -> Response:
	response.headers["Origin-Agent-Cluster"] = "?1"
	return response
