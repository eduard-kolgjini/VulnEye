import requests
from colorama import Fore

def test_open_redirect(url, verbose=False, proxy=None):
    """
    Test for open redirect vulnerability.
    Sends a payload that could cause a redirect to an external malicious site.
    """
    payload = "http://evil.com"
    try:
        proxies = {'http': proxy, 'https': proxy} if proxy else None
        response = requests.get(url + "?redirect=" + payload, proxies=proxies, timeout=10, allow_redirects=False)
        if verbose:
            print(f"Request to {url}?redirect={payload} - Status Code: {response.status_code}")

        if response and response.status_code in [301, 302] and payload in response.headers.get('Location', ''):
            print(Fore.RED + f"Open Redirect vulnerability found at {url}?redirect=")
            return {"Open Redirect": f"{url}?redirect="}
        else:
            return {}
    except Exception as e:
        print(Fore.RED + f"Error testing open redirect at {url}: {e}")
        return {}
