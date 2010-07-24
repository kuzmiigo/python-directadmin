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
import cmd
import getpass
import directadmin

__author__ = "Andrés Gattinoni <andresgattinoni@gmail.com>"
__version__ = "0.1"
__revision__ = "$Revision: 26 $"

class DAConsole (cmd.Cmd):

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

    prompt = "> "
    intro = "=============================\n" \
            "  DirectAdmin Console v.%s\n" \
            "=============================\n" \
            "Type help or ? for help.\n" \
            "Type quit, Ctrl+D or Ctrl+C to exit" % \
             __version__

    def __init__ (self):
        """Constructor

        Instanciates a new Directadmin Console.
        Adds all the available commands.
        """
        cmd.Cmd.__init__(self)

    def _get_api (self):
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

    def do_quit (self, s):
        """Quits the console"""
        return True

    def do_version (self, args=None):
        """Prints version information"""
        print "Directadmin Console, v.%s" % __version__

    def do_suspend (self, username):
        """Suspends a Directadmin user"""
        api = self._get_api()
        if api.suspend_account(username):
            print "User %s suspended" % username
        else:
            print "Failed to suspend user %s" % username

    def do_unsuspend (self, username):
        """Un-suspends a Directadmin user"""
        api = self._get_api()
        if api.unsuspend_account(username):
            print "User %s un-suspended" % username
        else:
            print "Failed to un-suspend user %s" % username

    def do_server_info (self, args=None):
        """Prints some basic server information"""
        api = self._get_api()
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

    do_EOF = do_quit

def main ():
    """Main

    This is the main function of the program.
    Handles the main loop and returns an
    exit status
    """
    console = DAConsole()
    try:
        console.cmdloop()
    except KeyboardInterrupt:
        console.do_quit(None)
    return 0

if __name__ == "__main__":
    sys.exit(main())
