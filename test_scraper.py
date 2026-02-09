#!/usr/bin/env python3
"""
Test cases for TikTok Shop Reviews Scraper
"""

import unittest
import time
from unittest.mock import Mock, patch, MagicMock
from selenium.webdriver.common.by import By

from tiktok_shop_scraper import TikTokShopScraper, ProductInfo, ReviewInfo
from config import get_config
from utils import clean_text, normalize_rating, validate_review_data, deduplicate_reviews


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions"""
    
    def test_clean_text(self):
        """Test text cleaning function"""
        # Test normal text
        self.assertEqual(clean_text("  Hello   World  "), "Hello World")
        
        # Test text with newlines
        self.assertEqual(clean_text("Hello\nWorld\r\n"), "Hello World")
        
        # Test empty text
        self.assertEqual(clean_text(""), "")
        self.assertEqual(clean_text(None), "")
        
        # Test quotes escaping
        text_with_quotes = 'He said "Hello World"'
        cleaned = clean_text(text_with_quotes)
        self.assertIn('""', cleaned)
    
    def test_normalize_rating(self):
        """Test rating normalization"""
        # Test numeric ratings
        self.assertEqual(normalize_rating("4.5"), "4.5")
        self.assertEqual(normalize_rating("5 stars"), "5.0")
        
        # Test star symbols
        self.assertEqual(normalize_rating("★★★★★"), "5")
        self.assertEqual(normalize_rating("⭐⭐⭐"), "3")
        
        # Test invalid ratings
        self.assertEqual(normalize_rating(""), "N/A")
        self.assertEqual(normalize_rating("abc"), "abc")
    
    def test_validate_review_data(self):
        """Test review data validation"""
        # Valid review
        valid_review = {
            'product_url': 'https://shop.tiktok.com/vn/product/123',
            'reviewer_name': 'TestUser',
            'review_text': 'This is a valid review with enough content'
        }
        self.assertTrue(validate_review_data(valid_review))
        
        # Invalid review - missing fields
        invalid_review = {
            'product_url': 'https://shop.tiktok.com/vn/product/123'
        }
        self.assertFalse(validate_review_data(invalid_review))
        
        # Invalid review - short text
        short_review = {
            'product_url': 'https://shop.tiktok.com/vn/product/123',
            'reviewer_name': 'TestUser',
            'review_text': 'Short'
        }
        self.assertFalse(validate_review_data(short_review))
    
    def test_deduplicate_reviews(self):
        """Test review deduplication"""
        reviews = [
            {
                'reviewer_name': 'User1',
                'review_text': 'Great product!',
                'review_date': '2024-08-01',
                'product_url': 'https://example.com/1'
            },
            {
                'reviewer_name': 'User1',
                'review_text': 'Great product!',
                'review_date': '2024-08-01',
                'product_url': 'https://example.com/1'
            },  # Duplicate
            {
                'reviewer_name': 'User2',
                'review_text': 'Different review',
                'review_date': '2024-08-02',
                'product_url': 'https://example.com/1'
            }
        ]
        
        unique_reviews = deduplicate_reviews(reviews)
        self.assertEqual(len(unique_reviews), 2)


class TestScraperConfiguration(unittest.TestCase):
    """Test scraper configuration"""
    
    def test_config_loading(self):
        """Test configuration loading"""
        config = get_config()
        
        # Test required fields
        self.assertIn('vietnam', config.MARKETS)
        self.assertIn('saudi_arabia', config.MARKETS)
        self.assertEqual(config.TARGET_BRAND, 'lancome')
        self.assertIsInstance(config.USER_AGENTS, list)
        self.assertGreater(len(config.USER_AGENTS), 0)
    
    def test_market_configuration(self):
        """Test market-specific configuration"""
        config = get_config()
        
        # Test Vietnam market
        vietnam_config = config.MARKETS['vietnam']
        self.assertEqual(vietnam_config['code'], 'vn')
        self.assertEqual(vietnam_config['language'], 'vi-VN')
        
        # Test Saudi Arabia market
        sa_config = config.MARKETS['saudi_arabia']
        self.assertEqual(sa_config['code'], 'sa')
        self.assertEqual(sa_config['language'], 'ar-SA')


class TestScraperCore(unittest.TestCase):
    """Test core scraper functionality"""
    
    def setUp(self):
        """Setup test environment"""
        self.scraper = TikTokShopScraper(headless=True)
    
    def test_scraper_initialization(self):
        """Test scraper initialization"""
        self.assertIsNotNone(self.scraper)
        self.assertEqual(self.scraper.headless, True)
        self.assertIn('vietnam', self.scraper.markets)
        self.assertIn('saudi_arabia', self.scraper.markets)
    
    def test_get_tiktok_shop_url(self):
        """Test TikTok Shop URL generation"""
        vn_url = self.scraper.get_tiktok_shop_url('vietnam')
        self.assertEqual(vn_url, 'https://shop.tiktok.com/vn')
        
        sa_url = self.scraper.get_tiktok_shop_url('saudi_arabia')
        self.assertEqual(sa_url, 'https://shop.tiktok.com/sa')
        
        # Test invalid market
        with self.assertRaises(ValueError):
            self.scraper.get_tiktok_shop_url('invalid_market')
    
    def test_random_delay(self):
        """Test random delay function"""
        start_time = time.time()
        self.scraper.random_delay(0.1, 0.2)
        end_time = time.time()
        
        delay = end_time - start_time
        self.assertGreaterEqual(delay, 0.1)
        self.assertLessEqual(delay, 0.3)  # Allow some tolerance
    
    @patch('tiktok_shop_scraper._MODULE.webdriver.Chrome')
    def test_setup_driver(self, mock_chrome):
        """Test driver setup"""
        mock_driver = Mock()
        mock_chrome.return_value = mock_driver
        
        driver = self.scraper.setup_driver('vietnam')
        
        # Verify Chrome was called
        mock_chrome.assert_called_once()
        
        # Verify anti-detection script was executed
        mock_driver.execute_script.assert_called_once()


class TestProductExtraction(unittest.TestCase):
    """Test product information extraction"""
    
    def setUp(self):
        """Setup test environment"""
        self.scraper = TikTokShopScraper(headless=True)
    
    def test_extract_product_info(self):
        """Test product information extraction"""
        # Create mock element
        mock_element = Mock()
        mock_element.tag_name = 'a'
        mock_element.get_attribute.return_value = 'https://shop.tiktok.com/vn/product/123'
        
        # Mock child elements
        mock_name_element = Mock()
        mock_name_element.text = 'Lancôme Advanced Génifique'
        
        mock_price_element = Mock()
        mock_price_element.text = '₫1,500,000'
        
        mock_element.find_element.side_effect = [
            mock_name_element,  # First call for name
            mock_price_element  # Second call for price
        ]
        
        product = self.scraper.extract_product_info(mock_element, 'vietnam')
        
        self.assertIsInstance(product, ProductInfo)
        self.assertEqual(product.name, 'Lancôme Advanced Génifique')
        self.assertEqual(product.price, '₫1,500,000')
        self.assertEqual(product.market, 'vietnam')


class TestReviewExtraction(unittest.TestCase):
    """Test review extraction functionality"""
    
    def setUp(self):
        """Setup test environment"""
        self.scraper = TikTokShopScraper(headless=True)
        self.sample_product = ProductInfo(
            url='https://shop.tiktok.com/vn/product/123',
            name='Lancôme Test Product',
            price='₫1,000,000',
            rating='4.5',
            review_count='100',
            brand='Lancôme',
            market='vietnam'
        )
    
    def test_extract_review_info(self):
        """Test review information extraction"""
        # Create mock review element
        mock_element = Mock()
        
        # Mock sub-elements
        mock_reviewer = Mock()
        mock_reviewer.text = 'TestUser123'
        
        mock_rating = Mock()
        mock_rating.get_attribute.return_value = '5'
        mock_rating.text = '5 stars'
        
        mock_text = Mock()
        mock_text.text = 'This is an amazing product! Highly recommend.'
        
        mock_date = Mock()
        mock_date.text = '2024-08-15'
        
        mock_helpful = Mock()
        mock_helpful.text = '12'
        
        # Setup find_element to return appropriate mocks
        def mock_find_element(by, selector):
            if 'reviewer-name' in selector or 'username' in selector:
                return mock_reviewer
            elif 'rating' in selector or 'star' in selector:
                return mock_rating
            elif 'review-text' in selector or 'comment-text' in selector:
                return mock_text
            elif 'review-date' in selector or 'timestamp' in selector:
                return mock_date
            elif 'helpful' in selector or 'likes' in selector:
                return mock_helpful
            else:
                raise Exception("Element not found")
        
        mock_element.find_element.side_effect = mock_find_element
        
        review = self.scraper.extract_review_info(mock_element, self.sample_product)
        
        self.assertIsInstance(review, ReviewInfo)
        self.assertEqual(review.reviewer_name, 'TestUser123')
        self.assertEqual(review.rating, '5')
        self.assertEqual(review.review_text, 'This is an amazing product! Highly recommend.')
        self.assertEqual(review.product_name, 'Lancôme Test Product')


class TestIntegration(unittest.TestCase):
    """Integration tests (require actual browser)"""
    
    def setUp(self):
        """Setup test environment"""
        self.scraper = TikTokShopScraper(headless=True)
    
    def test_save_to_csv(self):
        """Test CSV saving functionality"""
        import tempfile
        import os
        import csv
        
        # Create sample reviews
        sample_reviews = [
            ReviewInfo(
                product_url='https://shop.tiktok.com/vn/product/123',
                product_name='Test Product',
                reviewer_name='TestUser',
                rating='5',
                review_text='Great product!',
                review_date='2024-08-15',
                verified_purchase='Yes',
                helpful_votes='10',
                review_id='test123',
                country_market='vn',
                scrape_timestamp='2024-08-21T10:00:00'
            )
        ]
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp_file:
            tmp_filename = tmp_file.name
        
        try:
            # Save to CSV
            self.scraper.save_to_csv(sample_reviews, tmp_filename)
            
            # Verify file was created and contains data
            self.assertTrue(os.path.exists(tmp_filename))
            
            # Read and verify content
            with open(tmp_filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]['product_name'], 'Test Product')
            self.assertEqual(rows[0]['reviewer_name'], 'TestUser')
            
        finally:
            # Cleanup
            if os.path.exists(tmp_filename):
                os.unlink(tmp_filename)


def run_manual_tests():
    """Run manual tests that require user interaction"""
    print("\n🧪 Running Manual Tests")
    print("=" * 40)
    
    # Test 1: Browser setup
    print("\n1. Testing browser setup...")
    try:
        scraper = TikTokShopScraper(headless=True)
        driver = scraper.setup_driver('vietnam')
        driver.get('https://www.google.com')
        title = driver.title
        driver.quit()
        print(f"✅ Browser test passed: {title}")
    except Exception as e:
        print(f"❌ Browser test failed: {e}")
    
    # Test 2: TikTok Shop accessibility
    print("\n2. Testing TikTok Shop accessibility...")
    try:
        scraper = TikTokShopScraper(headless=True)
        driver = scraper.setup_driver('vietnam')
        url = scraper.get_tiktok_shop_url('vietnam')
        driver.get(url)
        time.sleep(3)
        title = driver.title
        driver.quit()
        print(f"✅ TikTok Shop accessible: {title}")
    except Exception as e:
        print(f"❌ TikTok Shop access failed: {e}")
        print("This may be normal if TikTok Shop is geo-restricted")
    
    print("\n✅ Manual tests completed")


def main():
    """Main test runner"""
    print("🧪 TikTok Shop Scraper - Test Suite")
    print("=" * 50)
    
    # Run unit tests
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run manual tests
    try:
        run_manual_tests()
    except KeyboardInterrupt:
        print("\n⏹️ Manual tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Manual tests failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Test suite completed!")
    print("\nTo run specific tests:")
    print("  python -m unittest test_scraper.TestUtilityFunctions")
    print("  python -m unittest test_scraper.TestScraperCore.test_scraper_initialization")


if __name__ == '__main__':
    main()
