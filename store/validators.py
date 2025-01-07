from django.core.exceptions import ValidationError


def validate_file_size(file):
	file_size_kb = 10000

	if file.size > file_size_kb * 1024:
		raise ValidationError(f'Files cannot be larger than {file_size_kb}KB')
