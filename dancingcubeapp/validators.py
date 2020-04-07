def validate_file_extension_for_map(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.zip']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. It has to be a zip.')

def validate_file_extension_for_music(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.ogg', '.mp3', '.wav']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Accepted extensions: ogg, mp3, wav')

def validate_file_extension_for_image(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.png', '.jpg', '.PNG', '.JPEG']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Accepted extensions: png, jpg')
