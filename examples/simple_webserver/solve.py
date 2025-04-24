import sys
import os
import random
# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import time
import chronotank
import adapters.dumb_http_GETrequest as adapter
# import visualizers.live_update_plot_matplotlib as lp_mp
import visualizers.live_update_plot_plotly as lp_pl

# Initialize the adapter for the binary we're testing
adapter = adapter.DumbHttpGetRequest("http://192.168.1.119:5000/check_flag","flag")

# Create a ChronoTank instance with performance settings
# - batch_size: Number of measurements per input configuration
# - threads: Parallel execution threads for faster analysis
# - verbose: Whether to print detailed progress information
ch = chronotank.ChronoTank(adapter, 
                           batch_size=1,
                            threads=1, 
                            verbose=False)

# Initialize the live plotting visualization
plot = lp_pl.LiveUpdatePlot(title="ChronoTank", x_label="Input Size", y_label="Time (s)")
plot.show()


min_len = 10
max_len = 32
len_times = {}

for i in range(min_len, max_len):
    len_times[i] = chronotank.RunResult([], i,i,i)


## randomly choose len to test in a loop
i =0
len_arr = list(range(min_len, max_len))
while True:
    # time.sleep(0.01)
    i+=1
    len_to_test = random.choice(len_arr)
    len_arr.remove(len_to_test)
    if len_arr == []:
        len_arr = list(range(min_len, max_len))
    result = ch.run_once_batch("A" * len_to_test)
    len_times[len_to_test].add_runs(result.runs)
    # plot.update(len_times[len_to_test])
    print(f"Testing length {len_to_test}: {len_times[len_to_test].avg:.4f} seconds")
    if i % 10 == 0:
        plot.clear()
        for k in len_times:
            len_times[k] = len_times[k].remove_outliers()
            plot.update(len_times[k])

    


