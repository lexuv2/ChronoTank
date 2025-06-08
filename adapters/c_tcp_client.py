import adapters.base_adapter
import subprocess

class c_tcp_client(adapters.base_adapter.Adapter):
    def __init__(self):
        pass



    def run(self, inp):
        command = f"./client"
        out = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=inp)

        for i,line in enumerate(out.stdout.decode().split('\n')):
            # if self.correct_string in line:
            #     return "Found Flag"
            # if 'instructions' in line:
            #     return int(line.split()[0].replace(',', ''))
            # print (f"line: {line}")
            if i == 1:
                ret = float(line.split()[0].replace(',', ''))*1000000
                # print (f"ret: {ret}")
                return ret
        return -1
            