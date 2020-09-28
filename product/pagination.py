from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class CustiomLimitOffsetPagination(LimitOffsetPagination):
    limit_query_param = 'l'
    offset_query_param = 'o'
    default_limit = 1


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 1
    page_query_param = 'p'
