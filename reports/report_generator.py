from datetime import datetime
import os

# Function to generate detailed report and save to file
def save_report(url, vulnerabilities, report_type="txt"):
    if vulnerabilities:
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        if report_type == "html":
            report_filename = f"reports/{sanitize_url(url)}_{timestamp}.html"
            save_html_report(url, vulnerabilities, report_filename)
        else:
            report_filename = f"reports/{sanitize_url(url)}_{timestamp}.txt"
            save_text_report(url, vulnerabilities, report_filename)
        print(f"Report saved: {report_filename}")

# Helper function to sanitize the URL for file names
def sanitize_url(url):
    return url.replace('http://', '').replace('https://', '').replace('/', '_').replace(':', '')

# Save report as a text file
def save_text_report(url, vulnerabilities, report_filename):
    if not os.path.exists("reports"):
        os.makedirs("reports")

    with open(report_filename, 'w') as report_file:
        report_file.write(f"Vulnerability Report for {url}\n")
        report_file.write("="*50 + "\n")
        for vuln_type, details in vulnerabilities.items():
            report_file.write(f"Vulnerability: {vuln_type}\n")
            report_file.write(f"Location: {details}\n\n")

# Save report as an HTML file
def save_html_report(url, vulnerabilities, report_filename):
    if not os.path.exists("reports"):
        os.makedirs("reports")

    with open(report_filename, 'w') as report_file:
        report_file.write("<html><head><title>Vulnerability Report</title></head><body>")
        report_file.write(f"<h1>Vulnerability Report for {url}</h1>\n")
        report_file.write("<hr>\n")
        for vuln_type, details in vulnerabilities.items():
            report_file.write(f"<h2>{vuln_type}</h2>\n")
            report_file.write(f"<p>Location: {details}</p>\n")
        report_file.write("</body></html>")

# Example function for a detailed vulnerability block
def format_vulnerability_block(vuln_type, details):
    return f"<h2>{vuln_type}</h2><p>Location: {details}</p>"

# Advanced report generation features can be added here.
