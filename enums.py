from enum import Enum


class PageType(Enum):
    HTML = 'HTML'
    BINARY = 'BINARY'
    DUPLICATE = 'DUPLICATE'
    FRONTIER = 'FRONTIER'


class DataType(Enum):
    PDF = 'PDF'
    DOC = 'DOC'
    DOCX = 'DOCX'
    PPT = 'PPT'
    PPTX = 'PPTX'


class MimeType(Enum):
    PDF = 'application/pdf'
    DOC =  'application/msword'
    DOCX = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    PPT =  'application/vnd.ms-powerpoint'
    PPTX = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
