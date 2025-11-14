import io
from PIL import Image

def _make_image_bytes():
    img = Image.new("RGB", (64, 64), color=(128, 128, 128))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf

def test_upload_image_minimal(client):
    img_bytes = _make_image_bytes()
    files = {"file": ("test.jpg", img_bytes, "image/jpeg")}
    data = {"gps_lat": "-23.8859", "gps_lng": "31.5205"}
    resp = client.post("/upload/", files=files, data=data)
    assert resp.status_code == 200
    body = resp.json()
    # Current simplified endpoint response
    assert body.get("status") == "success"
    assert body.get("filename") in ("test.jpg", "test_image.jpg")