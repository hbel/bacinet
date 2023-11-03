from typing import Any, Callable
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.datastructures import MutableHeaders
from .headers import apply

class BacinetMiddleware:
	"""AGSI Middleware to set the proper response headers.
	   Creating the middleware without any additional parameters will use all of the defined headers (which can still be configured via the option variable)
	   Alteratively, provide a function that sets the headers with your individual preferences by supplying a function to the apply_headers parameter
	"""
	def __init__(
		self,
		app: ASGIApp,
		apply_headers: Callable[[dict[str, str]], None] = apply
	) -> None:
		self.app = app
		self.apply_headers = apply_headers
	
	async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
		if scope["type"] != "http":
			await self.app(scope, receive, send)
			
		async def handle_outgoing_request(message: Any) -> None:
			if message['type'] == 'http.response.start':
				headers = MutableHeaders(scope=message)
				response_headers: dict[str, str] = dict(headers.items())
				for key, value in response_headers.items():
					del headers[key]
				self.apply_headers(response_headers)
				for key, value in response_headers.items():
					headers.append(key, value)
				await send(message)
		
		await self.app(scope, receive, handle_outgoing_request)
