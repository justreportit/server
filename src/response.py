#!/usr/bin/env python3

"""
Generic http response generator
"""

import json

class HttpResponse():
    """
    Generic http response class
    """
    @staticmethod
    def resp(status, code, **kwargs):
        """
        Response generator to be used in conjunction with success or failure methods
        """
        data = {}
        error = {}
        for key, value in kwargs.items():
            if key == "error":
                error = value
            else:
                data.update({key: value})
        return {
            "statusCode": code,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "status": status,
                "data": data,
                "error": error
            })
        }

    @staticmethod
    def success(status, **kwargs):
        """
        Static method used for successful requests
        """
        return HttpResponse.resp("success", status.value, **kwargs)

    @staticmethod
    def failure(status, **kwargs):
        """
        Static method used for successful requests
        """
        return HttpResponse.resp("failure", status.value, **kwargs)
