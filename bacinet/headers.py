
from typing import Any, cast

from .header_options import options
from .exceptions import HeaderOptionError

def apply(response: dict[str, str]) -> None:
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

def strict_transport_security(response: dict[str, str]) -> None:
	option: dict[str, Any] = cast(dict[str, Any], options["Strict-Transport-Security"])
	directives: list[str] = []
	for dir in option.keys():
		match dir:
			case "maxAge": directives.append(f"maxAge={option['maxAge']}")
			case "includeSubDomains": 
				if option["includeSubDomains"] == True: directives.append("includeSubDomains")																		   
			case "preload": 
				if option["preload"] == True: directives.append("preload")
			case _: raise HeaderOptionError(dir, "Strict-Transport-Security")
			
	response["Strict-Transport-Security"] = ";".join(directives)

def content_security_policy(response: dict[str, str]) -> None:
	option: dict[str, list[str]] = cast(dict[str, list[str]], options["Content-Security-Policy"])
	directives: list[str] = []
	for dir in option.keys():
		if len(option[dir]) > 0 and option[dir][0] != "":
			directives.append(f"{dir} {' '.join(option[dir])}")
		else:
			directives.append(dir)
	response["Content-Security-Policy"] = ";".join(directives)

def referrer_policy(response: dict[str, str]) -> None:
	# TODO It should be allowed to set more than one referrer policy (array option)
	allowed = ["no-referrer", "no-referrer-when-downgrade", "same-origin", "origin", "strict-origin", "origin-when-cross-origin", "strict-origin-when-cross-origin", "unsafe-url", ""]
	option: str = cast(str, options["Referrer-Policy"])
	if option not in allowed:
		raise HeaderOptionError(option, "Referrer-Policy")	
	response["Referrer-Policy"] = "no-referrer"

def cross_origin_embedder_policy(response: dict[str, str]) -> None:
	option: str = cast(str, options["Cross-Origin-Embedder-Policy"])
	if option not in ["require-corp", "credentialless"]:
		raise HeaderOptionError(option, "Cross-Origin-Embedder-Policy")	
	response["Cross-Origin-Embedder-Policy"] = option

def x_permitted_cross_domain_policies(response: dict[str, str]) -> None:
	option: str = cast(str, options["X-Permitted-Cross-Domain-Policies"])
	if option not in ["none","master-only","by-content-type","all"]:
		raise HeaderOptionError(option, "X-Permitted-Cross-Domain-Policies")	
	response["X-Permitted-Cross-Domain-Policies"] = option

def cross_origin_opener_policy(response: dict[str, str]) -> None:
	option: str = cast(str, options["Cross-Origin-Opener-Policy"])
	if option not in ["same-origin", "same-origin-allow-popups", "unsafe-none"]:
		raise HeaderOptionError(option, "Cross-Origin-Opener-Policy")	
	response["Cross-Origin-Opener-Policy"] = option

def x_frame_options(response: dict[str, str]) -> None:
	option: str = cast(str, options["X-Frame-Options"])
	if option not in ["DENY", "SAMEORIGIN", "SAME-ORIGIN"]:
		raise HeaderOptionError(option, "X-Frame-Options")
	if option == "SAME-ORIGIN":
		option = "SAMEORIGIN"
	response["X-Frame-Options"] = option

def cross_origin_resource_policy(response: dict[str, str]) -> None:
	option: str = cast(str, options["Cross-Origin-Resource-Policy"])
	if option not in ["same-origin", "same-site", "cross-origin"]:
		raise HeaderOptionError(option, "Cross-Origin-Resource-Policy")
	response["Cross-Origin-Resource-Policy"] = option

def x_dns_prefetch_control(response: dict[str, str]) -> None:
	option: str = cast(str, options["X-DNS-Prefetch-Control"])
	if option not in ["off", "on"]:
		raise HeaderOptionError(option, "X-DNS-Prefetch-Control")
	response["X-DNS-Prefetch-Control"] = option

def x_download_options(response: dict[str, str]) -> None:
	response["X-Download-Options"] = "noopen"

def x_powered_by(response: dict[str, str]) -> None:
	if response.get("X-Powered-By") != None:
		del response["X-Powered-By"]
	if response.get("x-powered-by") != None:
		del response["x-powered-by"]

def x_xss_protection(response: dict[str, str]) -> None:
	response["X-XSS-Protection"] = "1"

def x_content_type_options(response: dict[str, str]) -> None:
	response["X-Content-Type-Options"] = "nosniff"

def origin_agent_cluster(response: dict[str, str]) -> None:
	response["Origin-Agent-Cluster"] = "?1"
