from playwright.sync_api import sync_playwright
from playwright._impl._errors import Error as PlaywrightError
import re

def get_java_server_version():
    """Returns the Java Edition server version using Playwright."""
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        context = browser.new_context()
        page = browser.new_page()

        try:
            page.goto(
                "https://www.minecraft.net/en-us/download/server",
                wait_until="networkidle",   # Wait for all JS to finish
                timeout=20000
            )
        except PlaywrightError as e:
            print(f"Playwright failed: {e}")
            context.close()
            browser.close()
            return None

        # Wait for the version text to appear
        try:
            page.wait_for_selector("code:has-text('minecraft_server')", timeout=10000)
        except PlaywrightError:
            print("Version text did not appear")
            context.close()
            browser.close()
            return None

        html = page.content()

        context.close()
        browser.close()

        # Extract version from text like minecraft_server.1.21.4.jar
        match = re.search(r"minecraft_server\.(\d+\.\d+\.\d+)\.jar", html)
        if match:
            return match.group(1)

        return None

version = get_java_server_version()
if version:
    print(version)
