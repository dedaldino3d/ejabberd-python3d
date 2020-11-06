from __future__ import unicode_literals

from abc import ABCMeta, abstractmethod
from enum import Enum as BaseClassEnum


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



class Enum(BaseClassEnum):
    @classmethod
    def get_by_name(cls, name):
        return getattr(cls, name, None)
    
    @classmethod
    def get_by_value(cls, value):
        return cls(value)



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


class EjabberdBaseAPI(ABCMeta):
    @abstractmethod
    def echo(self, sentence):
        pass
    
    @abstractmethod
    def registered_users(self, host):
        pass
    
    @abstractmethod
    def register(self, user, host, password):
        pass
    
    @abstractmethod
    def unregister(self, user, host):
        pass
    
    @abstractmethod
    def change_password(self, user, host, password, newpass):
        pass
    
    @abstractmethod
    def check_password_hash(self, user, host, password):
        pass
    
    @abstractmethod
    def set_nickname(sel, user, host, nickname):
        pass
    
    @abstractmethod
    def conneected_users(self):
        pass
    
    @abstractmethod
    def conneected_users_info(self):
        pass
    
    @abstractmethod
    def conneected_users_number(self):
        pass
    
    @abstractmethod
    def user_sessions_info(self):
        pass
    
    @abstractmethod
    def muc_online_rooms(self, host=None):
        pass
    
    @abstractmethod
    def muc_online_rooms(self. host=None):
        pass

    @abstractmethod
    def create_room(self, name, service, host):
        pass
    
    @abstractmethod
    def destroy_room(self, name, service, host):
        pass
    
    @abstractmethod
    def get_room_options(self, name, service):
        pass
    
    @abstractmethod
    def change_room_option(self, name, service, option, value):
        pass
    
    @abstractmethod
    def set_room_affiliation(self, name, service, jid, affiliation):
        pass
    
    @abstractmethod
    def get_room_affiliations(self, name, service):
        pass

    @abstractmethod
    def add_roster_item(self, localuser, localserver, user, server, nick, group, subs):
        pass
    
    @abstractmethod
    def remove_rosteritem(self, localuser, localserver, user, server):
        pass
    
    @abstractmethod
    def get_roster(self, user, host):
        pass
