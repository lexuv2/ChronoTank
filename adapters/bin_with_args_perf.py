import adapters.base_adapter
import subprocess

class BinWithArgsPerf(adapters.base_adapter.Adapter):
    def __init__(self, binary_path, correct_string):
        self.binary_path = binary_path
        self.correct_string = correct_string



    def run(self, inp):
        command = f"perf stat {self.binary_path} {inp}"
        out = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        for line in out.stderr.decode().split('\n'):
            if self.correct_string in line:
                return "Found Flag"
            if 'instructions' in line:
                return int(line.split()[0].replace(',', ''))
        return -1
            