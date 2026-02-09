#!/usr/bin/env python3
"""Import-friendly wrapper around tiktok-shop-scraper.py."""

import importlib.util
from pathlib import Path


_SCRIPT_PATH = Path(__file__).with_name("tiktok-shop-scraper.py")
_SPEC = importlib.util.spec_from_file_location("tiktok_shop_scraper_impl", _SCRIPT_PATH)
_MODULE = importlib.util.module_from_spec(_SPEC)
assert _SPEC and _SPEC.loader
_SPEC.loader.exec_module(_MODULE)

ProductInfo = _MODULE.ProductInfo
ReviewInfo = _MODULE.ReviewInfo
TikTokShopScraper = _MODULE.TikTokShopScraper
main = _MODULE.main

