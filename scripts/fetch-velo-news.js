const puppeteer = require('puppeteer');

async function fetchVeloNews() {
    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    try {
        const page = await browser.newPage();
        await page.goto('https://velo.xyz/news', { 
            waitUntil: 'networkidle2',
            timeout: 30000 
        });
        
        // Wait for content to load (adjust selector as needed)
        await page.waitForTimeout(3000);
        
        // Extract news items
        const news = await page.evaluate(() => {
            const items = [];
            // Common selectors for news/blog posts
            const selectors = [
                'article',
                '[class*="news"]',
                '[class*="post"]',
                '[class*="blog"]',
                '.card',
                'a[href*="/news/"]',
                'a[href*="/blog/"]',
                'a[href*="/article/"]'
            ];
            
            for (const selector of selectors) {
                const elements = document.querySelectorAll(selector);
                elements.forEach(el => {
                    const title = el.querySelector('h1, h2, h3, h4, .title, [class*="title"]')?.innerText?.trim() || 
                                  el.innerText?.split('\n')[0]?.trim();
                    const link = el.href || el.querySelector('a')?.href;
                    const date = el.querySelector('time, [class*="date"], [class*="time"]')?.innerText?.trim();
                    const excerpt = el.querySelector('p, [class*="excerpt"], [class*="summary"], [class*="description"]')?.innerText?.trim();
                    
                    if (title && title.length > 5) {
                        items.push({ title, link, date, excerpt });
                    }
                });
            }
            
            // Remove duplicates
            return [...new Map(items.map(item => [item.link || item.title, item])).values()];
        });
        
        return news;
        
    } catch (error) {
        console.error('Error fetching Velo news:', error);
        return [];
    } finally {
        await browser.close();
    }
}

// Run if called directly
if (require.main === module) {
    fetchVeloNews().then(news => {
        console.log(JSON.stringify(news, null, 2));
        process.exit(0);
    }).catch(err => {
        console.error(err);
        process.exit(1);
    });
}

module.exports = { fetchVeloNews };
