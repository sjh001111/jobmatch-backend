import asyncio
from playwright.async_api import async_playwright


async def fetch_seek_job_playwright(url: str):
    """Fetch job posting from seek.com.au using Playwright"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = await context.new_page()
        
        try:
            await page.goto(url, wait_until='networkidle')
            await page.wait_for_timeout(2000)
            
            # Get all text content from page
            all_text = await page.evaluate('document.body.innerText')
            
            # Simple text extraction - look for patterns
            lines = all_text.split('\n')
            
            job_data = {
                'title': 'Not found',
                'company': 'Not found', 
                'location': 'Not found',
                'description': all_text  # 전체 텍스트 저장
            }
            
            # Try to find title, company, location from text patterns
            for i, line in enumerate(lines[:50]):  # Check first 50 lines
                line = line.strip()
                if not line:
                    continue
                    
                # Title is usually first meaningful text or contains "Engineer", "Developer", etc
                if job_data['title'] == 'Not found' and any(word in line.lower() for word in ['engineer', 'developer', 'analyst', 'manager', 'specialist']):
                    job_data['title'] = line
                    
                # Company might be after title or contain "Pty", "Ltd", "Inc"
                if job_data['company'] == 'Not found' and any(word in line for word in ['Pty', 'Ltd', 'Inc', 'Company', 'Corp']):
                    job_data['company'] = line
                    
                # Location patterns
                if job_data['location'] == 'Not found' and any(word in line for word in ['NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'NT', 'ACT', 'Sydney', 'Melbourne', 'Brisbane']):
                    job_data['location'] = line
            
            await browser.close()
            return job_data
            
        except Exception as e:
            print(f"Error: {e}")
            await browser.close()
            return None


async def test_playwright_scraper():
    """Test the Playwright scraper"""
    url = "https://www.seek.com.au/job/85528600"
    
    print(f"Scraping: {url}")
    job_data = await fetch_seek_job_playwright(url)
    
    if job_data:
        print(f"Title: {job_data['title']}")
        print(f"Company: {job_data['company']}")
        print(f"Location: {job_data['location']}")
        print(f"Total text length: {len(job_data['description'])} characters")
        
        # Save to file
        with open("seek_job.txt", "w", encoding="utf-8") as f:
            f.write(f"Title: {job_data['title']}\n")
            f.write(f"Company: {job_data['company']}\n")
            f.write(f"Location: {job_data['location']}\n\n")
            f.write(f"Description:\n{job_data['description']}")
        
        print("\nSaved to 'seek_job.txt'")
    else:
        print("Failed to scrape")


if __name__ == "__main__":
    asyncio.run(test_playwright_scraper())