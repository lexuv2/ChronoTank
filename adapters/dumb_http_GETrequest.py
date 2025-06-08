import adapters.base_adapter
import subprocess
import requests

class DumbHttpGetRequest(adapters.base_adapter.Adapter):
    ## will call request with pattern url?=param_name
    def __init__(self, url , param_name):import adapters.base_adapter
import subprocess
import requests

class DumbHttpGetRequest(adapters.base_adapter.Adapter):
    ## will call request with pattern url?=param_name
    def __init__(self, url , param_name):
        self.url = url
        self.param_name = param_name



    def run(self, inp):
        base64pwd = f"admin:{inp}".encode("utf-8").hex()
        r = requests.get(self.url, headers={"Authorization": f"Basic {base64pwd}"})
        return r.elapsed.microseconds
        ()
        r = requests.get(self.url, headers={"Authorization": f"Basic {base64pwd}"})
        return r.elapsed.microseconds
        