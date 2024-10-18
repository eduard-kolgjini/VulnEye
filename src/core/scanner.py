import concurrent.futures
import time
import logging
from src.scanners.sql_injection import test_sql_injection
from src.scanners.xss import test_xss
from src.scanners.admin_panel import test_admin_panel
from src.scanners.csrf import test_csrf_token
from src.scanners.file_upload import test_file_upload
from src.scanners.command_injection import test_command_injection
from src.scanners.directory_traversal import test_directory_traversal
from src.scanners.open_redirect import test_open_redirect
from src.scanners.security_headers import test_security_headers
from src.core.utils import check_website_reachability
from reports.report_generator import save_report

# Initialize logging
logging.basicConfig(filename='vuln_eye.log', level=logging.INFO, format='%(asctime)s - %(message)s')


def scan_website(url, delay=0, verbose=False, proxy=None, report_type="txt"):
    """
    Scans a single website for vulnerabilities using different vulnerability scanners.
    Saves the report if any vulnerabilities are found.
    """
    logging.info(f"Starting scan for {url}")
    print(f"\nStarting scan for {url}...\n")

    vulnerabilities = {}

    try:
        # Check if the website is reachable
        if check_website_reachability(url, verbose=verbose, proxy=proxy):
            # Run all the scanners and collect results
            vulnerabilities.update(test_sql_injection(url, verbose=verbose, proxy=proxy))
            vulnerabilities.update(test_xss(url, verbose=verbose, proxy=proxy))
            vulnerabilities.update(test_admin_panel(url, verbose=verbose, proxy=proxy))
            vulnerabilities.update(test_csrf_token(url, verbose=verbose, proxy=proxy))
            vulnerabilities.update(test_file_upload(url, verbose=verbose, proxy=proxy))
            vulnerabilities.update(test_command_injection(url, verbose=verbose, proxy=proxy))
            vulnerabilities.update(test_directory_traversal(url, verbose=verbose, proxy=proxy))
            vulnerabilities.update(test_open_redirect(url, verbose=verbose, proxy=proxy))
            vulnerabilities.update(test_security_headers(url, verbose=verbose, proxy=proxy))

            # If vulnerabilities are found, save a report
            if vulnerabilities:
                save_report(url, vulnerabilities, report_type=report_type)
                logging.info(f"Vulnerabilities found for {url}: {vulnerabilities}")
            else:
                logging.info(f"No vulnerabilities found for {url}")
                print(f"No vulnerabilities found for {url}")

        else:
            logging.warning(f"Website unreachable: {url}")
            print(f"Website unreachable: {url}")

    except Exception as e:
        logging.error(f"Error scanning {url}: {e}")
        print(f"Error scanning {url}: {e}")

    # Delay to avoid rate-limiting issues
    if delay:
        print(f"Sleeping for {delay} seconds to avoid rate limiting...")
        time.sleep(delay)


def batch_scan(file_path, delay=0, verbose=False, proxy=None, report_type="txt", parallel=1):
    """
    Batch scan multiple URLs from a file, supports parallel execution.
    """
    try:
        with open(file_path, 'r') as file:
            urls = [line.strip() for line in file.readlines()]
        
        # Parallel scanning using ThreadPoolExecutor
        if parallel > 1:
            logging.info(f"Starting batch scan with {parallel} threads")
            with concurrent.futures.ThreadPoolExecutor(max_workers=parallel) as executor:
                executor.map(scan_website, urls)
        else:
            for url in urls:
                scan_website(url, delay=delay, verbose=verbose, proxy=proxy, report_type=report_type)

    except Exception as e:
        logging.error(f"Error reading batch file: {e}")
        print(f"Error reading batch file: {e}")
