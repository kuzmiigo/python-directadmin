#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
An interactive command line console to interact with Directadmin Control Panel

This file is part of python-directadmin.

python-directadmin is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

python-directadmin is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with python-directadmin.  If not, see <http://www.gnu.org/licenses/>.

Author: Andrés Gattinoni
$Id$

Usage:
./daconsole.py

To-Do:
- Add configuration file
- Add more commands
"""
import sys
import getpass
import directadmin

__author__ = "Andrés Gattinoni <andresgattinoni@gmail.com>"
__version__ = "0.1"
__revision__ = "$Revision$"

class CommandError (Exception):
    """Command Error

    Basic exception. 
    This should be thrown when an error 
    ocurrs during the execution of a command.
    It will be caught by the command handler,
    to display the error and return the prompt
    """
    pass

class Console (object):

    """Console

    Base console class.
    Implements the basic functionality
    of an interactive console. 
    It allows to register commands with its handlers.

    It provides the user prompt and handles its input.
    """

    _prompt = '> '
    _loop = True
    _handlers = {}

    def __init__ (self):
        """Constructor

        Initializes the console with its basic
        commands (currently "quit" and "help")
        """
        # Add the basic commands
        self.add_handler("quit", self.quit, "Quit the console")
        self.add_handler("help", self.printHelp, "Print command information")

    def main_loop (self):
        """Main loop

        Main console loop. Once the Console
        object is instanciated, the main_loop 
        will start providing the prompt and
        handling commands.
        """
        try:
            while self._loop:
                self._handle_cmd(self._read())
        except KeyboardInterrupt, e:
            self.quit()

    def quit (self, args=None):
        """Quit

        Native command. Quits the console.
        """
        print "Bye bye..."
        self._loop = False

    def printHelp (self, args=None):
        """Print help

        Native command. 
        Prints all the commands registered
        on the console instance.
        """
        print "Available commands:"
        for token in sorted(self._handlers.keys()):
            print "%s    - %s" % (token, self._handlers[token]['info'])
            

    def add_handler (self, token, handler, info=None):
        """Add handler

        Adds a new command handler to the console.

        Parameters:
        token - string - command token (one word)
        handler - callable - command callback
        info - string - information about the command to display
                        with the "help" command.
        """
        self._handlers[token] = {'handler': handler, \
                                 'info': info }

    def _read (self):
        """Read

        Reads user input
        """
        return raw_input(self._prompt)

    def _handle_cmd (self, input):
        """Handle command

        Handles user input

        Parameters:
        input - string - user's input
        """
        args = input.split(" ")
        action = args.pop(0)
        if action in self._handlers:
            try:
                self._handlers[action]['handler'](args)
            except CommandError, e:
                print "Command error: %s" % (str(e))
        else:
            print "Unknown command '%s'. Type 'help' for a list of commands." % action


class DAConsole (Console):

    """Directadmin Console

    Interactive console implementation to interact
    with Directadmin Control Panel
    """
    _username = None
    _password = None
    _hostname = None
    _port = 2222
    _https = False

    _api = None

    def __init__ (self):
        """Constructor

        Instanciates a new Directadmin Console.
        Adds all the available commands.
        """
        Console.__init__(self)
        self.version()
        self.add_handler("version", self.version, "Print version information")
        self.add_handler("connect", self.connect, "Connect to a Directadmin Server")
        self.add_handler("suspend", self.suspend, "Suspends a user on Directadmin")
        self.add_handler("unsuspend", self.unsuspend, "Un-suspends a user on Directadmin")
        self.add_handler("server_info", self.server_info, "Prints statistical information about the server")

    def _getApi (self):
        """Get API

        Returns an instance of Directadmin API.
        It takes care of asking for connection and login
        information to the user.
        """
        if self._api is None:
            # Check hostname and port
            if self._hostname is None:                
                host = raw_input('Host [localhost]: ')
                if host is None:
                    self._hostname = "localhost"
                else:
                    self._hostname = host

                port = raw_input('Port [%d]: ' % self._port)
                try:
                    port = int(port)
                except:
                    port = 0
                if port > 0:
                    self._port = port

                https = raw_input('Use HTTPS? (yes/no) [no]: ')
                self._https = (https.lower() == 'yes')

            # Check username
            if self._username is None:
                self._username = raw_input('Username: ')        

            # Check password
            if self._password is None:
                self._password = getpass.getpass('Password: ')

            self._api = directadmin.Api(self._username, \
                                        self._password, \
                                        self._hostname, \
                                        self._port, \
                                        self._https)
        
        return self._api

    def connect (self, args):
        """Connect

        Connect to a Directadmin Server
        """
        self._getApi()

    def version (self, args=None):
        """Version

        Prints version information
        """
        print "Directadmin Console, v.%s" % __version__

    def suspend (self, args):
        """Suspend

        Command: suspends a Directadmin user
        """
        if not args:
            raise CommandError("Missing user to suspend")

        api = self._getApi()
        user = args.pop(0)
        if api.suspend_account(user):
            print "User %s suspended" % user
        else:
            print "Failed to suspend user %s" % user

    def unsuspend (self, args):
        """Unsuspend

        Command: un-suspends a Directadmin user
        """
        if not args:
            raise CommandError("Missing user to un-suspend")

        api = self._getApi()
        user = args.pop(0)
        if api.unsuspend_account(user):
            print "User %s un-suspended" % user
        else:
            print "Failed to un-suspend user %s" % user

    def server_info (self, args=None):
        """Server info

        Prints server information
        """
        api = self._getApi()
        info = api.get_server_stats()
        print "Hostname:\t%s" % self._hostname
        print "Load average:\t%s" % info['loadavg'][0]
        print "Bandwidth:\t%d GB" % (long(info['bandwidth'][0]) / 1024)
        print "RX:\t%s" % info['RX'][0]
        print "TX:\t%s" % info['TX'][0]
        print "Quota:\t%d GB" % (long(info['quota'][0]) / 1024)
        print "Domains:\t%d" % int(info['vdomains'][0])
        print "Subdomains:\t%d" % int(info['nsubdomains'][0])
        print "Users:\t%d" % int(info['nusers'][0])
        print "Resellers:\t%d" % int(info['nresellers'][0])
        print "Discs information:"
        print "Filesystem\tBlocks\tAvailable\tUsed\t% used\tMount point"
        for key in info.keys():
            if key.startswith('disk'):
                print "%s\t%s\t%s\t%s\t%s\t%s" % \
                      (info[key][0]['filesystem'], \
                       info[key][0]['blocks'], \
                       info[key][0]['available'], \
                       info[key][0]['used'], \
                       info[key][0]['usedpercent'], \
                       info[key][0]['mounted'])

def main ():
    """Main

    This is the main function of the program.
    Handles the main loop and returns an
    exit status
    """
    console = DAConsole()
    console.main_loop()
    return 0

if __name__ == "__main__":
    sys.exit(main())
