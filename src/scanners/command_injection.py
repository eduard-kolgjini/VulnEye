import requests
from colorama import Fore

def test_command_injection(url, verbose=False, proxy=None):
    """
    Test for command injection vulnerability.
    Sends a payload that could trigger command execution on the server.
    """
    payload = "127.0.0.1; uname -a"
    try:
        proxies = {'http': proxy, 'https': proxy} if proxy else None
        response = requests.get(url + "?ip=" + payload, proxies=proxies, timeout=10)
        if verbose:
            print(f"Request to {url}?ip={payload} - Status Code: {response.status_code}")

        if response and any(system in response.text for system in ["Linux", "Darwin", "Windows"]):
            print(Fore.RED + f"Command Injection vulnerability found at {url}?ip=")
            return {"Command Injection": f"{url}?ip="}
        else:
            return {}
    except Exception as e:
        print(Fore.RED + f"Error testing command injection at {url}: {e}")
        return {}
