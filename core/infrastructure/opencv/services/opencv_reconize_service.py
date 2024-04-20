from core.domain.services.ia_award_service import IAAwardService
import cv2
import numpy as np

from core.domain.services.recognize_service import IRecognizeService


class OpenCVRecognizeService(IRecognizeService):
    # Recognize the image of the award using OpenCV, no face recognition
    async def recognize(self, images: list[bytes], image: bytes) -> bool:
        nparr = np.frombuffer(image, np.uint8)
        main_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        match = None
        score = 00.0

        return True

        for item in images:
            item_nparr = np.frombuffer(item, np.uint8)
            item_image = cv2.imdecode(item_nparr, cv2.IMREAD_COLOR)

            similarity = cv2.matchTemplate(
                main_image,
                item_image,
                cv2.TM_CCOEFF_NORMED,
            )[0][0]

            if match is None or similarity < score:
                match = item
                score = similarity

        return match is not None
