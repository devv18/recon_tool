# Subdomain Feature Detection Tool

A Python-based reconnaissance tool that scans subdomains and detects common web application functionalities such as authentication systems, search functionality, file uploads, chat systems, admin panels, forms, and input fields.

## Features

- Detects authentication pages
- Identifies search functionality
- Detects file upload forms
- Finds chat/support systems
- Detects admin panels and dashboards
- Counts forms and input fields
- Supports both HTTP and HTTPS
- Generates summarized results

## Requirements

Install the required Python modules:

```bash
pip install requests beautifulsoup4 urllib3

how to use it :

recon_test.py <sub_domain_filename>
