import asyncio
from playwright.async_api import async_playwright
import re

SEEDS = range(62, 72)

async def scrape_seed(page, seed):
    # Naya target URL jo aapne bataya
    url = f"https://sanand0.github.io/tdsdata/js_table/?seed={seed}"
    print(f"Navigating to Seed {seed}...")
    try:
        # Page load hone aur tables fully render hone ka weight karein
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await page.wait_for_selector("table", timeout=10000)
        
        # Saare table rows, cells aur tags se numeric contents fetch karna
        cells = await page.locator("td, th, p, div.table-responsive").all_text_contents()
        combined_text = " ".join(cells)
        
        # Sateek integers aur decimals numbers dhoondhna (-ve numbers samet)
        numbers = re.findall(r'-?\d+(?:\.\d+)?', combined_text)
        
        seed_sum = sum(float(num) for num in numbers)
        print(f"Seed {seed} localized sum: {seed_sum}")
        return seed_sum
    except Exception as e:
        print(f"Error on parsing Seed {seed}: {e}")
        return 0

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        total_sum = 0
        for seed in SEEDS:
            total_sum += await scrape_seed(page, seed)
            
        print("\n" + "="*40)
        print(f"TOTAL SUM OF ALL NUMBERS: {total_sum}")
        print("="*40)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
