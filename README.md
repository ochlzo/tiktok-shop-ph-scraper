# TikTok Shop Reviews Scraper for Lancôme Products

## 📋 Project Overview

This project is a technical assessment solution for scraping customer reviews from TikTok Shop, specifically targeting Lancôme products in Vietnam and Saudi Arabia markets. The scraper is designed to collect comprehensive review data while respecting website terms and implementing proper rate limiting.

## 🎯 Objectives

- **Step 1**: Scrape product URLs for Lancôme brand from TikTok Shop
- **Step 2**: Collect maximum available reviews from these product pages
- **Target Markets**: Vietnam (`shop.tiktok.com/vn`) and Saudi Arabia (`shop.tiktok.com/sa`)

## 🚀 Features

### Core Functionality
- ✅ Multi-market support (Vietnam & Saudi Arabia)
- ✅ Intelligent product discovery via search and brand pages
- ✅ Comprehensive review extraction with all metadata
- ✅ CSV export with standardized format
- ✅ Robust error handling and logging
- ✅ Anti-detection measures (user agent rotation, delays)

### Advanced Features
- 🔄 Automatic retry mechanisms
- 📊 Progress tracking and checkpoints
- 🛡️ Rate limiting and respectful scraping
- 🔍 Data validation and deduplication
- 📱 Responsive design detection
- 🌐 Proxy support (configurable)

## 📁 Project Structure

```
tiktok-shop-reviews-scraper/
├── tiktok-shop-scraper.py   # Main scraper implementation
├── config.py                              # Configuration settings
├── utils.py                               # Utility functions
├── requirements.txt                       # Python dependencies
├── README.md                              # This file
├── method_documentation.md                # Detailed methodology
├── setup.py                              # Setup script
├── test_scraper.py                       # Test cases
└── sample_output/                        # Sample output files
    └── aymane_aallaoui_tiktok_shop_reviews_sample.csv
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Chrome browser installed
- ChromeDriver (auto-downloaded via webdriver-manager)

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/aymaneallaoui/tiktok-shop-reviews-scraper.git
cd tiktok-shop-reviews-scraper

# Install dependencies
pip install -r requirements.txt

# Run the scraper
python tiktok-shop-scraper.py
```

### Advanced Setup with Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run setup script (optional)
python setup.py
```

## 🖥️ Usage

### Basic Usage

```python
from tiktok_shop_scraper import TikTokShopScraper

# Initialize scraper
scraper = TikTokShopScraper(headless=True)

# Run complete scraping process
reviews = scraper.run_complete_scraping()

# Save to CSV
scraper.save_to_csv(reviews, "reviews_output.csv")
```

### Advanced Configuration

```python
from config import get_config
from tiktok_shop_scraper import TikTokShopScraper

# Load configuration
config = get_config()

# Initialize with custom settings
scraper = TikTokShopScraper(
    headless=config.HEADLESS_BROWSER,
    proxy="http://proxy-server:port"  # Optional
)

# Scrape specific market
products = scraper.search_lancome_products('vietnam')
for product in products:
    reviews = scraper.scrape_product_reviews(product)
    print(f"Found {len(reviews)} reviews for {product.name}")
```

### Scrape Reviews From a Product URL

Use this command to scrape one product URL directly and save both CSV and JSON files:

```bash
python -c "from tiktok_shop_scraper import TikTokShopScraper, ProductInfo; url='https://www.tiktok.com/view/product/1732470931607225390'; p=ProductInfo(url=url,name='PH Product',price='N/A',rating='N/A',review_count='N/A',brand='N/A',market='philippines'); s=TikTokShopScraper(headless=False); r=s.scrape_product_reviews(p); s.save_to_csv(r,'ph_product_reviews.csv'); s.save_to_json(r,'ph_product_reviews.json'); print(f'Scraped {len(r)} reviews')"
```

Notes:
- Replace `url` with your target TikTok product URL.
- Set `market` to match the product market (`philippines`, `vietnam`, or `saudi_arabia`).
- Keep `headless=False` if you may need to solve a challenge manually.

## 📊 Output Format

The scraper generates a CSV file with the following structure:

| Column | Description |
|--------|-------------|
| `product_url` | Direct URL to the product page |
| `product_name` | Name of the Lancôme product |
| `reviewer_name` | Name/username of the reviewer |
| `rating` | Numerical rating (1-5 stars) |
| `review_text` | Full text of the review |
| `review_date` | Date when review was posted |
| `verified_purchase` | Whether purchase was verified |
| `helpful_votes` | Number of helpful votes |
| `review_id` | Unique identifier for the review |
| `country_market` | Market code (vn/sa) |
| `scrape_timestamp` | When the data was collected |

### Sample Output

```csv
product_url,product_name,reviewer_name,rating,review_text,review_date,verified_purchase,helpful_votes,review_id,country_market,scrape_timestamp
https://shop.tiktok.com/vn/product/123,Lancôme Advanced Génifique,UserXYZ,5,Amazing serum! Really improved my skin texture...,2024-08-15,Yes,12,abc123def456,vn,2024-08-21T21:30:00
```

## ⚙️ Configuration

### Environment Variables

```bash
# Optional proxy configuration
export PROXY_URL="http://username:password@proxy-server:port"

# Environment mode
export ENVIRONMENT="production"  # or "development"
```

### Config Customization

Edit `config.py` to modify:
- Target markets and languages
- Scraping delays and timeouts
- CSS selectors (if site structure changes)
- Output file names
- Browser options

## 🧪 Testing

```bash
# Run basic tests
python test_scraper.py

# Test specific functionality
python -c "from test_scraper import test_product_search; test_product_search()"
```

## 📋 Methodology Overview

The scraping approach follows a two-phase strategy:

### Phase 1: Product Discovery
1. **Search-based**: Query TikTok Shop search with "lancome"
2. **Brand page**: Navigate to official Lancôme store pages
3. **URL extraction**: Collect product URLs using multiple CSS selectors
4. **Validation**: Filter results to ensure Lancôme brand match

### Phase 2: Review Collection
1. **Page navigation**: Visit each product URL
2. **Dynamic loading**: Handle infinite scroll and "Load More" buttons
3. **Review extraction**: Parse review elements with fallback selectors
4. **Data normalization**: Clean and standardize collected data
5. **Deduplication**: Remove duplicate reviews

## 🛡️ Anti-Detection Measures

- **User Agent Rotation**: Random browser signatures
- **Request Delays**: Human-like browsing patterns
- **Session Management**: Proper cookie and session handling
- **Proxy Support**: IP rotation capabilities
- **Stealth Mode**: Disabled automation detection

## ⚠️ Limitations & Considerations

### Technical Limitations
- **Market Availability**: TikTok Shop may not be available in all target markets
- **Product Availability**: Lancôme products may be limited or unavailable
- **Site Changes**: Website structure changes may require selector updates
- **Rate Limiting**: Aggressive scraping may trigger anti-bot measures

### Ethical Considerations
- Respects `robots.txt` when present
- Implements reasonable delays between requests
- Uses public data only
- No authentication bypass attempts

### Legal Compliance
- Scraping for research/assessment purposes
- No commercial use without proper authorization
- Respects website terms of service

## 🔧 Troubleshooting

### Common Issues

**"No products found"**
```bash
# Solution: Check if TikTok Shop is available in target market
# Try with headless=False to see what's happening
python -c "TikTokShopScraper(headless=False).search_lancome_products('vietnam')"
```

**"ChromeDriver issues"**
```bash
# Solution: Update ChromeDriver
pip install --upgrade webdriver-manager
```

**"Access denied/blocked"**
```bash
# Solution: Use proxy or increase delays
# Edit config.py to increase MIN_DELAY and MAX_DELAY
```

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Run with visible browser
scraper = TikTokShopScraper(headless=False)
```

## 📈 Performance Optimization

### For Large Scale Scraping
1. Use headless mode: `headless=True`
2. Disable images: Add `--disable-images` to Chrome options
3. Use proxy rotation for IP diversity
4. Implement distributed scraping across multiple machines
5. Use checkpointing to resume interrupted sessions

### Memory Management
```python
# Process products in batches
for batch in batches(products, batch_size=5):
    reviews = process_batch(batch)
    save_checkpoint(reviews)
```

## 🤝 Contributing

This is a technical assessment project, but improvements are welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is created for educational and assessment purposes. Please respect the terms of service of the websites being scraped.

## 👨‍💻 Author

**Aymane Aallaoui**
- GitHub: [@aymaneallaoui](https://github.com/aymaneallaoui)
- LinkedIn: [aymane-aallaoui](https://praxe.design/)
- Email: Available upon request

## 🙏 Acknowledgments

- Selenium WebDriver team for excellent browser automation
- BeautifulSoup for HTML parsing capabilities
- The open-source community for various utilities used

---

**Note**: This scraper is designed as a technical demonstration. Always ensure compliance with website terms of service and applicable laws when scraping data.
