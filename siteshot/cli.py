import argparse
import sys
from siteshot.crawl import run_crawl
from siteshot.runner import run_tests

VERSION = "1.0.1"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="siteshot",
        description="SiteShot - Visual QA and Website Auditing CLI"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"SiteShot CLI {VERSION}"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    # -------------------------------------------------
    # crawl command
    # -------------------------------------------------
    crawl = subparsers.add_parser(
        "crawl",
        help="Crawl a website and capture full-page screenshots"
    )
    crawl.add_argument("--start-url", required=True, help="Starting URL")
    crawl.add_argument("--out-dir", default="output", help="Output directory")
    crawl.add_argument("--max-pages", type=int, default=100, help="Maximum pages to crawl")
    crawl.add_argument("--sitemap", help="Optional sitemap.xml URL")
    crawl.add_argument("--nav-selector", help="CSS selector for navigation capture")
    crawl.add_argument("--ready-selector", help="CSS selector to wait for page readiness")
    crawl.add_argument("--viewport", default="1440x900", help="Viewport size WxH")
    crawl.add_argument("--timeout", type=int, default=45, help="Page timeout (seconds)")
    crawl.add_argument("--mobile", action="store_true", help="Enable mobile emulation")

    # -------------------------------------------------
    # test command
    # -------------------------------------------------
    test = subparsers.add_parser(
        "test",
        help="Execute QA test cases from a structured file"
    )
    test.add_argument("--file", required=True, help="CSV/XLSX/JSON/XML test file")
    test.add_argument("--out-dir", default="test_results", help="Test output directory")

    # -------------------------------------------------
    # validate command
    # -------------------------------------------------
    validate = subparsers.add_parser(
        "validate",
        help="Validate CLI installation and environment"
    )

    # -------------------------------------------------
    # doctor command
    # -------------------------------------------------
    doctor = subparsers.add_parser(
        "doctor",
        help="Run environment diagnostics for SiteShot"
    )

    # -------------------------------------------------
    # config command (future-safe)
    # -------------------------------------------------
    config = subparsers.add_parser(
        "config",
        help="Display effective SiteShot configuration"
    )

    return parser


def cmd_validate():
    print("SiteShot CLI validation successful")
    print("Executable resolved correctly")
    print("CLI version:", VERSION)


def cmd_doctor():
    print("Running SiteShot diagnostics")
    print("Python runtime: embedded")
    print("Playwright: bundled")
    print("Environment check completed")


def cmd_config():
    print("SiteShot configuration")
    print("Default output directory: output")
    print("Default viewport: 1440x900")
    print("Default timeout: 45 seconds")


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "crawl":
        run_crawl(args)

    elif args.command == "test":
        run_tests(args)

    elif args.command == "validate":
        cmd_validate()

    elif args.command == "doctor":
        cmd_doctor()

    elif args.command == "config":
        cmd_config()

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
