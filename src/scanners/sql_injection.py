from src.core.utils import make_request, log_vulnerability
from colorama import Fore


def test_sql_injection(url, payloads=None, verbose=False, proxy=None):
    if payloads is None:
        payloads = ["' OR 1=1--"]
    
    for payload in payloads:
        try:
            response = make_request(f"{url}?id={payload}", verbose=verbose, proxy=proxy)
            if response and ("SQL syntax" in response.text or "mysql" in response.text):
                print(Fore.RED + f"SQL Injection vulnerability found at {url}?id=")
                log_vulnerability("SQL Injection", f"{url}?id=")
                return {"SQL Injection": f"{url}?id="}
        except Exception as e:
            print(Fore.RED + f"Error testing SQL Injection at {url}: {e}")
    return {}
