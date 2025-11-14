"""Utils package for RhinoGuardians backend."""

from utils.notifications import NotificationService


# Expose test image helpers for tests that import from `utils`
from io import BytesIO

def create_test_image(
    mode: str = "RGB",
    size: tuple | None = None,
    color: tuple = (128, 128, 128),
    image_format: str = "JPEG",
    width: int | None = None,
    height: int | None = None,
) -> BytesIO:
    """
    Create an in-memory test image and return a BytesIO handle positioned at start.
    Supports either size=(w, h) or width=..., height=....
    Lazy-imports PIL to avoid hard dependency during module import.
    """
    from PIL import Image  # lazy import
    if size is None:
        if width is None or height is None:
            width, height = 64, 64
        size = (width, height)
    img = Image.new(mode, size, color=color)
    buf = BytesIO()
    img.save(buf, format=image_format)
    buf.seek(0)
    return buf

def create_test_image_file(
    filename: str = "test.jpg",
    mode: str = "RGB",
    size: tuple = (64, 64),
    color: tuple = (128, 128, 128),
):
    """
    Create a (filename, fileobj, mimetype) triple suitable for multipart uploads.
    """
    buf = create_test_image(mode=mode, size=size, color=color, image_format="JPEG")
    return (filename, buf, "image/jpeg")

__all__ = ["NotificationService", "create_test_image", "create_test_image_file"]
