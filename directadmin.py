#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Directadmin API - Python implementation of Directadmin Web API

Copyright (C) 2009, Andrés Gattinoni

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

=======================================================================

Proyect URL: http://code.google.com/p/python-directadmin/

For more information about Directadmin's Web API, visit:
http://www.directadmin.com/api.html

Author: Andrés Gattinoni <andresgattinoni@gmail.com>

To-Do:
- Add support for HTTPS

$Id$
"""

__author__ = "Andrés Gattinoni <andresgattinoni@gmail.com>"
__version__ = "$Revision$"

import urllib2
import urllib
import urlparse
import base64

_user_agent = "Python Directadmin"

class ApiError (Exception):
    """API Error

    Generic exception for API error handling
    """
    pass

class Api (object):
    """API

    Directadmin API implementation
    """
    _hostname = None
    _port = 0
    _username = None
    _password = None

    def __init__ (self, username, password, hostname, port=2222):
        """Constructor

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

    def _execute_cmd (self, cmd, parameters=None):
       """Execute command

       Executes a command of the API
       processes the result and returns it

       Parameters:
       cmd = command name
       parameters = list of tuples with parameters (default: None)
       """
       if parameters is not None:
           parameters = urllib.urlencode(parameters)

       request = urllib2.Request(self._get_url(cmd), parameters)

       # Directadmin's API requires Basic HTTP Authentication
       base_auth = base64.b64encode("%s:%s" % \
                                    (self._username, self._password))
       request.add_header('Authorization', 'Basic %s' % base_auth)

       # Identify our app with a custom User-Agent
       request.add_header('User-Agent', _user_agent)

       # Open the URL and handle the response
       return self._handle_response(urllib2.urlopen(request))

    def _get_url (self, cmd):
        """Get URL

        Returns the URL for a specific command
        """
        return 'http://%s:%d/%s' % \
               (self._hostname, \
                self._port, \
                cmd)

    def _handle_response (self, response):
        """Handle response

        Takes the response string returned by
        Directadmin server, checks for errors
        and returns a python-friendly object

        Parameters:
        response -- response object

        Returns a list or dictionary according
        to the method

        Raises ApiError on errors
        """
        # Get response headers to check if there
        # was any problem with login
        info = response.info()
        if info.getheader('X-DirectAdmin') == 'unauthorized':
            raise ApiError("Invalid username or password")

        # Parse the response query string
        response =  urlparse.parse_qs(response.read())

        # Check for 'error' flag
        if 'error' in response:
            # If 'error' is 0, the operation was successful
            if response['error'][0] == "0":
                return True
            # If not, check for details of the error
            else:
                if 'details' in response:
                    raise ApiError(response['details'][0])
                else:
                    raise ApiError("Uknown error detected")
        # If we got a 'list[]' keyword, we return only the list
        elif 'list[]' in response:
            return response['list[]']
        # On any other case return the whole structure
        else:
            return response

    def _on_off (self, bool):
        """Translates a boolean to "ON"/"OFF" """
        if bool:
            return "ON"
        else:
            return "OFF"

    def _yes_no (self, bool):
        """Translates a boolean to "yes"/"no" """
        if bool:
            return "yes"
        else:
            return "no"

    def create_admin (self, \
                      username, \
                      email, \
                      password, \
                      notify=True):
        """Create admin

        Implements command CMD_API_ACCOUNT_ADMIN

        Creates a new admin user

        Parameters:
        username -- Admin's username 4-8 alphanumeric characters
        email -- a valid email address
        password -- Admin's password, +5 ascii characters
        notify -- boolean: if true sends a notification email
        """
        notify = _yes_no(notify)
        parameters = [('action', 'create'), \
                      ('username', username), \
                      ('email', email), \
                      ('passwd', password), \
                      ('passwd2', password), \
                      ('notify', notify)]
        return self._execute_cmd("CMD_API_ACCOUNT_ADMIN", parameters)

    def create_reseller (self, \
                         username, \
                         email, \
                         passwd, \
                         domain, \
                         package=None, \
                         ip="shared", \
                         notify=True,
                         **keywords):
        """Create reseller

        Implements command CMD_API_ACCOUNT_RESELLER

        Creates a reseller assigning him a reseller package
        or with a custom configuration.
        If the package is sent as None, then the custom configuration
        will apply.

        Mandatory parameters:
            username        -- The Reseller's username. 4-8 characters, alphanumeric
            email           -- A valid email address
            password        -- The admins password. 5+ characters, ascii
            domain          -- A valid domain name in the form: domain.com
            package         -- One of the Reseller packages created by an admin
            ip              -- shared or assign. If shared, domain will use the
                               server's main ip. assign will use one of the reseller's ips
            notify          -- Boolean. If true, an email will be sent to email

        Custom configuration parameters (apply if package is None)
            bandwidth       -- Amount of bandwidth Reseller will be allowed to use.
                               Number, in Megabytes
            ubandwidth      -- ON or OFF. If ON, bandwidth is ignored and no limit is set
            quota           -- Amount of disk space Reseller will be allowed to use.
                               Number, in Megabytes
            uquota          -- ON or OFF. If ON, quota is ignored and no limit is set
            vdomains        -- Number of domains the reseller and his/her User's are
                               allowed to create
            uvdomains       -- ON or OFF. If ON, vdomains is ignored and no limit is set
            nsubdomains     -- Number of subdomains the reseller and his/her User's are
                               allowed to create
            unsubdomains    -- ON or OFF. If ON, nsubdomains is ignored and no limit is set
            ips             -- Number of ips that will be allocated to the Reseller upon
                               account during account
            nemails         -- Number of pop accounts the reseller and his/her User's are
                               allowed to create
            unemails        -- ON or OFF Unlimited option for nemails
            nemailf         -- Number of forwarders the reseller and his/her User's are
                               allowed to create
            unemailf        -- ON or OFF Unlimited option for nemailf
            nemailml        -- Number of mailing lists the reseller and his/her User's are
                               allowed to create
            unemailml       -- ON or OFF Unlimited option for nemailml
            nemailr         -- Number of autoresponders the reseller and his/her User's are
                               allowed to create
            unemailr        -- ON or OFF Unlimited option for nemailr
            mysql           -- Number of MySQL databases the reseller and his/her User's are
                               allowed to create
            umysql          -- ON or OFF Unlimited option for mysql
            domainptr       -- Number of domain pointers the reseller and his/her User's are
                               allowed to create
            udomainptr      -- ON or OFF Unlimited option for domainptr
            ftp             -- Number of ftp accounts the reseller and his/her User's are
                               allowed to create
            uftp            -- ON or OFF Unlimited option for ftp
            aftp            -- ON or OFF If ON, the reseller and his/her users will be
                               able to have anonymous ftp accounts.
            php             -- ON or OFF If ON, the reseller and his/her users will
                               have the ability to run php scripts.
            cgi             -- ON or OFF If ON, the reseller and his/her users will
                               have the ability to run cgi scripts in their cgi-bins.
            ssl             -- ON or OFF If ON, the reseller and his/her users will
                               have the ability to access their websites through secure https://.
            ssh             -- ON or OFF If ON, the reseller will be have an ssh account.
            userssh         -- ON or OFF If ON, the reseller will be allowed to create
                               ssh accounts for his/her users.
            dnscontrol      -- ON or OFF If ON, the reseller will be able to modify his/her
                               dns records and to create users with or without this option.
            dns             -- "OFF" or "TWO" or "THREE".
                               If OFF, no dns's will be created.
                               TWO: domain ip for ns1 and another ip for ns2.
                               THREE: domain has own ip. ns1 and ns2 have their own ips
            serverip        -- ON or OFF If ON, the reseller will have the ability to
                               create users using the servers main ip.
        """
        options = {'bandwidth' : 0,
                   'ubandwidth' : "OFF",
                   'quota' : 0,
                   'uquota' : "OFF", 
                   'vdomains' : 0, 
                   'uvdomains' : "OFF", 
                   'nsubdomains' : 0, 
                   'unsubdomains' : "OFF", 
                   'ips' : 0, 
                   'nemails' : 0, 
                   'unemails' : "OFF", 
                   'nemailf' : 0, 
                   'unemailf' : "OFF", 
                   'nemailml' : 0, 
                   'unemailml' : "OFF", 
                   'nemailr' : 0, 
                   'unemailr' : "OFF", 
                   'mysql' : 0, 
                   'umysql' : "OFF", 
                   'domainptr' : 0, 
                   'udomainptr' : "OFF", 
                   'ftp' : 0, 
                   'uftp' : "OFF", 
                   'aftp' : "OFF", 
                   'php' : "ON", 
                   'cgi' : "ON", 
                   'ssl' : "OFF", 
                   'ssh' : "OFF", 
                   'userssh' : "OFF", 
                   'dnscontrol' : "OFF", 
                   'dns' : "OFF", 
                   'serverip' : "OFF"}

        parameters = [('username', username), \
                      ('email', email), \
                      ('passwd', password), \
                      ('passwd2', password), \
                      ('domain', domain), \
                      ('ip', ip), \
                      ('notify', _yes_no(notify))]

        # Check if we will set a package or create a custom config
        if package is not None:
            parameters.append(('package', package))
        else:
            # Iterate through all the options
            for key, value in options:
                # If we are receiving the option as a parameter
                # then we append the value of the parameter
                if key in keywords:
                    parameters.append((key, keywords[key]))
                # else, we append the default value
                else:
                    parameters.append((key, value))

        return self._execute_cmd("CMD_API_ACCOUNT_RESELLER", parameters)


    def delete_account (self, username):
        """Delete account

        Implements command CMD_API_SELECT_USERS

        Deletes an account of *ANY* type

        Parameters:
        username -- name of the Admin/Reseller/User to delete
        """
        parameters = [('confirmed', 'Confirm'), \
                      ('delete', 'yes'), \
                      ('select0', username)]
        return self._execute_cmd("CMD_API_SELECT_USERS", parameters)

    def list_all_users (self):
        """List All Users

        Implements command CMD_API_SHOW_ALL_USERS

        Returns a list of all the users on the server

        Method info: http://www.directadmin.com/api.html#showallusers
        """
        return self._execute_cmd("CMD_API_SHOW_ALL_USERS")

    def list_users (self, reseller=None):
        """List Users

        Implements command CMD_API_SHOW_USERS

        Returns the list of users corresponding to the reseller logged in.
        If a reseller username is provided, it will return the users for it.

        Method info: http://www.directadmin.com/api.html#showusers
        """
        parameters = None
        if reseller is not None:
            parameters = [('reseller', reseller)]

        return self._execute_cmd("CMD_API_SHOW_USERS", parameters)

    def list_resellers (self):
        """List Resellers

        Implements command CMD_API_SHOW_RESELLERS

        Returns the list of resellers on the server

        Method info: http://www.directadmin.com/api.html#showresellers
        """
        return self._execute_cmd("CMD_API_SHOW_RESELLERS")

    def list_admins (self):
        """List Admins

        Implements command CMD_API_SHOW_ADMINS

        Returns the list of all the admins on the server

        Method info: http://www.directadmin.com/api.html#showradmins
        """
        return self._execute_cmd("CMD_API_SHOW_ADMINS")

    def get_server_stats (self):
        """Get Server Statistics

        Implements command CMD_API_ADMIN_STATS

        Returns a dictionary with information of the server.

        Method info: http://www.directadmin.com/api.html#info
        """
        return self._execute_cmd("CMD_API_ADMIN_STATS")

    def get_user_usage (self, user):
        """Get User Usage

        Implements command CMD_API_SHOW_USER_USAGE

        Returns a dictionary with the usage information for a user

        Method info: http://www.directadmin.com/api.html#info
        """
        return self._execute_cmd("CMD_API_SHOW_USER_USAGE", \
                                 [('user', user)])

    def get_user_limits (self, user):
        """Get User Limits

        Implements command CMD_API_SHOW_USER_CONFIG

        Returns a dictionary with the user's upper limits
        and settings that defines their account

        Method info: http://www.directadmin.com/api.html#info
        """
        return self._execute_cmd("CMD_API_SHOW_USER_CONFIG", \
                                 [('user', user)])

    def get_user_domains (self, user):
        """Get User Domains

        Implements command CMD_API_SHOW_USER_DOMAINS

        Returns a list of domains owned by the user

        Method info: http://www.directadmin.com/api.html#info
        """
        return self._execute_cmd("CMD_API_SHOW_USER_DOMAINS", \
                                 [('user', user)])

    def list_reseller_packages (self):
        """List Reseller Packages

        Implements command CMD_API_PACKAGES_RESELLER

        Returns the list of all available reseller packages

        Method info: http://www.directadmin.com/api.html#package
        """
        return self._execute_cmd("CMD_API_PACKAGES_RESELLER")

    def get_reseller_package (self, package):
        """Get Reseller Package

        Implements command CMD_API_PACKAGES_RESELLER

        Returns the information of a reseller package

        Method info: http://www.directadmin.com/api.html#package
        """
        return self._execute_cmd("CMD_API_PACKAGES_RESELLER", \
                                 [('package', package)])

    def list_user_packages (self):
        """List User Packages

        Implements command CMD_API_PACKAGES_USER

        Returns the list of all available user packages

        Method info: http://www.directadmin.com/api.html#package
        """
        return self._execute_cmd("CMD_API_PACKAGES_USER")

    def get_user_package (self, package):
        """Get User Package

        Implements command CMD_API_PACKAGES_USER

        Returns the information of a user package

        Method info: http://www.directadmin.com/api.html#package
        """
        return self._execute_cmd("CMD_API_PACKAGES_USER", \
                                 [('package', package)])
