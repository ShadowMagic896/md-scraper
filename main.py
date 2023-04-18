import asyncio
from driver import MemedroidFirefox


async def main():
    await MemedroidFirefox().cycle()

if __name__ == "__main__":
    asyncio.run(main())