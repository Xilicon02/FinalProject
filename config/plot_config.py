import matplotlib.pyplot as plt
from config.detector_config import detectors


plt.style.use("seaborn-whitegrid")
plt.rcParams.update({
    "font.size": 12,
    "axes.labelsize": 14,
    "axes.titlesize": 16,
    "legend.fontsize": 12,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "lines.linewidth": 2,
    "lines.markersize": 6,
    "grid.alpha": 0.3,
    "figure.dpi": 150,
})


# ===== 3D Plot Configuration =====
def configure_plot(ax):
    ax.set_xlim(-200, 200)
    ax.set_ylim(-200, 200)
    ax.set_zlim(0, 200)
    ax.set_xlabel('X (cm)')
    ax.set_ylabel('Y (cm)')
    ax.set_zlabel('Z (cm)')


# ===== Color Configuration =====
def get_rainbow_colors(n):
    cmap = plt.cm.rainbow
    return [cmap(i / n) for i in range(n)]

colors = get_rainbow_colors(7)  # 可以根据 z 层数动态设置
z_to_color = {}

def get_color_by_z(z):
    if z not in z_to_color:
        z_to_color[z] = colors[len(z_to_color) % len(colors)]
    return z_to_color[z]
