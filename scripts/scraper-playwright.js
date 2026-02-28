const { chromium } = require('playwright');

/**
 * Generic web scraper using Playwright (lighter than Puppeteer)
 * @param {string} url - The URL to scrape
 * @param {Object} options - Configuration options
 * @returns {Promise<Object>} - Extracted content
 */
async function scrapeUrl(url, options = {}) {
    const {
        waitTime = 3000,
        timeout = 30000,
        selectors = null
    } = options;

    let browser;
    try {
        browser = await chromium.launch({
            headless: true
        });
        
        const context = await browser.newContext({
            userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        });
        
        const page = await context.newPage();
        
        await page.goto(url, { 
            waitUntil: 'networkidle',
            timeout: timeout 
        });
        
        // Wait for dynamic content
        await page.waitForTimeout(waitTime);
        
        // Extract page info
        const pageInfo = await page.evaluate(() => ({
            title: document.title,
            url: window.location.href,
            description: document.querySelector('meta[name="description"]')?.content ||
                        document.querySelector('meta[property="og:description"]')?.content || ''
        }));
        
        // Extract content
        const content = await page.evaluate((customSelectors) => {
            const results = {
                articles: [],
                headings: [],
                paragraphs: [],
                links: [],
                images: [],
                metadata: {}
            };
            
            // Article selectors
            const articleSelectors = customSelectors || [
                'article',
                '[class*="article"]',
                '[class*="blog"]',
                '[class*="news"]',
                '[class*="post"]',
                '.card',
                '.item',
                '[role="article"]'
            ];
            
            for (const selector of articleSelectors) {
                const elements = document.querySelectorAll(selector);
                elements.forEach(el => {
                    const titleEl = el.querySelector('h1, h2, h3, h4, [class*="title"], [class*="headline"]');
                    const linkEl = el.querySelector('a');
                    const dateEl = el.querySelector('time, [datetime], [class*="date"], [class*="time"]');
                    const excerptEl = el.querySelector('p, [class*="excerpt"], [class*="summary"], [class*="description"]');
                    
                    const title = titleEl?.innerText?.trim() || el.querySelector('a')?.innerText?.trim();
                    const link = linkEl?.href || el.closest('a')?.href;
                    const date = dateEl?.innerText?.trim() || dateEl?.getAttribute('datetime');
                    const excerpt = excerptEl?.innerText?.trim();
                    
                    if (title && title.length > 3 && title.length < 300) {
                        results.articles.push({
                            title: title.substring(0, 200),
                            link: link || '',
                            date: date || '',
                            excerpt: excerpt ? excerpt.substring(0, 500) : ''
                        });
                    }
                });
            }
            
            // Headings
            document.querySelectorAll('h1, h2, h3').forEach(h => {
                const text = h.innerText.trim();
                if (text.length > 3 && text.length < 200) {
                    results.headings.push({ level: h.tagName, text: text });
                }
            });
            
            // Paragraphs
            document.querySelectorAll('p').forEach(p => {
                const text = p.innerText.trim();
                if (text.length > 50 && text.length < 1000) {
                    results.paragraphs.push(text.substring(0, 500));
                }
            });
            
            // Links
            document.querySelectorAll('a[href]').forEach(a => {
                const text = a.innerText.trim();
                const href = a.href;
                if (text.length > 3 && text.length < 150 && href && !href.startsWith('javascript:')) {
                    results.links.push({ text: text.substring(0, 100), url: href });
                }
            });
            
            // Images
            document.querySelectorAll('img[src]').forEach(img => {
                const src = img.src;
                const alt = img.alt || '';
                if (src && !src.includes('data:image')) {
                    results.images.push({ src: src, alt: alt.substring(0, 100) });
                }
            });
            
            // Metadata
            results.metadata = {
                ogTitle: document.querySelector('meta[property="og:title"]')?.content || '',
                ogDescription: document.querySelector('meta[property="og:description"]')?.content || '',
                ogImage: document.querySelector('meta[property="og:image"]')?.content || '',
                author: document.querySelector('meta[name="author"]')?.content || '',
                publishedDate: document.querySelector('meta[property="article:published_time"]')?.content || ''
            };
            
            return results;
        }, selectors);
        
        // Deduplicate articles
        const seen = new Set();
        content.articles = content.articles.filter(a => {
            const key = a.link || a.title;
            if (seen.has(key)) return false;
            seen.add(key);
            return true;
        }).slice(0, 20);
        
        return {
            success: true,
            page: pageInfo,
            content: content,
            scrapedAt: new Date().toISOString()
        };
        
    } catch (error) {
        return {
            success: false,
            error: error.message,
            url: url,
            scrapedAt: new Date().toISOString()
        };
    } finally {
        if (browser) await browser.close();
    }
}

// CLI usage
if (require.main === module) {
    const url = process.argv[2];
    if (!url) {
        console.error('Usage: node scraper-playwright.js <url>');
        process.exit(1);
    }
    
    scrapeUrl(url, { waitTime: 5000 }).then(result => {
        console.log(JSON.stringify(result, null, 2));
        process.exit(result.success ? 0 : 1);
    }).catch(err => {
        console.error(JSON.stringify({ success: false, error: err.message }, null, 2));
        process.exit(1);
    });
}

module.exports = { scrapeUrl };
