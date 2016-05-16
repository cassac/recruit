from PIL import Image
import mimetypes
from io import StringIO, BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile

def generate_thumbnail(file):
	size = 100, 100
	im = Image.open(file)
	filename = file.name.split('/')[-1].split('.')[0]
	mime = mimetypes.guess_type(file.name)[0]
	file_type = mime.split('/')[-1]
	filename = filename + '-thumb.' + file_type
	im.thumbnail(size)
	memory_file = BytesIO()
	im.save(memory_file, file_type)
	suf = SimpleUploadedFile(filename, memory_file.getvalue(), content_type=mime)
	return suf

def delete_from_s3(instances_list):
	for instance in instances_list:
		instance.storage.delete(name=instance.name)
	return instances_list
