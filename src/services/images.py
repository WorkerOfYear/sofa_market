from src.helpers.storage import StorageClient

class ImageService:
    def __init__(self, storage: StorageClient):
        self.storage = storage

    async def save_image(self, image: bytes, name: str) -> None:
        await self.storage.upload_file(image, name)
