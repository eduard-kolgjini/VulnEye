# VulnEye - Website Vulnerability Scanner

VulnEye is a powerful tool designed for scanning websites for various security vulnerabilities. It helps identify common security issues, including SQL Injection, Cross-Site Scripting (XSS), Directory Traversal, Open Redirect, and more.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Report Generation](#report-generation)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Multiple Vulnerability Tests**: Detects various vulnerabilities, including:
  - SQL Injection
  - Cross-Site Scripting (XSS)
  - Directory Traversal
  - Open Redirect
  - Command Injection
  - Missing Security Headers
  - Exposed Admin Panels
  - Missing CSRF Tokens
  - File Upload Vulnerabilities

- **Batch Scanning**: Supports scanning multiple URLs from a file.
- **Parallel Execution**: Speed up scans by running multiple threads.
- **Verbose Output**: Detailed output of each scan operation for better debugging and understanding.
- **Custom Payloads**: Option to use custom payloads for advanced detection methods.
- **Report Generation**: Generates comprehensive reports in both text and HTML formats.

## Installation

To install VulnEye, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/vuln-eye.git
   cd vuln-eye
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
### Usage

To use the VulnEye scanner, run the following command:
```bash
python vuln_eye.py --url <TARGET_URL>
```

To scan multiple URLs from a file, use the --batch option:
```bash
python vuln_eye.py --batch urls.txt --parallel <NUMBER_OF_THREADS>
```
### Options

- `-u`, `--url`: URL of the website to scan.
- `--batch`: Path to a file containing multiple URLs for batch scanning.
- `--rate-limit`: Time delay between requests in seconds.
- `--verbose`: Enable verbose mode for detailed output.
- `--proxy`: Proxy to use for requests (e.g., `http://localhost:8080`).
- `--html`: Generate report in HTML format.

### Report Generation

The scanner generates reports detailing any vulnerabilities found during the scan. Reports are saved in the `reports` directory with a timestamp in the filename.

### Contributing

Contributions are welcome! If you would like to contribute, please fork the repository and submit a pull request with your changes.

### License

This project is licensed under the MIT License.
