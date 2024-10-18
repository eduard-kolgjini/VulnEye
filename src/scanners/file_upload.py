import requests
from colorama import Fore

def test_file_upload(url, verbose=False, proxy=None):
    """
    Test for file upload vulnerability.
    Attempts to upload a simple text file and checks if it gets reflected in the server response.
    """
    files = {'file': ('test.txt', 'This is a test file', 'text/plain')}
    
    try:
        proxies = {'http': proxy, 'https': proxy} if proxy else None
        response = requests.post(url, files=files, proxies=proxies, timeout=10)

        if verbose:
            print(f"Request to {url} - Status Code: {response.status_code}")
            print(f"Response Headers: {response.headers}")
            print(f"Response Content: {response.text[:200]}")  # Print the first 200 characters of the response
        
        if response and "test.txt" in response.text:
            print(Fore.RED + f"File upload vulnerability found at {url}")
            return {"File Upload": f"{url}"}
    
    except Exception as e:
        print(Fore.RED + f"Error testing file upload at {url}: {e}")
        return {}

    # Return an empty dict if no file upload vulnerability is found
    return {}
