import argparse
from siteshot.crawl import run_crawl
from siteshot.runner import run_tests

VERSION = "1.0.0"

def main():
    parser = argparse.ArgumentParser(prog="siteshot", description="SiteShot - Visual QA CLI")
    parser.add_argument("--version", action="version", version=VERSION)
    sub = parser.add_subparsers(dest="command")

    crawl = sub.add_parser("crawl", help="Crawl site & take screenshots")
    crawl.add_argument("--start-url", required=True)
    crawl.add_argument("--out-dir", default="output")
    crawl.add_argument("--max-pages", type=int, default=100)
    crawl.add_argument("--sitemap")
    crawl.add_argument("--nav-selector")
    crawl.add_argument("--ready-selector")
    crawl.add_argument("--viewport", default="1440x900")
    crawl.add_argument("--timeout", type=int, default=45)
    crawl.add_argument("--mobile", action="store_true")

    test = sub.add_parser("test", help="Run QA tests from file")
    test.add_argument("--file", required=True)
    test.add_argument("--out-dir", default="test_results")

    args = parser.parse_args()

    if args.command == "crawl":
        run_crawl(args)
    elif args.command == "test":
        run_tests(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
