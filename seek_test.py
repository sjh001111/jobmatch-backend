import asyncio
import aiohttp
from lxml import html


async def fetch_seek_job(url: str):
    """Fetch and parse job posting from seek.com.au"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0'
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                html_content = await response.text()
                return parse_seek_job(html_content)
            else:
                print(f"Failed to fetch: {response.status}")
                return None


def parse_seek_job(html_content: str):
    """Parse HTML to extract job information"""
    tree = html.fromstring(html_content)
    
    job_data = {}
    
    # Job title
    title_elem = tree.xpath('//h1[@data-automation="job-detail-title"]')
    job_data['title'] = title_elem[0].text_content().strip() if title_elem else "Title not found"
    
    # Company name
    company_elem = tree.xpath('//a[@data-automation="advertiser-name"] | //span[@data-automation="advertiser-name"]')
    job_data['company'] = company_elem[0].text_content().strip() if company_elem else "Company not found"
    
    # Location
    location_elem = tree.xpath('//span[@data-automation="job-detail-location"]')
    job_data['location'] = location_elem[0].text_content().strip() if location_elem else "Location not found"
    
    # Job description
    desc_elem = tree.xpath('//div[@data-automation="jobAdDetails"]')
    job_data['description'] = desc_elem[0].text_content().strip() if desc_elem else "Description not found"
    
    # Additional details
    details_elem = tree.xpath('//dl[contains(@class, "_1wkzzau0")]')
    if details_elem:
        dt_elements = details_elem[0].xpath('.//dt')
        dd_elements = details_elem[0].xpath('.//dd')
        
        details = {}
        for dt, dd in zip(dt_elements, dd_elements):
            key = dt.text_content().strip()
            value = dd.text_content().strip()
            details[key] = value
        job_data['details'] = details
    
    return job_data


async def test_seek_scraper():
    """Test the scraper with the provided URL"""
    url = "https://www.seek.com.au/job/85528600"
    
    print(f"Fetching job from: {url}")
    job_data = await fetch_seek_job(url)
    
    if job_data:
        print("\n=== Job Information ===")
        print(f"Title: {job_data.get('title', 'N/A')}")
        print(f"Company: {job_data.get('company', 'N/A')}")
        print(f"Location: {job_data.get('location', 'N/A')}")
        
        if 'details' in job_data:
            print("\n=== Additional Details ===")
            for key, value in job_data['details'].items():
                print(f"{key}: {value}")
        
        print(f"\n=== Description Preview ===")
        description = job_data.get('description', 'N/A')
        print(description[:500] + "..." if len(description) > 500 else description)
        
        # Save full description to file for analysis
        with open("scraped_job_posting.txt", "w", encoding="utf-8") as f:
            f.write(f"Title: {job_data.get('title', 'N/A')}\n")
            f.write(f"Company: {job_data.get('company', 'N/A')}\n")
            f.write(f"Location: {job_data.get('location', 'N/A')}\n\n")
            f.write("Description:\n")
            f.write(description)
        
        print("\nFull job posting saved to 'scraped_job_posting.txt'")
        
    else:
        print("Failed to scrape job data")


if __name__ == "__main__":
    asyncio.run(test_seek_scraper())