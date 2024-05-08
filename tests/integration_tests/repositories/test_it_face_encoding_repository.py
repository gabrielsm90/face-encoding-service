from os.path import join, dirname, abspath

from src.repositories.face_encoding_repository import FaceEncodingRepository

repo = FaceEncodingRepository()


def test_generate_face_encodings_returns_list_of_encodings_per_face():
    file_name = "img1.jpg"
    fixtures_dir = join(dirname(abspath(__file__)), "../../fixtures")
    file_path = join(fixtures_dir, file_name)
    with open(file_path, "rb") as file:
        image_data = file.read()

    result = repo.get_face_encodings(image_data)

    assert result is not None
