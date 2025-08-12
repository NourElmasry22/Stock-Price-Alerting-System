# tasks.py
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.conf import settings
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from .services import StockDataService

logger = logging.getLogger(__name__)


def fetch_all_stock_data():
    """Fetch stock data for all predefined stocks"""
    try:
        service = StockDataService()
        updated_stocks = service.fetch_all_stock_data()
        logger.info(f"Fetched data for {len(updated_stocks)} stocks: {updated_stocks}")
    except Exception as e:
        logger.error(f"Error fetching stock data: {e}")


def fetch_stock_data_for_symbol(symbol):
    """Fetch data for a specific stock symbol"""
    try:
        service = StockDataService()
        result = service.fetch_detailed_stock_data(symbol)
        if result:
            logger.info(f"Updated {symbol}: ${result.price}")
        else:
            logger.warning(f"No data received for {symbol}")
    except Exception as e:
        logger.error(f"Error fetching data for {symbol}: {e}")


def initialize_stock_data():
    """Initialize stock data"""
    try:
        service = StockDataService()
        created_stocks = service.initialize_stocks()
        logger.info(f"Initialized {len(created_stocks)} stocks")

        updated_stocks = service.fetch_all_stock_data()
        logger.info(f"Fetched initial data for {len(updated_stocks)} stocks")
    except Exception as e:
        logger.error(f"Error initializing stock data: {e}")


def start_scheduler():
    """Start APScheduler"""
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # Fetch all stocks every 5 minutes
    scheduler.add_job(
        fetch_all_stock_data,
        trigger=IntervalTrigger(minutes=5),
        id="fetch_all_stock_data",
        replace_existing=True,
    )

    # Initialize once at startup
    scheduler.add_job(
        initialize_stock_data,
        trigger=IntervalTrigger(seconds=5),
        id="initialize_stock_data",
        replace_existing=True,
    )

    register_events(scheduler)
    scheduler.start()
    logger.info("APScheduler started.")
