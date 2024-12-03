import json
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# Load the interaction data
with open("interaction_data.json", "r") as file:
    data = json.load(file)

# Extract relevant data
target_positions = [(entry["targetDetails"]["x"], entry["targetDetails"]["y"]) for entry in data]
touch_positions = [(entry["touchX"], entry["touchY"]) for entry in data]
sizes = [entry["targetDetails"]["size"] for entry in data]
timestamps = [entry["timestamp"] for entry in data]

# Calculate speed (time between touches)
time_differences = [
    (timestamps[i + 1] - timestamps[i]) / 1000.0 for i in range(len(timestamps) - 1)
]
time_differences.insert(0, 0)  # First touch has no prior time

# Visualization 1: Target and touch positions
plt.figure(figsize=(8, 6))
for (x, y), size in zip(target_positions, sizes):
    circle = Circle((x, y), size / 2, color="blue", alpha=0.3)
    plt.gca().add_patch(circle)
plt.scatter(*zip(*touch_positions), color="red", label="Touches", zorder=2)
plt.scatter(*zip(*target_positions), color="blue", label="Targets", zorder=3)
plt.title("Target and Touch Positions")
plt.xlabel("X Position (px)")
plt.ylabel("Y Position (px)")
plt.legend()
plt.axis("equal")
plt.grid()
plt.show()

# Visualization 2: Trajectories
plt.figure(figsize=(8, 6))
plt.plot(
    [pos[0] for pos in touch_positions],
    [pos[1] for pos in touch_positions],
    marker="o",
    color="green",
    label="Trajectory",
)
plt.title("Trajectory of Touches")
plt.xlabel("X Position (px)")
plt.ylabel("Y Position (px)")
plt.legend()
plt.grid()
plt.show()

# Visualization 3: Speed (time between touches)
plt.figure(figsize=(8, 6))
plt.plot(range(len(time_differences)), time_differences, marker="o", color="purple")
plt.title("Time Between Touches")
plt.xlabel("Touch Index")
plt.ylabel("Time (seconds)")
plt.grid()
plt.show()

# Visualization 4: Accuracy (distance from target)
def distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

distances = [
    distance(touch, target)
    for touch, target in zip(touch_positions, target_positions)
]

plt.figure(figsize=(8, 6))
plt.bar(range(len(distances)), distances, color="orange")
plt.title("Accuracy: Distance from Target")
plt.xlabel("Touch Index")
plt.ylabel("Distance (px)")
plt.grid()
plt.show()
