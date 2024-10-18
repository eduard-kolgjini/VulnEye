from src.core.utils import make_request, log_vulnerability
from colorama import Fore

def test_xss(url, verbose=False, proxy=None):
    payload = "<script>alert('XSS')</script>"
    try:
        response = make_request(f"{url}?q={payload}", verbose=verbose, proxy=proxy)
        if response and payload in response.text:
            print(Fore.RED + f"XSS vulnerability found at {url}?q=")
            log_vulnerability("XSS", f"{url}?q=")
            return {"XSS": f"{url}?q="}
    except Exception as e:
        print(Fore.RED + f"Error testing XSS at {url}: {e}")
    return {}
