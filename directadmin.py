#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Directadmin API

Python implementation of Directadmin Web API

For more information, visit:
http://www.directadmin.com/api.html

Author: Andrés Gattinoni <andresgattinoni@gmail.com>

To-Do:
- Add support for HTTPS
"""
__version__ = 0.1

import urllib2
import urllib
import urlparse
import base64

class ApiError (Exception):

    """
    API Error

    Generic exception for API error handling
    """

    pass

class Api (object):

    """

    Directadmin API

    Python implementation of Directadmin Web API

    For more information, visit:
    http://www.directadmin.com/api.html

    Author: Andrés Gattinoni <andresgattinoni@gmail.com>

    """
    
    _hostname = None
    _port = 0
    _username = None
    _password = None

    def __init__ (self, username, password, hostname, port=2222):

        """
        Constructor

        Parameters:
        username = username to login on Directadmin
        password = password to login on Directadmin
        hostname = Directadmin's hostname
        port = port on which Directadmin listens (default: 2222)
        """

        self._hostname = hostname
        self._port = int(port)
        self._username = username
        self._password = password

    def _executeCmd (self, cmd, parameters=None):

       """
       Execute command

       Executes a command of the API
       processes the result and returns it

       Parameters:
       cmd = command name
       parameters = dictionary of parameters (default: None)
       """
       if parameters:
           parameters = urllib.urlencode(parameters)

       request = urllib2.Request(self._getURL(cmd), parameters)
       request.add_header('Authorization', 'Basic ' + base64.b64encode(self._username + ':' + self._password))
       return self._handleResponse(urllib2.urlopen(request))

    def _getURL (self, cmd):
        
        """
        Get URL

        Returns the URL for a specific command
        """

        return 'http://%s:%d/%s' % \
               (self._hostname, \
                self._port, \
                cmd)

    def _handleResponse (self, response):

        """
        Handle response

        Takes the response string returned by
        Directadmin server, checks for errors
        and returns a python-friendly object
        """
        info = response.info()
        if info.getheader('X-DirectAdmin') == 'unauthorized':
            raise ApiError("Invalid username or password")    

        response =  urlparse.parse_qs(response.read())
        if 'error' in response:
            if 'details' in response:
                raise ApiError(response['details'][0])
            else:
                raise ApiError("Uknown error detected")
        elif 'list[]' in response:
            return response['list[]']
        return response 

    def listAllUsers (self):

        """
        List All Users

        Implements command CMD_API_SHOW_ALL_USERS

        Returns a list of all the users on the server

        Method info: http://www.directadmin.com/api.html#showallusers
        """

        return self._executeCmd("CMD_API_SHOW_ALL_USERS")

    def listUsers (self, reseller=None):

        """
        List Users

        Implements command CMD_API_SHOW_USERS

        Returns the list of users corresponding to the reseller logged in.
        If a reseller username is provided, it will return the users for it.

        Method info: http://www.directadmin.com/api.html#showusers
        """

        parameters = None
        if reseller:
            parameters = [('reseller', reseller)]

        return self._executeCmd("CMD_API_SHOW_USERS", parameters)

    def listResellers (self):

        """
        List Resellers

        Implements command CMD_API_SHOW_RESELLERS

        Returns the list of resellers on the server

        Method info: http://www.directadmin.com/api.html#showresellers
        """

        return self._executeCmd("CMD_API_SHOW_RESELLERS")

    def listAdmins (self):

        """
        List Admins

        Implements command CMD_API_SHOW_ADMINS

        Returns the list of all the admins on the server

        Method info: http://www.directadmin.com/api.html#showradmins
        """

        return self._executeCmd("CMD_API_SHOW_ADMINS")


    def getServerStats (self):
        
        """
        Get Server Statistics

        Implements command CMD_API_ADMIN_STATS

        Returns a dictionary with information of the server.

        Method info: http://www.directadmin.com/api.html#info
        """

        return self._executeCmd("CMD_API_ADMIN_STATS")

    def getUserUsage (self, user):
        
        """
        Get User Usage

        Implements command CMD_API_SHOW_USER_USAGE

        Returns a dictionary with the usage information for a user

        Method info: http://www.directadmin.com/api.html#info
        """

        return self._executeCmd("CMD_API_SHOW_USER_USAGE", [('user', user)])

    def getUserLimits (self, user):
        
        """
        Get User Limits

        Implements command CMD_API_SHOW_USER_CONFIG

        Returns a dictionary with the user's upper limits 
        and settings that defines their account

        Method info: http://www.directadmin.com/api.html#info
        """

        return self._executeCmd("CMD_API_SHOW_USER_CONFIG", [('user', user)])


    def getUserDomains (self, user):
        
        """
        Get User Domains

        Implements command CMD_API_SHOW_USER_DOMAINS

        Returns a list of domains owned by the user

        Method info: http://www.directadmin.com/api.html#info
        """

        return self._executeCmd("CMD_API_SHOW_USER_DOMAINS", [('user', user)])

    def listResellerPackages (self):

        """
        List Reseller Packages

        Implements command CMD_API_PACKAGES_RESELLER

        Returns the list of all available reseller packages

        Method info: http://www.directadmin.com/api.html#package
        """

        return self._executeCmd("CMD_API_PACKAGES_RESELLER")

    def getResellerPackage (self, package):

        """
        Get Reseller Package

        Implements command CMD_API_PACKAGES_RESELLER

        Returns the information of a reseller package

        Method info: http://www.directadmin.com/api.html#package
        """

        return self._executeCmd("CMD_API_PACKAGES_RESELLER", [('package', package)])

    def listUserPackages (self):

        """
        List User Packages

        Implements command CMD_API_PACKAGES_USER

        Returns the list of all available user packages

        Method info: http://www.directadmin.com/api.html#package
        """

        return self._executeCmd("CMD_API_PACKAGES_USER")

    def getUserPackage (self, package):

        """
        Get User Package

        Implements command CMD_API_PACKAGES_USER

        Returns the information of a user package

        Method info: http://www.directadmin.com/api.html#package
        """

        return self._executeCmd("CMD_API_PACKAGES_USER", [('package', package)])

