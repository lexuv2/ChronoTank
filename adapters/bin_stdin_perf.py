import adapters.base_adapter
import subprocess

class BinWithStdinPerf(adapters.base_adapter.Adapter):
    def __init__(self, binary_path):
        self.binary_path = binary_path



    def run(self, inp):
        command = f"perf stat {self.binary_path}"
        out = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=inp)

        for line in out.stderr.decode().split('\n'):
            if 'instructions' in line:
                return int(line.split()[0].replace(',', ''))
        print(out.stderr.decode())
        raise Exception("Instructions not found in perf output. Check if perf is installed and the binary is correct.")
        