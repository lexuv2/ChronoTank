import matplotlib.pyplot as plt
import threading
from matplotlib.widgets import Cursor  # Add Cursor for interactivity

class LiveUpdatePlot:
    def __init__(self, title="Live Update Plot", x_label="X", y_label="Y"):
        """Initialize the live update plot."""
        self.data_x = []
        self.data_y = []
        self.lock = threading.Lock()  # Thread-safe updates

        # Initialize the plot
        plt.ion()  # Turn on interactive mode
        self.fig, self.ax = plt.subplots(figsize=(12, 6))  # Increase figure size
        self.fig.patch.set_facecolor('black')  # Set figure background to black
        self.ax.set_facecolor('black')  # Set axes background to black
        self.ax.set_title(title, color='white')  # Title in white
        self.ax.set_xlabel(x_label, color='white')  # X label in white
        self.ax.set_ylabel(y_label, color='white')  # Y label in white
        self.ax.tick_params(colors='white')  # Set tick labels to white
        self.bars = None  # Placeholder for bar plot
        self.annotations = []  # Store annotations for tooltips
        self.cursor = Cursor(self.ax, useblit=True, color='white', linewidth=1)  # Add cursor

    def show(self):
        """Display the plot."""
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def update(self, run_result):
        """Update the plot with a new RunResult."""
        with self.lock:
            new_x = [run_result.description]  # Use description as x value
            new_y = [run_result.avg]
            self.data_x.extend(new_x)
            self.data_y.extend(new_y)
            self._update_plot()
            self._add_tooltip(run_result)
    
    def update_batch(self, run_results):
        """Update the plot with a batch of RunResults."""
        with self.lock:
            for run_result in run_results:
                new_x = [run_result.description]
                new_y = [run_result.avg]
                self.data_x.extend(new_x)
                self.data_y.extend(new_y)
                self._add_tooltip(run_result)
            self._update_plot()

    def clear(self):
        """Clear the plot data."""
        with self.lock:
            self.data_x.clear()
            self.data_y.clear()
            self.ax.clear()

    def _add_tooltip(self, run_result):
        """Add a tooltip for a bar."""
        bar_index = len(self.data_x) - 1
        annotation = self.ax.annotate(
            run_result.long_description, 
            xy=(bar_index, run_result.avg), 
            xytext=(10, 10), 
            textcoords="offset points",
            ha='center', 
            color='black',  # Change text color to black for contrast
            bbox=dict(boxstyle="round,pad=0.3", edgecolor='white', facecolor='yellow', alpha=0.9),  # Yellow background
            visible=False  # Initially hidden
        )
        self.annotations.append(annotation)

    def _update_plot(self):
        """Refresh the plot with the latest data."""
        self.ax.clear()  # Clear the previous bars
        bars = self.ax.bar(self.data_x, self.data_y, color='red')  # Bar plot with red bars
        self.ax.set_title(self.ax.get_title(), color='white')  # Retain title in white
        self.ax.set_xlabel(self.ax.get_xlabel(), color='white')  # Retain x label in white
        self.ax.set_ylabel(self.ax.get_ylabel(), color='white')  # Retain y label in white
        self.ax.tick_params(colors='white')  # Ensure tick labels remain white
        if self.data_y:  # Check if there is data to scale
            y_min = min(self.data_y) - 1  # Add some padding
            y_max = max(self.data_y) + 1
            self.ax.set_ylim(y_min, y_max)  # Manually set y-axis limits
        self.ax.set_xticks(self.data_x)  # Ensure all x labels are visible
        self.ax.relim()  # Recalculate limits
        self.ax.autoscale_view()  # Adjust scale to fit data

        # Add event handling for hover
        def on_hover(event):
            for bar, annotation in zip(bars, self.annotations):
                if bar.contains(event)[0]:  # Check if the mouse is over a bar
                    annotation.set_visible(True)
                    annotation.xy = (bar.get_x() + bar.get_width() / 2, bar.get_height())
                else:
                    annotation.set_visible(False)
            self.fig.canvas.draw_idle()

        self.fig.canvas.mpl_connect("motion_notify_event", on_hover)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
