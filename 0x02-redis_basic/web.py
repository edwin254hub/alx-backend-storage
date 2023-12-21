import redis
import requests
from typing import Callable
from functools import wraps

rd = redis.Redis()

def count_requests(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(url):
        rd.incr(f"count:{url}")
        cached_html = rd.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')

        response = method(url)  # Use the result of the decorated function
        html = response.text  # Extract HTML from the Response object
        rd.setex(f"cached:{url}", 10, html)
        return html

    return wrapper

@count_requests
def get_page(url: str) -> requests.Response:  # Change the return type to requests.Response
    req = requests.get(url)
    return req
