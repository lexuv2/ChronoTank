import threading
import tqdm
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.animation as animation
import multiprocessing

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
        self.avg  = sum(runs) / len(runs)
        self.max  = max(runs)
        self.min  = min(runs)
        self.input = input
        self.description = description
        self.long_description = long_description
        
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
        return RunResult(filtered_runs, self.input)

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
                alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+{}|:<>?"
                ):
        """Initialize the ChronoTank instance.
        
        Args:
            adapter: Object with a run method accepting encoded input and returning timing results
            batch_size (int, optional): Number of runs per input. Defaults to 8.
            threads (int, optional): Number of threads to use. Defaults to 1.
            verbose (bool, optional): Whether to print detailed output. Defaults to False.
            alphabet (str, optional): Character set for testing. Defaults to alphanumeric and special chars.
        """
        self.adapter = adapter
        self.batch_size = batch_size
        self.threads = threads
        self.verbose = verbose
        self.alphabet = alphabet


    def run_once_batch(self, input):
        """Run the adapter multiple times on the same input and collect timing statistics.
        
        Args:
            input (str): The input string to test
            
        Returns:
            RunResult: Result object containing timing statistics
        """
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
        result = self.adapter.run(input.encode())
        return result
    
    def find_len(self, max_flag_len=100):
        """Find the optimal length by timing responses to inputs of increasing length.
        
        Args:
            max_flag_len (int, optional): Maximum length to test. Defaults to 100.
            
        Yields:
            RunResult: Result object for each tested length
        """
        flag = ""
        times = {} 
        for i in range(1, max_flag_len):
            flag += "A"
            result = self.run_once_batch(flag)
            result.description = f"{i}"
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















