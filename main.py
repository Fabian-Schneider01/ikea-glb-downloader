import asyncio
from playwright.async_api import async_playwright
import re
import os
from urllib.parse import urlparse

DOWNLOAD_DIR = "models"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

async def download_ikea_glb_model(product_url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        glb_urls = []

        async def route_intercept(route):
            url = route.request.url
            if ".glb" in url or "glb_draco" in url:
                print(f"Found 3D model URL: {url}")
                glb_urls.append(url)
            await route.continue_()

        await page.route("**/*", route_intercept)

        print(f"Opening product page: {product_url}")
        await page.goto(product_url, wait_until="networkidle")

        ar_button_selector = ".pip-xr-button"
        try:
            await page.wait_for_selector(ar_button_selector, timeout=5000)
            print("3D button found, clicking it...")
            await page.click(ar_button_selector)
        except Exception:
            print("No 3D button found or timeout.")

        await asyncio.sleep(15)

        if not glb_urls:
            print("No 3D model (.glb) found.")
            await browser.close()
            return

        glb_url = glb_urls[-1]
        print(f"Downloading: {glb_url}")

        title = await page.title()
        title_clean = re.sub(r'[<>:"/\\|?*]', '', title.split(" - IKEA")[0].strip())
        product_id_match = re.search(r'/(\d+)[_/]', glb_url)
        product_id = product_id_match.group(1) if product_id_match else ""
        filename = f"{title_clean} ({product_id}).glb" if product_id else f"{title_clean}.glb"
        filename = filename.strip()
        filepath = os.path.join(DOWNLOAD_DIR, filename)

        try:
            download_response = await page.request.get(glb_url)
            if download_response.ok:
                data = await download_response.body()
                with open(filepath, "wb") as f:
                    f.write(data)
                print(f"Model saved: {filepath}")
            else:
                print(f"Download error: HTTP {download_response.status}")
        except Exception as e:
            print(f"Download error: {e}")

        await browser.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Please provide IKEA product URL as an argument.")
        sys.exit(1)
    url = sys.argv[1]
    asyncio.run(download_ikea_glb_model(url))
