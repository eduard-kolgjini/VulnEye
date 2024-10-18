import requests
from colorama import Fore

def test_csrf_token(url, verbose=False, proxy=None):
    """
    Test for missing CSRF tokens in forms.
    A valid CSRF token should be present in forms for protection against CSRF attacks.
    """
    try:
        proxies = {'http': proxy, 'https': proxy} if proxy else None
        response = requests.get(url, proxies=proxies, timeout=10)
        
        if verbose:
            print(f"Request to {url} - Status Code: {response.status_code}")
        
        if "<form" in response.text and "csrf" not in response.text.lower():
            print(Fore.RED + f"Missing CSRF token in forms at {url}")
            return {"CSRF Token Missing": f"{url}"}
    
    except Exception as e:
        print(Fore.RED + f"Error testing for CSRF token at {url}: {e}")
        return {}

    # Return an empty dict if no CSRF vulnerability is found
    return {}
