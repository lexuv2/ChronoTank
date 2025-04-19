# ChronoTank

ChronoTank is a tool designed to assist in solving Reverse Engineering (RE) and PWN challenges using timing attacks. It provides a framework for analyzing timing data, visualizing results, and extending functionality through custom adapters.

## Features
- Analyze timing data to identify vulnerabilities.
- Visualize results with descriptive plots.
- Extend functionality by writing custom adapters.

---

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Required Python libraries (install via `requirements.txt` if provided)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ChronoTank.git
   cd ChronoTank
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage
import adapter from avaliable adapters and instance it
```python
from adapters import adapters.example_adapter
adapter = example_adapter.ExampleAdapter("binary path or url")
```
Later import chronotank and instance it with this adapter
```python
from chronotank import ChronoTank
ct = ChronoTank(adapter,batch_size=100,threads=10)
```

Than you can use functionality provided by chronotank:
 - `ct.find_len` - find the length of the input
 - `ct.find_flag` - find the flag
 - `ct.run_once_batch` - run a batch of tests

see `examples/` for more examples

---

## Writing Your Own Adapters

Adapters allow you to customize how data is processed. To create an adapter:


2. **Implement the Adapter**:
   - Define a class with methods to process your specific data format.
   - Example:
     ```python
     # filepath: /home/lexu/Documents/GitHub/ChronoTank/adapters/my_adapter.py
     class MyAdapter:
         def __init__(self, target):
             self.target = target
             
         def run(self,input):
            # Example: measure execution time
            start_time = time.time()
            # Run your process with self.target and self.input_data
            return end_time = time.time() ## return time it took to run the process     
     ```


