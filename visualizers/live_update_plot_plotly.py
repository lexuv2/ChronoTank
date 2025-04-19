import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import threading
from queue import Queue
import webbrowser  # Import webbrowser to open the browser automatically
import time

class LiveUpdatePlot:
    def __init__(self, title="Live Update Plot", x_label="X", y_label="Y"):
        """Initialize the live update plot."""
        self.data_x = []
        self.data_y = []
        self.tooltips = []
        self.lock = threading.Lock()  # Thread-safe updates
        self.update_queue = Queue()  # Queue for thread-safe updates
        self.server_thread = None  # Thread to run the Dash server
        self.title = title
        self.x_label = x_label
        self.y_label = y_label

        # Initialize Dash app
        self.app = dash.Dash(__name__)
        self.app.layout = html.Div(
            style={'backgroundColor': 'black', 'color': 'white', 'height': '100vh'},  # Set black background and white text
            children=[
                dcc.Graph(id='live-plot'),
                dcc.Interval(id='interval-update', interval=200, n_intervals=0)  # Update every 200ms
            ]
        )

        # Set up callbacks
        @self.app.callback(
            Output('live-plot', 'figure'),
            [Input('interval-update', 'n_intervals')]
        )
        def update_graph(n_intervals):
            return self.update_graph(n_intervals)

    def show(self):
        """Run the Dash app in a separate thread and open the browser."""
        def run_server():
            import logging
            logging.getLogger('werkzeug').setLevel(logging.ERROR)  # Suppress Werkzeug debug info
            webbrowser.open("http://127.0.0.1:8050")  # Open the browser automatically
            self.app.run(debug=False, host="127.0.0.1", port=8050)  # Disable Dash debug info

        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        time.sleep(1)  # Give the server a moment to start

    def update(self, run_result):
        """Queue a single update for the plot."""
        self.update_queue.put(("single", {
            "x": run_result.description,
            "y": run_result.avg,
            "tooltip": run_result.long_description
        }))

    def update_batch(self, run_results):
        """Queue a batch update for the plot."""
        descriptions = [r.description for r in run_results]
        avgs = [r.avg for r in run_results]
        tooltips = [r.long_description for r in run_results]
        self.update_queue.put(("batch", {
            "x": descriptions,
            "y": avgs,
            "tooltips": tooltips
        }))

    def clear(self):
        """Clear the plot data."""
        with self.lock:
            self.data_x.clear()
            self.data_y.clear()
            self.tooltips.clear()

    def _adjust_y_scale(self):
        """Adjust the y-axis scale based on the data."""
        if self.data_y:
            y_min = min(self.data_y) - 1  # Add some padding
            y_max = max(self.data_y) + 1
        else:
            y_min, y_max = 0, 1  # Default scale if no data
        return y_min, y_max

    def update_graph(self, n_intervals):
        """Update the graph layout and data."""
        with self.lock:
            # Process updates from the queue
            while not self.update_queue.empty():
                update_type, data = self.update_queue.get()
                if update_type == "single":
                    self.data_x.append(data['x'])
                    self.data_y.append(data['y'])
                    self.tooltips.append(data['tooltip'])
                elif update_type == "batch":
                    self.data_x.extend(data['x'])
                    self.data_y.extend(data['y'])
                    self.tooltips.extend(data['tooltips'])

            # Adjust y-axis scale
            y_min, y_max = self._adjust_y_scale()

            # Create the figure
            return go.Figure(
                data=[
                    go.Bar(
                        x=self.data_x,
                        y=self.data_y,
                        text=self.tooltips,
                        hoverinfo='text',  # Show tooltips on hover
                        marker=dict(color='red')
                    )
                ],
                layout=go.Layout(
                    title=self.title,
                    xaxis=dict(title=self.x_label),
                    yaxis=dict(title=self.y_label, range=[y_min, y_max]),  # Set y-axis range
                    template='plotly_dark'  # Use plotly_dark theme
                )
            )
