const puppeteer = require('puppeteer');

/**
 * Generic web scraper that extracts content from any URL
 * @param {string} url - The URL to scrape
 * @param {Object} options - Configuration options
 * @returns {Promise<Object>} - Extracted content
 */
async function scrapeUrl(url, options = {}) {
    const {
        waitTime = 3000,
        timeout = 30000,
        selectors = null,  // Custom selectors if known
        extractAllLinks = false,
        screenshot = false
    } = options;

    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
    });
    
    try {
        const page = await browser.newPage();
        await page.setViewport({ width: 1280, height: 800 });
        
        // Set user agent to avoid bot detection
        await page.setUserAgent(
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        );
        
        await page.goto(url, { 
            waitUntil: 'networkidle2',
            timeout: timeout 
        });
        
        // Wait for dynamic content
        await new Promise(resolve => setTimeout(resolve, waitTime));
        
        // Extract page info
        const pageInfo = await page.evaluate(() => ({
            title: document.title,
            url: window.location.href,
            description: document.querySelector('meta[name="description"]')?.content ||
                        document.querySelector('meta[property="og:description"]')?.content || '',
        }));
        
        // Extract content using multiple strategies
        const content = await page.evaluate((customSelectors) => {
            const results = {
                articles: [],
                headings: [],
                paragraphs: [],
                links: [],
                images: [],
                metadata: {}
            };
            
            // Strategy 1: Look for article/blog/news containers
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
                    
                    if (title && title.length > 3) {
                        results.articles.push({
                            title: title.substring(0, 200),
                            link: link || '',
                            date: date || '',
                            excerpt: excerpt ? excerpt.substring(0, 500) : ''
                        });
                    }
                });
            }
            
            // Strategy 2: Extract all headings
            document.querySelectorAll('h1, h2, h3').forEach(h => {
                const text = h.innerText.trim();
                if (text.length > 3 && text.length < 200) {
                    results.headings.push({
                        level: h.tagName,
                        text: text
                    });
                }
            });
            
            // Strategy 3: Extract main content paragraphs
            document.querySelectorAll('p').forEach(p => {
                const text = p.innerText.trim();
                if (text.length > 50 && text.length < 1000) {
                    results.paragraphs.push(text.substring(0, 500));
                }
            });
            
            // Strategy 4: Extract all links with text
            document.querySelectorAll('a[href]').forEach(a => {
                const text = a.innerText.trim();
                const href = a.href;
                if (text.length > 3 && text.length < 100 && href && !href.startsWith('javascript:')) {
                    results.links.push({
                        text: text.substring(0, 100),
                        url: href
                    });
                }
            });
            
            // Strategy 5: Extract images
            document.querySelectorAll('img[src]').forEach(img => {
                const src = img.src;
                const alt = img.alt || '';
                if (src && !src.includes('data:image')) {
                    results.images.push({
                        src: src,
                        alt: alt.substring(0, 100)
                    });
                }
            });
            
            // Strategy 6: Extract metadata
            results.metadata = {
                ogTitle: document.querySelector('meta[property="og:title"]')?.content || '',
                ogDescription: document.querySelector('meta[property="og:description"]')?.content || '',
                ogImage: document.querySelector('meta[property="og:image"]')?.content || '',
                author: document.querySelector('meta[name="author"]')?.content || 
                       document.querySelector('[class*="author"]')?.innerText?.trim() || '',
                publishedDate: document.querySelector('meta[property="article:published_time"]')?.content ||
                              document.querySelector('meta[name="publishedDate"]')?.content || ''
            };
            
            return results;
        }, selectors);
        
        // Remove duplicate articles
        const uniqueArticles = [...new Map(content.articles.map(a => [a.link || a.title, a])).values()];
        content.articles = uniqueArticles.slice(0, 20); // Limit to 20 articles
        
        // Take screenshot if requested
        let screenshotData = null;
        if (screenshot) {
            screenshotData = await page.screenshot({ 
                encoding: 'base64',
                fullPage: false 
            });
        }
        
        return {
            success: true,
            page: pageInfo,
            content: content,
            screenshot: screenshotData,
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
        await browser.close();
    }
}

// CLI usage
if (require.main === module) {
    const url = process.argv[2];
    if (!url) {
        console.error('Usage: node scraper.js <url>');
        console.error('Example: node scraper.js https://velo.xyz/news');
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
