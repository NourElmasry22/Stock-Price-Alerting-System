import requests
import logging
from decimal import Decimal
from datetime import datetime
from django.conf import settings
from django.utils import timezone
from .models import Stock, StockPrice
from .constants import STOCK_NAMES, BASE_PRICES, PREDEFINED_STOCKS
import random

logger = logging.getLogger(__name__)


class StockDataService:
    """Service class for fetching stock data from external APIs"""
    
    def __init__(self):
        self.api_key = settings.TWELVE_DATA_API_KEY
        self.base_url = "https://api.twelvedata.com"
    
    def fetch_stock_data(self, symbol):
        """Fetch current stock price for a given symbol"""
        if not self.api_key:
            logger.warning("No API key configured for Twelve Data")
            return self._get_mock_data(symbol)
        
        try:
            # Fetch real-time price
            url = f"{self.base_url}/price"
            params = {
                'symbol': symbol,
                'apikey': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'price' in data:
                price = Decimal(str(data['price']))
                
                # Get or create stock
                stock, created = Stock.objects.get_or_create(
                    symbol=symbol,
                    defaults={'name': f'{symbol} Inc.', 'is_active': True}
                )
                
                # Create price record
                stock_price = StockPrice.objects.create(
                    stock=stock,
                    price=price,
                    timestamp=timezone.now()
                )
                
                logger.info(f"Updated {symbol}: ${price}")
                return stock_price
            else:
                logger.error(f"No price data for {symbol}: {data}")
                return None
                
        except requests.RequestException as e:
            logger.error(f"API request failed for {symbol}: {e}")
            return self._get_mock_data(symbol)
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {e}")
            return None
    
    def fetch_detailed_stock_data(self, symbol):
        """Fetch detailed stock data including OHLCV"""
        if not self.api_key:
            return self._get_mock_detailed_data(symbol)
        
        try:
            # Fetch quote data
            url = f"{self.base_url}/quote"
            params = {
                'symbol': symbol,
                'apikey': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if all(key in data for key in ['close', 'open', 'high', 'low']):
                # Get or create stock
                stock, created = Stock.objects.get_or_create(
                    symbol=symbol,
                    defaults={'name': data.get('name', f'{symbol} Inc.'), 'is_active': True}
                )
                
                # Update stock name if we got it from API
                if 'name' in data and data['name']:
                    stock.name = data['name']
                    stock.save()
                
                # Create price record
                stock_price = StockPrice.objects.create(
                    stock=stock,
                    price=Decimal(str(data['close'])),
                    open_price=Decimal(str(data['open'])) if data.get('open') else None,
                    high_price=Decimal(str(data['high'])) if data.get('high') else None,
                    low_price=Decimal(str(data['low'])) if data.get('low') else None,
                    volume=int(data['volume']) if data.get('volume') else None,
                    timestamp=timezone.now()
                )
                
                logger.info(f"Updated detailed data for {symbol}")
                return stock_price
            else:
                logger.error(f"Incomplete data for {symbol}: {data}")
                return None
                
        except requests.RequestException as e:
            logger.error(f"API request failed for {symbol}: {e}")
            return self._get_mock_detailed_data(symbol)
        except Exception as e:
            logger.error(f"Error fetching detailed data for {symbol}: {e}")
            return None
    
    def fetch_all_stock_data(self):
        """Fetch data for all predefined stocks"""
        updated_stocks = []
        
        for symbol in PREDEFINED_STOCKS:
            try:
                result = self.fetch_detailed_stock_data(symbol)
                if result:
                    updated_stocks.append(symbol)
            except Exception as e:
                logger.error(f"Failed to update {symbol}: {e}")
        
        return updated_stocks
    
    def _get_mock_data(self, symbol):
        """Generate mock data for testing when API is not available"""
        
        base_price = BASE_PRICES.get(symbol, 100)
        # Add some random variation (+/- 5%)
        variation = random.uniform(-0.05, 0.05)
        price = Decimal(str(round(base_price * (1 + variation), 2)))
        
        # Get or create stock
        stock, created = Stock.objects.get_or_create(
            symbol=symbol,
            defaults={'name': f'{symbol} Inc.', 'is_active': True}
        )
        
        # Create price record
        stock_price = StockPrice.objects.create(
            stock=stock,
            price=price,
            timestamp=timezone.now()
        )
        
        logger.info(f"Created mock data for {symbol}: ${price}")
        return stock_price
    
    def _get_mock_detailed_data(self, symbol):
        """Generate detailed mock data"""
       
        base_price = BASE_PRICES.get(symbol, 100)
        
        # Generate OHLC data
        open_price = base_price * random.uniform(0.98, 1.02)
        close_price = open_price * random.uniform(0.95, 1.05)
        high_price = max(open_price, close_price) * random.uniform(1.0, 1.03)
        low_price = min(open_price, close_price) * random.uniform(0.97, 1.0)
        volume = random.randint(1000000, 50000000)
        
        stock, created = Stock.objects.get_or_create(
            symbol=symbol,
            defaults={'name': STOCK_NAMES.get(symbol, f'{symbol} Inc.'), 'is_active': True}
        )
        
        # Create price record
        stock_price = StockPrice.objects.create(
            stock=stock,
            price=Decimal(str(round(close_price, 2))),
            open_price=Decimal(str(round(open_price, 2))),
            high_price=Decimal(str(round(high_price, 2))),
            low_price=Decimal(str(round(low_price, 2))),
            volume=volume,
            timestamp=timezone.now()
        )
        
        logger.info(f"Created detailed mock data for {symbol}")
        return stock_price
    
    def initialize_stocks(self):        
        created_stocks = []
        for symbol in PREDEFINED_STOCKS:
            stock, created = Stock.objects.get_or_create(
                symbol=symbol,
                defaults={
                    'name': STOCK_NAMES.get(symbol, f'{symbol} Inc.'),
                    'is_active': True
                }
            )
            if created:
                created_stocks.append(symbol)
        
        return created_stocks