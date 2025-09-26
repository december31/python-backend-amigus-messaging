from rest_framework.pagination import LimitOffsetPagination


class PageBasedPagination(LimitOffsetPagination):
    page_query_param = 'page'
    page_size_query_param = 'page-size'

    def get_limit(self, request):
        if self.page_size_query_param in request.query_params:
            return int(request.query_params[self.page_size_query_param])
        return super().get_limit(request)

    def get_offset(self, request):
        if self.page_query_param in request.query_params:
            return (int(request.query_params[self.page_query_param]) - 1) * self.get_limit(request)
        return super().get_offset(request)
