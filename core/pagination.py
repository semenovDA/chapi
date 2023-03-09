from rest_framework import pagination
from rest_framework.response import Response
from core.exceptions import BadRequestException

import logging
logger = logging.getLogger(__name__)

class LimitOffsetPagination(pagination.LimitOffsetPagination):
    limit_query_param = 'size'
    offset_query_param = 'from'
    max_limit = None

    def get_paginated_response(self, data):
        try:
            from_ = int(self.request.query_params.get('from', '0'))
            size = int(self.request.query_params.get('size', '10'))
        except:
            raise BadRequestException('Invaild query parameters')

        if(from_ < 0 or size <= 0):
            raise BadRequestException('from and size should be > 0 and not equals null')

        return Response(data)
