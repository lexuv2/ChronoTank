# Simple Timing Attack Example

This example demonstrates a basic timing attack against a binary that performs a string comparison when checking a password.

## Vulnerability Explanation

The C++ program (`sample.cpp`) contains a vulnerable string comparison function `comapre_string()` (note the typo). The vulnerability stems from how the function compares strings:

1. It checks each character one by one
2. It returns `false` as soon as it finds a mismatched character
3. It only returns `true` after checking all characters

This creates a **timing side-channel**: when more characters match at the beginning of the string, the program takes slightly longer to execute. By measuring these tiny time differences, an attacker can determine the correct password character by character.

## How solve_simple_binary.py Works

### Setup Phase
1. The script imports the necessary libraries and adds the project root to the Python path
2. It initializes a `BinWithStdinPerf` adapter for the compiled binary (`sample`)
3. It creates a `ChronoTank` instance with parameters:
   - `batch_size=100`: Each input is tested 100 times to gather statistically significant timing data
   - `threads=8`: Uses 8 parallel threads to speed up data collection
   - `verbose=False`: Suppresses detailed output
4. A live plot is initialized to visualize the timing results in real-time

### Password Length Detection
1. The script calls `ch.find_len()` which tests inputs of varying lengths
2. For each length, it calculates:
   - Average execution time (`AVG`)
   - Standard deviation (`STD`)
3. It removes statistical outliers for more reliable results
4. The timing data is visualized on the live plot
5. A significant spike in execution time is observed with inputs of 12 characters, revealing the password length

### Character-by-Character Discovery
1. The script begins with an empty string `flag = ""`
2. For each of the 12 positions:
   - Clears the plot for the current position
   - Calls `ch.test_single_alphabet()` which tries every possible character in the current position
   - Each character's timing results are added to the plot and stored in `results`
   - Finds the character with the highest average execution time using `max(results, key=lambda x: x.avg)`
   - This character is most likely correct because it causes the comparison to continue longer
   - The discovered character is added to the flag
   - The current progress is printed
   - Script pauses for user to review before proceeding to the next position

### Technical Details
- The `pad_flag=True` parameter ensures inputs are padded to maintain consistent length
- ChronoTank automatically tests various character sets (lowercase, uppercase, digits, symbols)
- The statistical analysis handles noise and system fluctuations to isolate the timing signal

## Running the Example

1. Compile the sample binary:
   ```
   g++ sample.cpp -o sample
   ```

2. Run the solver script:
   ```
   python solve_simple_binary.py
   ```

3. The script will display a live plot of execution times and print the discovered password characters.

## Mitigation

To prevent timing attacks:

- Use constant-time comparison functions provided by cryptographic libraries
- Avoid early returns in security-sensitive comparisons
- Consider adding random delays or using other techniques to obscure timing patterns

Remember that timing attacks are a real threat to any security system that processes sensitive information.
