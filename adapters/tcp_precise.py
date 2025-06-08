import adapters.base_adapter
import subprocess

class tcp_precise(adapters.base_adapter.Adapter):
    def __init__(self,ip, port):
        self.ip = ip
        self.port = port
        pass



    def run(self, inp):
        command = f"/home/lexu/Documents/GitHub/ChronoTank/adapters/http_request_precise/raw_tcp "+ self.ip + " "+self.port + " "  +inp.decode()
        # inp_done = (" 192.168.1.136 12345 " +inp.decode()).encode()
        # print (f"inp: {inp_done}")
        out = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # print (f"out: {out}")
        success = False
        ret = -1
        for i,line in enumerate(out.stdout.decode().split('\n')):
            # if self.correct_string in line:
            #     return "Found Flag"
            # if 'instructions' in line:
            #     return int(line.split()[0].replace(',', ''))
            # print (f"line: {line}")
            if "success" in line:
                success = True
            if i == 1:
                ret = float(line.split()[2].replace(',', ''))
                # print (f"ret: {ret}")
                
        if success:
            return ret
        else:
            return -1
            