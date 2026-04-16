import aiofiles
import aiohttp

from core import settings


async def download_file(link: str, file_name: str, session: aiohttp.ClientSession) -> None:
    """Загрузка файла из сайта"""

    async with settings.SEMAPHORE:
        async with session.get(link) as response:
            response.raise_for_status()
            async with aiofiles.open(settings.DOWNLOAD_DIR/file_name, 'wb') as file:
                async for chunk in response.content.iter_chunked(1024):
                    await file.write(chunk)
