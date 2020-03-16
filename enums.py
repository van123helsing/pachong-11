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
