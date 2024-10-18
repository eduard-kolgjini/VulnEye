import requests
from colorama import Fore

def test_security_headers(url, verbose=False, proxy=None):
    """
    Test for missing security headers.
    Checks if important HTTP security headers are present.
    """
    headers_to_check = [
        'X-Content-Type-Options',
        'X-Frame-Options',
        'Content-Security-Policy',
        'Strict-Transport-Security',
        'X-XSS-Protection'
    ]
    try:
        proxies = {'http': proxy, 'https': proxy} if proxy else None
        response = requests.get(url, proxies=proxies, timeout=10)
        if verbose:
            print(f"Request to {url} - Status Code: {response.status_code}")

        missing_headers = [header for header in headers_to_check if header not in response.headers]
        if missing_headers:
            print(Fore.RED + f"Missing security headers at {url}: {', '.join(missing_headers)}")
            return {"Missing Security Headers": missing_headers}
        else:
            return {}
    except Exception as e:
        print(Fore.RED + f"Error testing security headers at {url}: {e}")
        return {}
