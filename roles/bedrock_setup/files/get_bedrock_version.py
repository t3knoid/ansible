from playwright.sync_api import sync_playwright
from playwright._impl._errors import Error as PlaywrightError
import re

def get_bedrock_server_url():
    """ Returns the Bedrock server URL """
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        context = browser.new_context()
        page = browser.new_page()
        try:
            page.goto("https://www.minecraft.net/en-us/download/server/bedrock",
                    wait_until="domcontentloaded",
                    timeout=15000  # 15 seconds
            )
        except PlaywrightError as e:
            print(f"Playwright failed: {e}")
            print("Page load timed out")
            context.close()
            browser.close()
            return None
        # wait for download button element
        page.wait_for_selector("a#MC_Download_Server_2[aria-label='serverBedrockLinux'][href*='bedrock-server'][href$='.zip']")
        link = page.query_selector("a#MC_Download_Server_2[aria-label='serverBedrockLinux'][href$='.zip']")
        url = link.get_attribute("href")
        context.close()
        browser.close()
        return url

url = get_bedrock_server_url()
if url:
    match = re.search(r'bedrock-server-(\d+\.\d+\.\d+\.\d+)\.zip', url)
    if match:
        print(match.group(1))  # 👈 Only output the version
