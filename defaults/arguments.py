from __future__ import unicode_literals

from abc import ABCMeta, abstractmethod



class APIArgumentSerializer(ABCMeta):
    @abstractmethod
    def to_api(self, value):
        pass
    
    @abstractmethod
    def to_builtin(self, value):
        pass



class APIArgument(ABCMeta):
    def __init__(self, name, description=None, required=True):
        self.name = name
        self.description = description
        self.required = required
    
    @abstractmethod
    @property
    def serializer_class(self):
        pass



class API(ABCMeta):
    @abstractmethod
    @property
    def method(self):
        """
        Return the exact name of the XML-RPC API mthod to call
        """
        pass

    @abstractmethod
    @property
    def arguments(self):
        """
        Return an (orderd) list of APIArrgument objects
        """
        pass
    
    @property
    def authenticate(self):
        """
        Defines whether or not we should authenticate when calling API
        """
        return True
    
    def transform_arguments(self, **kwargs):
        """
        Handler methos to trasnform an argument before processing
        :param kwargs: Named argument dictionary
        """
        return kwargs
    
    def validate_response(self, api, arguments, response):
        """
        Handler to validate the API response, Can be used 
        to raise an Exception to indicate fail, the pipeline will continue with the
        'transform_response' method
        :param argumentd: The dictionary containing the arguments that have been used to perfom the call
        :parma response: object
        """
        pass
    
    def transform_response(self, api, arguments, response):
        """
        Handler method to process the response, The output of this method
        will be returnd as the outpu of the API
        :param api: The api object that has been used fot the call
        :param argumentd: The dictionary containing the arguments
        """
        return response
