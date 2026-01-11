from abc import ABC, abstractmethod

import aiofiles
from pathlib import Path


class StorageClient(ABC):
    @abstractmethod
    async def upload_file(self, file_bytes: bytes, destination: str | Path) -> None:
        pass


class LocalStorageClient(StorageClient):
    def __init__(self, base_path: str):
        self.base = Path(base_path).resolve()
        self.products_dir = "products"
        (self.base / self.products_dir).mkdir(parents=True, exist_ok=True)

    def get_product_image_path(self, product_id: int, filename: str) -> Path:
        return Path(self.products_dir) / str(product_id) / filename

    async def upload_file(self, file_bytes: bytes, destination: str | Path) -> None:
        full_path = self.base / destination
        full_path.parent.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(full_path, mode='wb') as f:
            await f.write(file_bytes)

    async def read_file(self, file_path: str | Path) -> bytes:
        async with aiofiles.open(self.base / file_path, mode='rb') as f:
            return await f.read()