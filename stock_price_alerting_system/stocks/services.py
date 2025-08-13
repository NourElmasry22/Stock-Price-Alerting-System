import requests
import logging
from decimal import Decimal
from django.conf import settings
from django.utils import timezone
from .models import Stock, StockPrice
from .constants import STOCK_NAMES, PREDEFINED_STOCKS

logger = logging.getLogger(__name__)

class StockDataService:
    def __init__(self):
        self.api_key = settings.TWELVE_DATA_API_KEY
        self.base_url = "https://api.twelvedata.com"
        if not self.api_key:
            warning_msg = "No API key configured for Twelve Data. Stock data fetching will not work."
            logger.warning(warning_msg)
            raise RuntimeWarning(warning_msg)

    def fetch_stock_data(self, symbol):
        """Fetch current stock price for given symbol."""
        try:
            url = f"{self.base_url}/price"
            params = {'symbol': symbol, 'apikey': self.api_key}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if 'price' not in data:
                logger.error(f"No price data for {symbol}: {data}")
                return None

            price = Decimal(str(data['price']))
            stock, _ = Stock.objects.get_or_create(
                symbol=symbol,
                defaults={'name': f'{symbol} Inc.', 'is_active': True}
            )
            stock_price = StockPrice.objects.create(
                stock=stock,
                price=price,
                timestamp=timezone.now()
            )
            logger.info(f"Updated {symbol}: ${price}")
            return stock_price

        except requests.RequestException as e:
            logger.error(f"API request failed for {symbol}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {e}")
            return None

    def fetch_detailed_stock_data(self, symbol):
        """Fetch detailed stock data including OHLCV for given symbol."""
        try:
            url = f"{self.base_url}/quote"
            params = {'symbol': symbol, 'apikey': self.api_key}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            required_keys = ['close', 'open', 'high', 'low']
            if not all(key in data for key in required_keys):
                logger.error(f"Incomplete data for {symbol}: {data}")
                return None

            stock, created = Stock.objects.get_or_create(
                symbol=symbol,
                defaults={'name': data.get('name', f'{symbol} Inc.'), 'is_active': True}
            )

            # Update stock name if present from API
            if data.get('name'):
                stock.name = data['name']
                stock.save()

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

        except requests.RequestException as e:
            logger.error(f"API request failed for {symbol}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error fetching detailed data for {symbol}: {e}")
            return None

    def fetch_all_stock_data(self):
        """Fetch detailed data for all predefined stocks."""
        updated_stocks = []
        for symbol in PREDEFINED_STOCKS:
            try:
                result = self.fetch_detailed_stock_data(symbol)
                if result:
                    updated_stocks.append(symbol)
            except Exception as e:
                logger.error(f"Failed to update {symbol}: {e}")
        return updated_stocks

    def initialize_stocks(self):
        """Create stock entries for all predefined symbols if they don't exist."""
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
