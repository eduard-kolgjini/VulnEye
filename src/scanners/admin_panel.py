import requests
from colorama import Fore

def test_admin_panel(url, verbose=False, proxy=None):
    """
    Test for exposed admin panels.
    Tries common admin panel paths to see if they are accessible.
    """
    admin_paths = ["/admin", "/login", "/admin.php", "/wp-admin", "/controlpanel"]
    try:
        proxies = {'http': proxy, 'https': proxy} if proxy else None
        for path in admin_paths:
            response = requests.get(url + path, proxies=proxies, timeout=10)
            if verbose:
                print(f"Request to {url}{path} - Status Code: {response.status_code}")
                
            if response.status_code == 200:
                print(Fore.RED + f"Exposed admin panel found at {url}{path}")
                return {"Exposed Admin Panel": f"{url}{path}"}
    except Exception as e:
        print(Fore.RED + f"Error testing for admin panel at {url}: {e}")
        return {}

    # Return an empty dict if no vulnerabilities are found
    return {}
