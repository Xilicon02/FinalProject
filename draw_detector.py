import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from config.detector_config import detectors
import models.detector as de
from config.plot_config import *


#print(f"Number of detectors: {len(detectors)}")

# Cost
#de.Get_Price(detectors)

# Draw detectors
fig = plt.figure(1, figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
configure_plot(ax)

for d in detectors:
    z = d.position[2]
    color = get_color_by_z(z)
    d.plot(ax, color=color)

plt.title(f"Total Detectors: {len(detectors)}, Cost: {de.Get_Price(detectors)}")


plt.savefig("detector_plot.png")