import asyncio
from driver import MemedroidFirefox
import logging
from settings import logging_level


async def main():
    logging.getLogger().setLevel(logging_level)
    logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s")
    logging.getLogger("selenium").setLevel(logging.INFO)
    logging.getLogger("urllib3").setLevel(logging.INFO)

    await MemedroidFirefox().cycle()


if __name__ == "__main__":
    asyncio.run(main())
