import argparse
from src.core.scanner import scan_website, batch_scan

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VulnEye - Website Vulnerability Scanner")
    parser.add_argument('-u', '--url', help="URL of the website to scan")
    parser.add_argument('--batch', help="Path to a file containing multiple URLs for batch scanning")
    parser.add_argument('--rate-limit', type=int, help="Time delay between requests in seconds")
    parser.add_argument('--verbose', action='store_true', help="Enable verbose mode for detailed output")
    parser.add_argument('--proxy', help="Proxy to use for requests (e.g., http://localhost:8080)")
    parser.add_argument('--html', action='store_true', help="Generate report in HTML format")
    parser.add_argument('--parallel', type=int, help="Number of parallel threads for scanning")
    parser.add_argument('--payloads', help="Custom payload file for advanced vulnerability scanning")

    args = parser.parse_args()

    report_type = "html" if args.html else "txt"

    if args.batch:
        batch_scan(args.batch, delay=args.rate_limit, verbose=args.verbose, proxy=args.proxy, report_type=report_type, parallel=args.parallel)
    elif args.url:
        scan_website(args.url, delay=args.rate_limit, verbose=args.verbose, proxy=args.proxy, report_type=report_type)
    else:
        print("Please provide a URL or a batch file for scanning.")
