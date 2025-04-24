import adapters.base_adapter
import subprocess
import requests

class DumbHttpGetRequest(adapters.base_adapter.Adapter):
    ## will call request with pattern url?=param_name
    def __init__(self, url , param_name):
        self.url = url
        self.param_name = param_name



    def run(self, inp):
        r = requests.get(self.url, params={self.param_name: inp})
        return r.elapsed.microseconds
        