import requests
from colorama import Fore
import logging

# Function to make HTTP requests, supporting verbose and proxy options
def make_request(url, verbose=False, proxy=None, allow_redirects=True):
    """
    Sends an HTTP request to the given URL.
    Supports verbose mode for detailed output and proxy for routing the requests.
    """
    try:
        proxies = {'http': proxy, 'https': proxy} if proxy else None
        response = requests.get(url, timeout=10, proxies=proxies, allow_redirects=allow_redirects)
        if verbose:
            print(f"Request to {url} - Status Code: {response.status_code}")
            print(f"Response Headers: {response.headers}")
            print(f"Response Content: {response.text[:200]}")  # Only show the first 200 chars
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Error connecting to {url}: {e}")
        print(Fore.RED + f"Error connecting to {url}: {e}")
        return None

# Function to log a found vulnerability
def log_vulnerability(vulnerability_type, url):
    """
    Logs the discovered vulnerability to the log file and prints it out.
    """
    message = f"{vulnerability_type} vulnerability found at {url}"
    logging.info(message)
    print(Fore.RED + message)

# Function to check if the website is reachable (already implemented)
def check_website_reachability(url, verbose=False, proxy=None):
    """
    Check if the website is reachable by sending a simple GET request.
    Returns True if the website is reachable, False otherwise.
    """
    try:
        proxies = {'http': proxy, 'https': proxy} if proxy else None
        response = requests.get(url, timeout=10, proxies=proxies)

        if verbose:
            print(f"Request to {url} - Status Code: {response.status_code}")
            print(f"Response Headers: {response.headers}")
            print(f"Response Content: {response.text[:200]}")  # Only show first 200 chars
        
        if response.status_code == 200:
            print(Fore.GREEN + f"Website is reachable: {response.status_code} OK")
            return True
        else:
            print(Fore.RED + f"Website returned status: {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error reaching {url}: {e}")
        return False
