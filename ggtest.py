import pandas as pd
from plotnine import *

# Read data from CSV file
data = pd.read_csv('KyotoFullFlower.csv')

# Convert DOY to date
data['Full-flowering date'] = pd.to_datetime('2024-01-01') + pd.to_timedelta(data['Full-flowering date (DOY)'] - 1, unit='D')

# Drop rows with missing or invalid dates
data = data.dropna(subset=['Full-flowering date'])

# Find the average full-flowering date
average_date = data['Full-flowering date'].mean()

# Define the custom marker for sakura image
sakura_marker = geom_point(data=data, mapping=aes(x='AD', y='Full-flowering date'), color='pink', shape='*')

# Create plot using plotnine
p = ggplot(data) + \
    geom_point(aes(x='AD', y='Full-flowering date'), color='#F57D1F', size=2) + \
    geom_line(aes(x='AD', y='Full-flowering date'), color='#F57D1F') + \
    sakura_marker + \
    geom_smooth(aes(x='AD', y='Full-flowering date'), method='lm', se=False, color='black') + \
    labs(x='AD', y='MD') + \
    scale_y_datetime(date_labels='%B-%d') +\
    theme_bw()

# Display the plot
print(p)


class testimport:
    def __init__(self) -> None:
        pass