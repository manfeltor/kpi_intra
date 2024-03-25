import matplotlib.pyplot as plt
import pandas as pd

def simple_bar_plot(df,x_column, y_column):

    x_values = df[x_column]
    y_values = df[y_column]

    plt.bar(x_values, y_values)
    plt.xlabel('zona')
    plt.ylabel('dias laborales')
    plt.title('titulo')

    return plt.gcf()