#coding: utf-8  

import soaplib  
from soaplib.core.service import rpc, DefinitionBase, soap  
from soaplib.core.model.primitive import String, Integer
from soaplib.core.server import wsgi  
from soaplib.core.model.clazz import Array

from functions import register, log_in, get_files, file_upload, file_read, file_del, user_search

class WebService(DefinitionBase): 
    @soap(String, _returns = Integer)  
    def search(self, username):
        info = user_search(username)
        return info

    @soap(String, String, _returns = Integer)  
    def reg(self, username, token):
        info = register(username, token)
        return info
 
    @soap(String, String, _returns = Integer)  
    def log(self, username, token):
        info = log_in(username, token)
        return info
        
    @soap(String, _returns = Array(Array(String)))  
    def files(self, username):
        info = get_files(username)
        return info
        
    @soap(String, String, String, _returns = Integer)  
    def upload(self, username, file_name, txt):
        info = file_upload(username, file_name, txt)
        return info
    
    @soap(String, String, _returns = Array(String))  
    def download(self, username, file_name):
        info = file_read(username, file_name)
        return info
    
    @soap(String, String)  
    def delete(self, username, file_name):
        file_del(username, file_name)
 
if __name__=='__main__':  
    try:  
        from wsgiref.simple_server import make_server  
        soap_application = soaplib.core.Application([WebService], 'tns')  
        wsgi_application = wsgi.Application(soap_application)  
        server = make_server('10.104.246.191', 7789, wsgi_application)  
        print 'soap server starting......'  
        server.serve_forever()  
    except ImportError:  
        print "Error: example server code requires Python >= 2.5"  
