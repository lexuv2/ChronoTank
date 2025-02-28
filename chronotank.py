import threading
import tqdm
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.animation as animation

matplotlib.use("TkAgg")
class ChronoTank:
    def __init__(self, adapter, prefix="", suffix="",
                 max_flag_len=128, 
                 batch_size=8,
                threads=1,
                verbose=False,
                alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+{}|:<>?"
                ):
        self.adapter = adapter
        self.prefix = prefix
        self.suffix = suffix
        self.max_flag_len = max_flag_len
        self.batch_size = batch_size
        self.threads = threads
        self.verbose = verbose
        self.x_plot_data = []
        self.y_plot_data = []
        self.graph = None
        self.alphabet = alphabet
        plt.ion()




    
    def get_len_times(self):
        flag = ""
        times = {} 
        self.x_plot_data = []
        self.y_plot_data = []
        for i in range(1, self.max_flag_len):
            flag += "A"
            avg_time = 0
            for _ in range(0, self.batch_size):
                avg_time += self.adapter.run(self.prefix + flag + self.suffix)
            avg_time /= self.batch_size
            times[i] = avg_time
            self.x_plot_data.append(i)
            self.y_plot_data.append(avg_time)
            yield i, avg_time

    def get_flag(self,padd_flag=False):
        flag = ""
        for i in range(1, self.max_flag_len):
            max_time = 0
            max_char = ""
            for char in self.alphabet:
                avg_time = 0
                for _ in range(0, self.batch_size):
                    padded_flag = flag + char
                    if padd_flag:
                        padded_flag = padded_flag.ljust(self.max_flag_len, "A")
                    avg_time += self.adapter.run(self.prefix + padded_flag + self.suffix)
                avg_time /= self.batch_size
                if avg_time > max_time:
                    max_time = avg_time
                    max_char = char
            flag += max_char
            yield i,max_char

    def update_plot(self):
        # print("Updating with data: " + str(self.x_plot_data))
        if self.graph is not None:
            self.graph.remove()
        max_val = max(self.y_plot_data)
        min_val = min(self.y_plot_data)
        plt.ylim(min_val, max_val)
        plt.xlim(0, len(self.x_plot_data)+1)
        self.graph = plt.bar(self.x_plot_data, self.y_plot_data,color="r")[0]
        plt.draw()        
        plt.pause(0.2)












