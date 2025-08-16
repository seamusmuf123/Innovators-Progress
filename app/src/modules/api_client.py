import os
import requests

# Simple API client used by Streamlit pages
BASE_URL = os.getenv("BASE_URL", "http://localhost:4000")


def set_base_url(url: str):
    global BASE_URL
    BASE_URL = url.rstrip("/")


def _url(path: str) -> str:
    if not path:
        return BASE_URL
    if path.startswith("http://") or path.startswith("https://"):
        return path
    return f"{BASE_URL.rstrip('/')}/{path.lstrip('/')}"


def get(path: str, **kwargs) -> requests.Response:
    return requests.get(_url(path), **kwargs)


def post(path: str, **kwargs) -> requests.Response:
    return requests.post(_url(path), **kwargs)


def put(path: str, **kwargs) -> requests.Response:
    return requests.put(_url(path), **kwargs)


def delete(path: str, **kwargs) -> requests.Response:
    return requests.delete(_url(path), **kwargs)
import os
import requests

# Simple API client used by Streamlit pages
BASE_URL = os.getenv("BASE_URL", "http://localhost:4000")


def set_base_url(url: str):
    global BASE_URL
    BASE_URL = url.rstrip("/")


def _url(path: str) -> str:
    if not path:
        return BASE_URL
    if path.startswith("http://") or path.startswith("https://"):
        return path
    return f"{BASE_URL.rstrip('/')}/{path.lstrip('/')}"


def get(path: str, **kwargs) -> requests.Response:
    return requests.get(_url(path), **kwargs)


def post(path: str, **kwargs) -> requests.Response:
    return requests.post(_url(path), **kwargs)


def put(path: str, **kwargs) -> requests.Response:
    return requests.put(_url(path), **kwargs)


def delete(path: str, **kwargs) -> requests.Response:
    return requests.delete(_url(path), **kwargs)
