from os import getenv

import requests


class FaceEncodingRepository:

    def get_face_encodings(self, image_content: bytes) -> list[list[float]]:
        response = requests.post(
            f"http://{self._get_face_encoder_service_host()}:8000/v1/selfie",
            files={"file": image_content},
        )
        response.raise_for_status()

        return response.json()

    @staticmethod
    def _get_face_encoder_service_host():
        return getenv("FACE_ENCODING_SERVICE_HOST", "localhost")
