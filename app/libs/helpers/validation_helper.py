# ===========================================================================================
# ValidationHelper
# Dev: anh.vu
# ===========================================================================================

# ===========================================================================================

import re

from typing import Optional, List
from fastapi import UploadFile, File
from app.libs.exception.soa_error import SOA

from app.libs.pattern.creational.singleton import Singleton
from app.libs.exception.exceptions import ValidationException
from app.libs.helpers.image_helper import ImageHelper, MB_UNIT
from app.libs.helpers.file_helper import FileHelper, MB_UNIT

# ===========================================================================================

REGEX_HTML = "<(\"[^\"]*\"|'[^']*'|[^'\">])*>"

IMAGE_CONTENT_TYPE = ["IMAGE/JPG", "IMAGE/JPEG", "IMAGE/PNG", "IMAGE/TIFF", "IMAGE/JFIF"]
PDF_CONTENT_TYPE = ['APPLICATION/PDF']

# Main class ================================================================================

class ValidationHelper(metaclass=Singleton):
    """
        Class này triển khai các phương thức hỗ trợ cho việc validate giá trị của model
    """
    def __init__(self) -> None:
        """"""

    
    @staticmethod
    def validate_type_variable(name: str, value: str, type):
        if not isinstance(value, type):
            raise ValidationException(
                message=f'Validation error - {name}\'s type must be {str(type.__name__)}!'
            )


    @staticmethod
    def validate_string_length(name: str, value: str, max_length: int, min_length: int = 0):
        # Check null, rỗng, dài quá max_length
        # if value is None or len(value.strip()) == 0:
        #     raise ValidationException(
        #         message=f'Validation error - {name} is empty!'
        #     )
        
        if len(value.strip()) < min_length:
            raise ValidationException(
                message=f'Validation error - {name}\'s length must be greater than {min_length}!'
            )
        
        if len(value.strip()) > max_length:
            raise ValidationException(
                message=f'Validation error - {name}\'s length must be less than {max_length}!'
            )
        
    
    @staticmethod
    def validate_string_character(name: str, value: str, regex):
        if not re.match(regex, value):
            raise ValidationException(
                message=f'Validation error - {name}\'s character must be in {regex}!'
            )
        
    
    @staticmethod
    def validate_html(name: str, value: str):
        if re.match(REGEX_HTML, value):
            raise ValidationException(
                message=f'Validation error - {name}\'s character must not contain html!'
            )
        
    
    @staticmethod
    def validate_string_value(name: str, value: str, list_value):
        if value not in list_value:
            raise ValidationException(
                message=f'Validation error - {name} must be in {list_value}!'
            )
        
    
    @staticmethod
    def validate_bound_number(name: str, value: int,  max_number: int = None, min_number: int = None):
        if min_number is not None and int(value) < int(min_number):
            raise ValidationException(
                message=f'Validation error - {name} must be greater than or equal {min_number}!'
            )
        
        if max_number is not None and int(value) > int(max_number):
            raise ValidationException(
                message=f'Validation error - {name} must be less than or equal {max_number}!'
            )
        
    
    @staticmethod
    def validate_two_value(name_value_1: str, value_1: int, name_value_2: str, value_2: int):
        if value_1 and value_2 and int(value_1) > int(value_2):
            raise ValidationException(
                message=f'Validation error - {name_value_1} must be less than or equal {name_value_2}!'
            )


    @staticmethod
    async def validate_image_required(image: UploadFile = File(...)):
        await ValidationHelper.validate_image(image)
        return image
    

    @staticmethod
    async def validate_list_file(files: List[UploadFile] = File(...)):
        """"""
        for file in files:
            _file_data = await file.read()
            await file.seek(0)
            
            if ImageHelper.is_image_data(_file_data):
                await ValidationHelper.validate_image(image=file)
            elif FileHelper.is_pdf_data(file_data=_file_data):
                await ValidationHelper.validate_file(file=file)
                if b'/JavaScript' in _file_data:
                    raise ValidationException(
                        message='This file contains JavaScript!',
                        soa_error_code=SOA.FILE_CONTAIN_JS.code
                    )
            else:
                raise ValidationException(
                    message='Validation error - File upload is not image or pdf!'
                )
        return files
    

    @staticmethod
    async def validate_a_file(file: UploadFile = File(...)):
        """"""
        _file_data = await file.read()
        await file.seek(0)
        
        if ImageHelper.is_image_data(_file_data):
            await ValidationHelper.validate_image(image=file)
        elif FileHelper.is_pdf_data(file_data=_file_data):
            await ValidationHelper.validate_file(file=file)
            if b'/JavaScript' in _file_data:
                raise ValidationException(
                    message='This file contains JavaScript!',
                    soa_error_code=SOA.FILE_CONTAIN_JS.code
                )
        else:
            raise ValidationException(
                message='Validation error - File upload is not image or pdf!'
            )
        return file
    

    @staticmethod
    async def validate_list_image(images: Optional[List[UploadFile]] = []):
        for image in images:
            if image is not None:
                _image_data = await image.read()

                if image.content_type.upper() not in IMAGE_CONTENT_TYPE:
                    raise ValidationException(
                        message=f'Validation error - Image upload must be image, type in {IMAGE_CONTENT_TYPE}!'
                    )
                
                if not ImageHelper.is_image_data(image_data=_image_data):
                    raise ValidationException(
                        message='Validation error - Image upload must be image file!'
                    )
                
                if ImageHelper.get_size_image_data(image_data=_image_data, unit=MB_UNIT)[0] > 30:
                    raise ValidationException(
                        message=f'Validation error - Image upload\'s size must be less than {30}MB!'
                    )
                await image.seek(0)

        return images
    

    @staticmethod
    async def validate_list_pdf(files: Optional[List[UploadFile]] = []):
        for file in files:
            if file is not None:
                if file.content_type.upper() not in PDF_CONTENT_TYPE:
                    raise ValidationException(
                        message=f'Validation error - File upload must be pdf, type in {PDF_CONTENT_TYPE}!'
                    )

        return files
    

    @staticmethod
    async def validate_list_commitments(commitments: Optional[List[UploadFile]] = []):
        for file in commitments:
            if file is not None:
                if file.content_type.upper() not in PDF_CONTENT_TYPE:
                    raise ValidationException(
                        message=f'Validation error - File upload must be pdf, type in {PDF_CONTENT_TYPE}!'
                    )

        return commitments
    

    @staticmethod
    async def validate_list_petition(petitions: Optional[List[UploadFile]] = []):
        for file in petitions:
            if file is not None:
                if file.content_type.upper() not in PDF_CONTENT_TYPE:
                    raise ValidationException(
                        message=f'Validation error - File upload must be pdf, type in {PDF_CONTENT_TYPE}!'
                    )

        return petitions



    @staticmethod
    async def validate_image(image: Optional[UploadFile] = File(None)):
        if image is not None:
            _image_data = await image.read()

            if image.content_type.upper() not in IMAGE_CONTENT_TYPE:
                raise ValidationException(
                    message=f'Validation error - File upload must be image, type in {IMAGE_CONTENT_TYPE}!'
                )
            
            if not ImageHelper.is_image_data(image_data=_image_data):
                raise ValidationException(
                    message='Validation error - File upload must be image file!'
                )
            
            if ImageHelper.get_size_image_data(image_data=_image_data, unit=MB_UNIT)[0] > 30:
                raise ValidationException(
                    message=f'Validation error - File upload\'s size must be less than {30}MB!'
                )
            await image.seek(0)
        return image
    

    @staticmethod
    async def validate_file(file: Optional[UploadFile] = File(None)):
        if file is not None:
            _file_data = await file.read()

            if file.content_type.upper() not in PDF_CONTENT_TYPE:
                raise ValidationException(
                    message=f'Validation error - File upload must be pdf, type in {PDF_CONTENT_TYPE}!'
                )
            
            if not FileHelper.is_pdf_data(file_data=_file_data):
                raise ValidationException(
                    message='Validation error - File upload must be pdf file!'
                )
            
            if FileHelper.get_size_file_data(file_data=_file_data, unit=MB_UNIT)[0] > 30:
                raise ValidationException(
                    message=f'Validation error - File upload\'s size must be less than {30}MB!'
                )
            
            await file.seek(0)
        return file
