import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import chronotank
import adapters.bin_stdin_perf as adapters
# import visualizers.live_update_plot_matplotlib as lp_mp
import visualizers.live_update_plot_plotly as lp_pl

# Initialize the adapter for the binary we're testing
adapter = adapters.BinWithStdinPerf("./examples/simple_binary/sample")

# Create a ChronoTank instance with performance settings
# - batch_size: Number of measurements per input configuration
# - threads: Parallel execution threads for faster analysis
# - verbose: Whether to print detailed progress information
ch = chronotank.ChronoTank(adapter, 
                           batch_size=100,
                            threads=8, 
                            verbose=False)

# Initialize the live plotting visualization
plot = lp_pl.LiveUpdatePlot(title="ChronoTank", x_label="Input Size", y_label="Time (s)")
plot.show()

# Phase 1: Determine the password length by testing different input lengths
# The correct length will likely show a timing anomaly (longer execution time)
for x in ch.find_len():
    print("\n\n=============")
    print(f"{len(x.input)} AVG:{x.avg}  STD:{x.STD()}")
    # Remove statistical outliers to get cleaner results
    without_outliers = x.remove_outliers()
    print("Without outliers")
    print(f"{len(x.input)} AVG:{without_outliers.avg}  STD:{without_outliers.STD()}")
    plot.update(without_outliers)

# Based on the timing analysis, we determine the password is 12 characters long

# Phase 2: Character-by-character brute force
# For each position, we test all possible characters and measure execution time
flag = ""
for i in range(0,12):
    plot.clear()
    results = []
    # Test all possible characters at the current position
    for x in ch.test_single_alphabet(flag, 12, pad_flag=True):
        plot.update(x)
        results.append(x)
    
    # The character with the highest average execution time is likely correct
    # (because it causes the comparison to continue longer before failing)
    max_result = max(results, key=lambda x: x.avg)
    flag += max_result.description
    print(f"Flag so far: {flag}")
    input("Press Enter to continue...")



