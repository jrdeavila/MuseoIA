from core.domain.services.ia_award_service import IAAwardService
import cv2
import numpy as np

from core.domain.services.recognize_service import IRecognizeService


class OpenCVRecognizeService(IRecognizeService):
    # Recognize the image of the award using OpenCV, no face recognition
    async def recognize(self, images: list[bytes], image: bytes) -> bool:
        nparr = np.frombuffer(image, np.uint8)
        image_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        match = None
        score = 0

        for item in images:
            similarity = np.sum(np.abs(image_cv - item))

            if match is None or similarity < score:
                match = item
                score = similarity

        return match is not None
