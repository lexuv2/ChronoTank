import threading
import tqdm
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.animation as animation
import multiprocessing
import time

import numpy as np
import sys
class RunResult:
    """ Result of one batch run of the adapter.
    
    Attributes:
        runs (list): Sorted list of times for each run
        input: Input used for the run
        avg (float): Average time for the run
        max (float): Maximum time for the run
        min (float): Minimum time for the run
        description (str): Short description used in axis plot
        long_description (str): Detailed description displayed when hovering over plot elements
    """

    def __init__(self, runs , input, description="",long_description=""):
        """Initialize a RunResult object.
        
        Args:
            runs (list): List of execution times
            input: Input used for the run
            description (str, optional): Short description for plot labels. Defaults to "".
            long_description (str, optional): Detailed description for hover info. Defaults to "".
        """
        self.runs = sorted(runs)
        if len(runs) == 0:
            self.avg = 0
            self.max = 0
            self.min = 0
        else:
            self.avg  = sum(runs) / len(runs)
            self.max  = max(runs)
            self.min  = min(runs)
        
        self.input = input
        self.description = description
        self.long_description = long_description




    
    def add_runs(self, runs):
        """Add additional runs to the existing list and recalculate statistics.
        
        Args:
            runs (list): List of additional execution times
        """
        self.runs.extend(runs)
        self.runs.sort()
        self.avg = sum(self.runs) / len(self.runs)
        self.max = max(self.runs)
        self.min = min(self.runs)

    

        
    def STD(self):
        """Calculate the standard deviation of the runs.
        
        Returns:
            float: Standard deviation value
        """
        avg = self.avg
        n = len(self.runs)
        return (sum((x - avg) ** 2 for x in self.runs) / n) ** 0.5
    
    def percentile(self, percent):
        """Calculate the specified percentile of the runs.
        
        Args:
            percent (float): Percentile to calculate (0-100)
            
        Returns:
            float: Value at the specified percentile
            
        Raises:
            ValueError: If percentile is not between 0 and 100
        """
        if percent < 0 or percent > 100:
            raise ValueError("Percentile must be between 0 and 100")
        index = int(percent / 100 * len(self.runs))
        return self.runs[index]

    def remove_outliers(self, threshold=1.5):
        if len(self.runs) == 0:
            return self
        """Remove outliers from the runs using the IQR method.
        
        Args:
            threshold (float, optional): Multiplier for IQR to determine outlier bounds. Defaults to 1.5.
            
        Returns:
            RunResult: New RunResult object with outliers removed
        """
        q1 = self.percentile(25)
        q3 = self.percentile(75)
        iqr = q3 - q1
        lower_bound = q1 - threshold * iqr
        upper_bound = q3 + threshold * iqr
        filtered_runs = [x for x in self.runs if lower_bound <= x <= upper_bound]
        ret = RunResult(filtered_runs, self.input)
        ret.description = self.description
        ret.long_description = self.long_description
        return ret

    def __str__(self):
        """String representation of the RunResult.
        
        Returns:
            str: Formatted string with key properties
        """
        return f"RunResult(input={self.input}, avg={self.avg}, max={self.max}, min={self.min})"


class ChronoTank:
    """A tool for timing-based analysis of functions or services.
    
    This class provides functionality to measure execution times of an adapter
    with various inputs, useful for timing attacks or performance analysis.
    
    Attributes:
        adapter: Object with a run method that accepts encoded input
        batch_size (int): Number of times each input is run per batch
        threads (int): Number of parallel threads to use
        verbose (bool): Whether to print detailed output
        alphabet (str): Characters to test when constructing inputs
    """

    def __init__(self, adapter,
                 batch_size=8,
                threads=1,
                verbose=False,
                alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+{}|:<>?",
                    save_file_name=""
                ):
        """Initialize the ChronoTank instance.
        
        Args:
            adapter: Object with a run method accepting encoded input and returning timing results
            batch_size (int, optional): Number of runs per input. Defaults to 8.
            threads (int, optional): Number of threads to use. Defaults to 1.
            verbose (bool, optional): Whether to print detailed output. Defaults to False.
            alphabet (str, optional): Character set for testing. Defaults to alphanumeric and special chars.
        """
        self.save_file_name = save_file_name
        if save_file_name == "":
            self.save_file_name = f"run{time.strftime('%Y%m%d_%H%M%S')}.csv"
        else:
            self.save_file_name = save_file_name+".csv"
        ## clear file and then open as append
        self.last_run_time = time.time_ns()
        self.save_file = open(self.save_file_name, "w")
        self.save_file.write("")
        self.save_file.close()
        self.save_file = open(self.save_file_name, "a")
        # input of the run, time taken, and time taken after the previous run
        self.save_file.write(f"input,time_taken,time_delta\n")
        self.adapter = adapter
        self.batch_size = batch_size
        self.threads = threads
        self.verbose = verbose
        self.alphabet = alphabet
        self.last_avg_update_time = time.time()
        self.tested_num = 0
        self.last_avg_update_num = 0
        self.tests_per_minute = 0.0
        self.start_time = time.time()
        self.combined_run_times = []
        

    def __del__(self):
        """Close the save file when the object is deleted."""
        if self.save_file:
            self.save_file.close()
    def run_once_batch(self, input,single_thread=False):
        """Run the adapter multiple times on the same input and collect timing statistics.
        
        Args:
            input (str): The input string to test
            
        Returns:
            RunResult: Result object containing timing statistics
        """
        if single_thread:
            results = []
            for _ in range(self.batch_size):
                result = self.run_one(input)
                results.append(result)
            
            result = RunResult(results, input)
            
        else:
            inputs = [input] * self.batch_size
            with multiprocessing.Pool(processes=self.threads) as pool:
                results = pool.map(self.run_one, inputs)

            result = RunResult(results, input)
        return result


    def run_one(self, input):
        """Run the adapter once with the given input.
        
        Args:
            input (str): The input string to test
            
        Returns:
            float: Execution time for this run
        """
        self.tested_num += 1
        result = self.adapter.run(input.encode())
        
        # save the result to the file
        delta = time.time_ns() - self.last_run_time
        self.save_file.write(f"{input.replace('\n','').replace('\r','')},{result},{delta}\n")
        self.last_run_time = time.time_ns()

        # self.combined_run_times.append(result)
        self.combined_run_times.append(result)
        # if self.last_print_time + 1 < time.time():
            # self.last_print_time = time.time()

        self.tests_per_minute = (self.tested_num) / ((time.time() - self.start_time) / 60)
                # print((time.time() - self.last_avg_update_time) / 60)
            
        #calculate standard deviation from self.combined_run_times
        std = np.std(self.combined_run_times)

        print(f"\r Testing: {input}, Time: {result}, Tested num: {self.tested_num}, TPM: {self.tests_per_minute:.2f} STD={std}", end="")

        return result

    def find_len(self, max_flag_len=100,start_len=1):
        """Find the optimal length by timing responses to inputs of increasing length.
        
        Args:
            max_flag_len (int, optional): Maximum length to test. Defaults to 100.
            
        Yields:
            RunResult: Result object for each tested length
        """
        flag = ""
        times = {} 
        for i in range(start_len, max_flag_len):
            flag += "A"
            result = self.run_once_batch(flag)
            result.description = f"{i}"
            result.long_description = f"len: {i}"
            avg_time = result.avg
            times[i] = avg_time
            yield result
            if self.verbose:
                print(f"Length: {i}, Time: {avg_time}")

    
    def test_single_alphabet(self, flag, flag_len, pad_flag=False, prefix="", suffix=""):
        """Test each character of the alphabet appended to the current flag.
        
        Args:
            flag (str): Current partial flag string
            flag_len (int): Expected total length of the flag
            pad_flag (bool, optional): Whether to pad the flag to full length. Defaults to False.
            prefix (str, optional): String to prepend to the flag. Defaults to "".
            suffix (str, optional): String to append after the test character. Defaults to "".
            
        Yields:
            RunResult: Result object for each tested character
        """
        for char in self.alphabet:
            padded_flag = prefix + flag + char + suffix
            if pad_flag:
                padded_flag = padded_flag.ljust(flag_len, "A")
            result = self.run_once_batch(padded_flag)
            result.description = f"{char}"
            result.long_description = f"{padded_flag}"
            yield result















