from PIL import Image
import mimetypes
from io import StringIO, BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile

def generate_thumbnail(file):
	size = 100, 100
	im = Image.open(file)
	filename, ext = file.name.split('/')[-1].split('.')
	mime = mimetypes.guess_type(file.name)
	filename = filename + '-thumb.' + ext
	im.thumbnail(size)
	memory_file = BytesIO()
	im.save(memory_file, ext)
	suf = SimpleUploadedFile(filename, memory_file.getvalue(), content_type=mime[0])
	return suf

def delete_from_s3(instances_list):
	for instance in instances_list:
		instance.storage.delete(name=instance.name)
	return instances_list