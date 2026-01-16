# SiteShot

SiteShot is a command-line interface (CLI) tool designed for **visual quality assurance (QA)** of websites.  
It crawls websites using a real browser engine (Playwright + Chromium), captures full-page screenshots, and produces structured execution artifacts suitable for audits, testing, and CI/CD pipelines.

This project is owned and maintained by **Credencesoft Private Limited**.  
All rights reserved.

---

## Purpose of SiteShot

Modern websites are dynamic, JavaScript-heavy, and frequently updated.  
Traditional crawlers cannot accurately represent what users actually see.

SiteShot exists to solve the following problems:

- Create a **single source of visual truth** for a website
- Enable **visual regression and UI audits**
- Provide **deterministic, repeatable screenshots**
- Support **manual QA and automated pipelines**
- Work reliably with **SPAs (React, Vue, Next.js, etc.)**

SiteShot is not a scraper.  
It is a **visual QA instrument**.

---

## High-Level Architecture

The SiteShot system is composed of the following layers:

- CLI Interface  
- Crawl Engine  
- Browser Automation Layer  
- Artifact Generation  
- Test Execution Framework  

### Technology Stack

- Python 3.9+
- Playwright (Chromium)
- Async I/O
- Structured logging
- File-based execution artifacts

Keywords:
python, playwright, chromium, siteshot, visual qa, website testing

---

## Key Capabilities

- Crawl websites starting from a URL or sitemap
- Discover internal links automatically
- Capture full-page screenshots
- Handle SPA navigation and client-side routing
- Emulate desktop and mobile viewports
- Execute QA test plans from CSV, XLSX, JSON, or XML
- Generate execution reports and logs
- Fail safely without stopping the run

---

## Output Artifacts

Each execution produces:

- Screenshots directory
- Manifest file (JSON)
- Execution logs
- Test execution report (CSV)

These artifacts are suitable for:

- QA evidence
- Compliance audits
- CI/CD pipeline attachments
- Manual review

---

## Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager
- Internet access for browser installation

### Install from Source

Clone the repository:

```bash
git clone https://github.com/sushil-credencesoft/siteshot.git
cd siteshot
```

Install the CLI locally:

```bash
pip install -e .
```

Install Playwright browsers:

```bash
playwright install
```

---

Install PowerShell

```bash
iwr https://raw.githubusercontent.com/sushil-credencesoft/siteshot/main/install/install.ps1 | ixe
```

---

## CLI Usage Overview

After installation, the following command becomes available globally:

```bash
siteshot
```

### Available Commands

- `siteshot crawl`  
  Crawl a website and capture screenshots

- `siteshot test`  
  Execute QA test cases from a file

Use the help command for full options:

```bash
siteshot --help
siteshot crawl --help
siteshot test --help
```

---

## Typical Use Cases

- Website visual regression testing
- QA verification before production releases
- UX and design audits
- SEO and sitemap validation
- Client deliverables and reporting
- Compliance and archival snapshots

---

## Repository Structure

```
siteshot/
├── siteshot/
│   ├── cli.py
│   ├── crawl.py
│   ├── runner.py
│   └── utils.py
├── pyproject.toml
├── README.md
└── LICENSE
```

---

## Security and Compliance

- SiteShot respects website boundaries and same-origin rules
- Robots.txt support can be enabled
- No data is transmitted externally
- All artifacts are stored locally unless explicitly uploaded

---

## Licensing and Ownership

Copyright © Credencesoft Private Limited.  
All rights reserved.

This repository is published for evaluation, controlled usage, and internal tooling purposes.  
Redistribution, modification, or commercial reuse without written permission from Credencesoft Private Limited is prohibited.

---

## Support and Maintenance

This tool is maintained by Credencesoft Private Limited.

For internal support, enhancements, or enterprise customization, please contact the Credencesoft engineering team.

---

## Disclaimer

SiteShot is provided as-is without warranty of any kind.  
Users are responsible for ensuring compliance with local laws, website terms of service, and organizational policies when crawling websites.
