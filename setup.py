#!/usr/bin/env python3
"""
Setup script for TikTok Shop Reviews Scraper
"""

import os
import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    else:
        print(f"✅ Python version: {sys.version.split()[0]}")


def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)


def setup_chrome_driver():
    """Setup ChromeDriver using webdriver-manager"""
    print("🚗 Setting up ChromeDriver...")
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        # Download and setup ChromeDriver
        driver_path = ChromeDriverManager().install()
        print(f"✅ ChromeDriver installed at: {driver_path}")
        
        # Test Chrome installation
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=options)
        driver.get('https://www.google.com')
        driver.quit()
        print("✅ Chrome browser test successful")
        
    except ImportError:
        print("⚠️ webdriver-manager not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "webdriver-manager"])
        print("✅ webdriver-manager installed")
    except Exception as e:
        print(f"❌ Chrome setup failed: {e}")
        print("Please make sure Google Chrome is installed on your system")
        return False
    
    return True


def create_directories():
    """Create necessary directories"""
    directories = [
        'logs',
        'output',
        'checkpoints',
        'sample_output'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"📁 Created directory: {directory}")


def create_sample_files():
    """Create sample configuration and output files"""
    
    # Create .env file template
    env_template = """
# TikTok Shop Scraper Configuration

# Environment (development/production)
ENVIRONMENT=development

# Optional: Proxy configuration
# PROXY_URL=http://username:password@proxy-server:port

# Optional: Custom delays (seconds)
# MIN_DELAY=2.0
# MAX_DELAY=5.0

# Optional: Output directory
# OUTPUT_DIR=./output
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_template.strip())
        print("✅ Created .env template file")
    
    # Create sample CSV header
    csv_header = "product_url,product_name,reviewer_name,rating,review_text,review_date,verified_purchase,helpful_votes,review_id,country_market,scrape_timestamp\n"
    
    sample_csv_path = "sample_output/aymane_aallaoui_tiktok_shop_reviews_sample.csv"
    if not os.path.exists(sample_csv_path):
        with open(sample_csv_path, 'w', encoding='utf-8') as f:
            f.write(csv_header)
            # Add sample row
            sample_row = (
                "https://shop.tiktok.com/vn/product/123456,"
                "Lancôme Advanced Génifique Serum 30ml,"
                "user123,"
                "5,"
                "Amazing product! Really improved my skin texture and appearance.,"
                "2024-08-15,"
                "Yes,"
                "12,"
                "abc123def456,"
                "vn,"
                "2024-08-21T21:30:00\n"
            )
            f.write(sample_row)
        print(f"✅ Created sample CSV: {sample_csv_path}")


def run_basic_test():
    """Run basic functionality test"""
    print("🧪 Running basic tests...")
    
    try:
        # Test imports
        from tiktok_shop_scraper import TikTokShopScraper
        from config import get_config
        from utils import clean_text, normalize_rating
        
        # Test configuration
        config = get_config()
        print(f"✅ Configuration loaded: {config.TARGET_BRAND}")
        
        # Test utility functions
        test_text = "  Test   review   text  "
        cleaned = clean_text(test_text)
        assert cleaned == "Test review text"
        
        test_rating = "4.5 stars"
        normalized = normalize_rating(test_rating)
        assert normalized == "4.5"
        
        print("✅ Utility functions working")
        
        # Test scraper initialization (without running)
        scraper = TikTokShopScraper(headless=True)
        print("✅ Scraper initialization successful")
        
        print("✅ All basic tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Basic test failed: {e}")
        return False


def print_usage_instructions():
    """Print usage instructions"""
    print("\n" + "="*60)
    print("🎉 Setup completed successfully!")
    print("="*60)
    print("\n📋 Usage Instructions:")
    print("\n1. Basic usage:")
    print("   python tiktok-shop-scraper.py")
    print("\n2. Development mode (visible browser):")
    print("   python -c \"from tiktok_shop_scraper import TikTokShopScraper; TikTokShopScraper(headless=False).run_complete_scraping()\"")
    print("\n3. Custom configuration:")
    print("   Edit config.py or .env file")
    print("\n4. Test specific market:")
    print("   python -c \"from tiktok_shop_scraper import TikTokShopScraper; scraper = TikTokShopScraper(); print(scraper.search_lancome_products('vietnam'))\"")
    print("\n📁 Output files will be saved as:")
    print("   - aymane_aallaoui_tiktok_shop_reviews_sample.csv")
    print("   - scraper.log")
    print("\n⚠️ Important Notes:")
    print("   - Ensure stable internet connection")
    print("   - TikTok Shop availability varies by region")
    print("   - Respect rate limits and website terms")
    print("   - Use VPN if needed for geo-restricted content")
    print("\n🔧 Troubleshooting:")
    print("   - Check logs in scraper.log file")
    print("   - Use headless=False to see browser actions")
    print("   - Increase delays in config.py if rate limited")
    print("\n" + "="*60)


def main():
    """Main setup function"""
    print("🚀 TikTok Shop Reviews Scraper - Setup")
    print("="*50)
    
    # Step 1: Check Python version
    check_python_version()
    
    # Step 2: Install dependencies
    install_dependencies()
    
    # Step 3: Setup ChromeDriver
    if not setup_chrome_driver():
        print("⚠️ Chrome setup failed, but you can continue if Chrome is already installed")
    
    # Step 4: Create directories
    create_directories()
    
    # Step 5: Create sample files
    create_sample_files()
    
    # Step 6: Run basic tests
    if not run_basic_test():
        print("⚠️ Some tests failed, but setup may still work")
    
    # Step 7: Print usage instructions
    print_usage_instructions()


if __name__ == "__main__":
    main()
