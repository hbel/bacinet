class HeaderOptionError(Exception):
	def __init__(self, option: str, header_name: str) -> None:
		super().__init__(f"Unknown option {option} for {header_name} header")
