# SiteShot CLI – v1.0.1

## Overview

SiteShot CLI is a production-grade command-line tool designed for visual quality assurance of websites.
It crawls web applications using a real browser engine and captures deterministic, full-page screenshots
suitable for QA validation, audits, and CI/CD pipelines.

This release represents a stability and packaging update to the initial public version.

---

## What’s New in v1.0.1

- Fixed missing CLI entry points that caused runtime import errors
- Improved binary packaging for Windows executable
- Ensured consistent CLI command resolution after installation
- Stabilized installer workflow for first-time users
- Internal refactoring for improved reliability

No breaking changes were introduced in this release.

---

## Key Capabilities

- Crawl websites starting from a base URL or sitemap
- Discover internal pages automatically
- Capture full-page screenshots using Chromium
- Handle JavaScript-heavy and SPA-based applications
- Support desktop and mobile viewport emulation
- Execute QA test cases from CSV, XLSX, JSON, and XML files
- Generate structured execution reports and logs
- Fail safely without interrupting test execution

---

## Distribution

This release includes:

- Updated Windows native executable
- Script-based installers for automated setup
- Public download artifacts hosted via GitHub Releases

No manual Python or dependency setup is required when using the provided installers.

---

## Installation

### Windows

```powershell
iwr https://raw.githubusercontent.com/sushil-credencesoft/siteshot/main/install/install.ps1 | iex
```

### Linux / macOS

```bash
curl -fsSL https://raw.githubusercontent.com/sushil-credencesoft/siteshot/main/install/install.sh | bash
```

After installation, restart the terminal and verify:

```bash
siteshot --help
```

---

## Intended Use

SiteShot CLI is intended for:

- Manual and automated QA validation
- Visual regression and UI audits
- Pre-release verification
- Client and compliance documentation
- CI/CD pipeline integration

---

## Platform Support

- Windows (native executable)
- Linux (native binary)
- macOS (native binary)

Each platform requires its corresponding executable.

---

## Ownership and Licensing

Copyright © Credencesoft Private Limited.
All rights reserved.

This software is provided for evaluation and controlled usage.
Redistribution, modification, or commercial reuse without written authorization is prohibited.

---

## Release Notes

This is a maintenance and bug-fix release.
Users of v1.0.0 are strongly recommended to upgrade to this version.
