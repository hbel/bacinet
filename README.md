# bacinet

Helmet-like http response Headers for FastAPI.

_This is alpha software lacking testing and proper documentation. Use at your own risk!_

## Basic usage

Install package via `pip install bacinet`.

In your code, import apply from the package and add it as a middleware to your app:

```python
from bacinet import apply
from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def add_bacinet(request: Request, call_next):
    response = await call_next(request)
    apply(response)
    return response
```

Alternatively, you can use an ASGI-conformant Middlware:

```python
from bacinet import BacinetMiddleware


app = FastAPI()


app.add_middleware(BacinetMiddleware)

```

To change the default options, import and change the options dictionary from bacinet:

```python
from bacinet import options

options["X-DNS-Prefetch-Control"] = "on"
```

You can also import individual header functions (like `x_download_options`) and apply those.
