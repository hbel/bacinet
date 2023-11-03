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
    apply(response.headers)
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

You can also import individual header functions (like `x_download_options`) and apply those on your own applicator function that can be provided to BacinetMiddleware's constructor.

## Headers

In it's standard form, the following headers will be set or removed by the middleware:

| Header                            |               Default               | Description                                                                            |
| :-------------------------------- | :---------------------------------: | :------------------------------------------------------------------------------------- |
| Origin-Agent-Cluster              |                `?1`                 | https://github.com/WICG/origin-agent-cluster                                           |
| X-Content-Type-Options            |              `nosniff`              | Prevents MIME type sniffing attacks                                                    |
| X-XSS-Protection                  |                 `1`                 | Enables XSS filtering and page sanitation in the browser                               |
| X-Powered-By                      |              _removed_              | Header gets removed to hinder server identification                                    |
| X-Download-Options                |              `noopen`               | Prevent automated opening of downloads in legacy browsers                              |
| X-DNS-Prefetch-Control            |                `off`                | Prevents general DNS prefetching for links                                             |
| Cross-Origin-Resource-Policy      |            `same-origin`            | disallow cross-origin no-cors requests                                                 |
| X-Frame-Options                   |               `DENY`                | Deny embedding in other sited                                                          |
| Cross-Origin-Opener-Policy        |            `same-origin`            | Deny sharing browsing context with cross-origin documents                              |
| X-Permitted-Cross-Domain-Policies |               `none`                | Disallow document embedding of the resource                                            |
| Cross-Origin-Embedder-Policy      |           `require-corp`            | https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Embedder-Policy |
| Referrer-Policy                   |            `no-referrer`            | Do not send referrer headers                                                           |
| Content-Security-Policy           |              see below              | Restrict resource access                                                               |
| Strict-Transport-Security         | `maxAge=15552000;includeSubDomains` | Make sure that the site is only accessed via https                                     |

### Default content-security policies

The following content-security policies are applied in the default setting:

-   `default-src 'self';base-uri 'self'`
-   `font-src 'self' https: data:`
-   `form-action 'self'`
-   `frame-ancestors 'self'`
-   `img-src 'self' data:`
-   `object-src 'none'`
-   `script-src 'self'`
-   `script-src-attr 'none'`
-   `style-src 'self' https: 'unsafe-inline'`
-   `upgrade-insecure-requests`
