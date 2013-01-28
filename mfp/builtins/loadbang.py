#! /usr/bin/env python 
'''
loadbang.py -- on-load message emitter 

Copyright (c) 2013 Bill Gribble <grib@billgribble.com>
'''

from ..processor import Processor 
from ..bang import Bang, Uninit 
from ..main import MFPApp

class LoadBang (Processor):
    def __init__(self, init_type, init_args, patch, scope, name): 
        Processor.__init__(self, 1, 1, init_type, init_args, patch, scope, name)

    def trigger(self):
        self.outlets[0] = self.inlets[0]
        self.inlets[0] = Uninit

    def onload(self):
        self.send(Bang)

def register():
    MFPApp().register("loadbang", LoadBang)