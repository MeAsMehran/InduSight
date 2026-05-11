from rest_framework.pagination import PageNumberPagination

class DeviceLogPagination(PageNumberPagination):
    page_query_param = 'page_number'     # <-- override from `page`
    page_size_query_param = 'page_size'   # <-- override from `page_size`
    max_page_size = 200
