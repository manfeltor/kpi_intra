import plotly.graph_objs as go
import pandas as pd

def interactive_bar_plot():
    # TODO test the func hard coded, then start passing DF
    # Create a sample DataFrame (replace this with your actual DataFrame)
    df = pd.DataFrame({
        'x_column': [1, 2, 3, 4],
        'y_column1': [10, 20, 15, 25],  # First y column
        'y_column2': [15, 25, 20, 30],  # Second y column
        'other_column1': [5, 10, 7, 12],  # Other columns...
        'other_column2': [8, 15, 10, 20],
        # Add more columns if needed
    })

    # Specify the x and y values for the traces
    x_values = df['x_column']
    y_values1 = df['y_column1']
    y_values2 = df['y_column2']

    # Create traces for the y columns
    trace1 = go.Bar(x=x_values, y=y_values1, name='y_column1')
    trace2 = go.Bar(x=x_values, y=y_values2, name='y_column2')

    # Create the Plotly figure
    fig = go.Figure(data=[trace1, trace2])
    fig.update_layout(title='Interactive Bar Chart with Multiple Y Columns', xaxis_title='X Axis Label', yaxis_title='Y Axis Label')

    # Convert the figure to JSON
    graph_json = fig.to_json()

    return graph_json