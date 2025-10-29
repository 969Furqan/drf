import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
test_data = [
    (
    "file.csv",
    "text/csv",
    b'title,genres,extra_data\ntest,comedy,{"directors":["name"]}\n',
    202,
    ),(
    "file.json",
    "application/json",
    b'[{"title": "test", "genres": ["comedy"], "extra_data":{"directors": ["name"]}}]',
    202,
    ),(
    "file.txt",
    "text/plain",
    b"This is a test.",
    400,
    ),
]

@pytest.mark.parametrize(
    "file_name, content_type, file_content, expected_status", test_data
)
@pytest.mark.django_db
def test_upload(client: APIClient, file_name: str, content_type: str, file_content: str, expected_status: int):
    url = reverse("Movies:upload_movie")
    upload_file = SimpleUploadedFile(name=file_name, content= file_content, content_type= content_type,  )
    
    response = client.post(url, {'file': upload_file}, format = 'multipart')
    
    assert response.status_code == expected_status