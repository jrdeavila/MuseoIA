class IRecognizeService:
    async def recognize(self, image: bytes, images: list[bytes]) -> bool:
        raise NotImplementedError()
