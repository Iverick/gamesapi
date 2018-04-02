# rest_framework import
from rest_framework.pagination import LimitOffsetPagination


class LimitOffsetPaginationWithMaxLimit(LimitOffsetPagination):
    '''
    Sets max limit for a number of object in a response.
    Restricts a response with 10 objects.
    '''
    max_limit = 10
