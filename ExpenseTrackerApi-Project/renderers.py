# Global Renderers file

from rest_framework import renderers
import json


class UserRenderer(renderers.JSONRenderer):
    charset='utf-8'

    # This function is called whenever django rest framework is returning responses..So we can check the type of data and send the response here accordingly
    def render(self,data,accepted_media_type=None,renderer_context=None):
        response=''

        # We want to send error responses having key as error in json response and correct ones with data as key..
        # Below code is handling this part
        if "ErrorDetail" in str(data):
            response=json.dumps({'error':data})
        else:
            response=json.dumps({'data':data})
        return response
