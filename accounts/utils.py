from PIL import Image
from io import StringIO, BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile

def generate_thumbnail(file):
	print('file:', file)

	size = 75, 75
	im = Image.open(file)
	filename, ext = file.name.split('/')[-1].split('.')
	filename = filename + '-thumb.' + ext
	im.thumbnail(size)

	im.filename = filename
	suf = SimpleUploadedFile(filename, im.tobytes(), content_type='image/jpeg')
	print(suf.size)
	return suf, filename
