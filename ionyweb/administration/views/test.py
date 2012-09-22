# -*- coding: utf-8 -*-
from djangorestframework.views import View
from djangorestframework.response import Response, ErrorResponse
from djangorestframework import status

class TestView(View):
    """
    Test of status code
    """

    def get(self, *args, **kwargs):
        """
        Handle GET requests, returning the form authentication if
        user is not authenticated.
        """
        status_code = kwargs['status_code']

        if status_code == '200':
            response = Response(status.HTTP_200_OK, {'html': '<h1>OK</h1>'})
        elif status_code == '400':
            raise ErrorResponse(status.HTTP_400_BAD_REQUEST, {'html': '<h1>BAD REQUEST</h1>'})
        elif status_code == '404':
            response = Response(status.HTTP_404_NOT_FOUND, {'msg': 'Objet introuvable',})
        elif status_code == '409':
            response = Response(status.HTTP_409_CONFLICT, {'msg': 'Existe déjà dans la BDD',})
        elif status_code == '500':
            response = Response(status.HTTP_500_INTERNAL_SERVER_ERROR, {'msg': 'Erreur serveur',})
            
        return self.render(response)
