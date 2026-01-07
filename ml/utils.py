from PIL import Image
from io import BytesIO

def get_uploaded_file(request):
    if 'file' not in request.files:
        return None, 'No file provided. Please send file with key "file"'

    file = request.files['file']

    if file.filename == '':
        return None, 'No file selected'

    return file, None


def validate_image(file_data):
    try:
        img = Image.open(BytesIO(file_data))
        img.verify()
        return True, None
    except Exception:
        return False, 'Uploaded file is not a valid image'


def get_image_format(file_data, allowed_ext):
    img = Image.open(BytesIO(file_data))
    image_format = img.format.lower()

    if image_format not in allowed_ext:
        return None, 'Unsupported image format'

    return image_format, None


def check_file_size(file_data, max_size):
    if len(file_data) > max_size:
        return False, 'File too large. Maximum size: 16MB'
    return True, None
