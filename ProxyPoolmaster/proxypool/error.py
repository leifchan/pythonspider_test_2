# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 19:39:50 2018

@author: DELL
"""

class PoolEmptyError(Exception):
    
    def __init__(self):
        Exception.__init__(self)
    
    def __str__(self):
        return repr('代理池已经枯竭')