import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
from ggtest import testimport
# Read data from CSV file
data = pd.read_csv('KyotoFullFlower.csv')

# Convert DOY to date
data['Full-flowering date'] = pd.to_datetime('2024-01-01') + pd.to_timedelta(data['Full-flowering date (DOY)'] - 1, unit='D')

# Drop rows with missing or invalid dates
data = data.dropna(subset=['Full-flowering date'])

# Find the average full-flowering date
average_date = data['Full-flowering date'].mean()

# Create Time Series Plot
plt.figure(figsize=(8, 6))

# Plot the graph
plt.plot(data['AD'], data['Full-flowering date'], color='#F57D1F')

# Plot the horizontal line
plt.axhline(y=average_date, color='black', linestyle='-.', label='Average Full-flowering date')

# Resize and load the image as background
img = Image.open('fuji.jpg')
img_resized = img.resize((int(img.width * 0.5), int(img.height * 0.5)))  # Resize the image to 50% of its original size
plt.imshow(img_resized, extent=[750, 2050, '2024-03-23', '2024-05-10'], aspect='auto')


sakura_img = plt.imread('sakura.png')
imagebox = OffsetImage(sakura_img, zoom=0.02)
for x, y in zip(data['AD'], data['Full-flowering date']):
    ab = AnnotationBbox(imagebox, (x, y), frameon=False)
    plt.gca().add_artist(ab)

# Customize y-axis labels
date_form = DateFormatter("%B-%d")  # Monthname-Day format
plt.gca().yaxis.set_major_formatter(date_form)

plt.xlabel('AD')
plt.ylabel('MD')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()