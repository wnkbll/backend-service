from concurrent.futures import ProcessPoolExecutor

from src.core.logger import configure_logging


async def create_start_app_handler() -> ProcessPoolExecutor:
    configure_logging()
    pool = ProcessPoolExecutor(max_workers=1)

    return pool


async def create_stop_app_handler(pool: ProcessPoolExecutor) -> None:
    pool.shutdown()
