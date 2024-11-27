import json
import matplotlib.pyplot as plt
import os
from scipy.stats import linregress
import re

# Load gaze data from the JSON file
json_file_path = "gaze_data.json"

# Check if the JSON file exists
if not os.path.exists(json_file_path):
    raise FileNotFoundError(f"JSON file not found: {json_file_path}")

# Load the gaze data
with open(json_file_path, "r") as file:
    gaze_data = json.load(file)

# Initialize data for target width vs. movement time plot
target_widths = []
movement_times = []

# Create a figure for each target
for target_id, target_info in gaze_data.items():
    target_details = target_info["targetDetails"]
    gaze_points = target_info["gazePoints"]

    # Extract gaze coordinates and timestamps
    gaze_x = [point["gazeX"] for point in gaze_points]
    gaze_y = [point["gazeY"] for point in gaze_points]
    timestamps = [point["time"] for point in gaze_points]

    # Calculate movement time as the difference between the first and last timestamp
    if timestamps:
        movement_time = timestamps[-1] - timestamps[0]  # ms
        movement_times.append(movement_time)
        target_widths.append(target_details["size"])  # Use the target size as its width

    # Plot the gaze path with arrows
    plt.figure(figsize=(8, 6))
    for i in range(len(gaze_x) - 1):
        plt.arrow(gaze_x[i], gaze_y[i], gaze_x[i + 1] - gaze_x[i], gaze_y[i + 1] - gaze_y[i],
                  head_width=25, head_length=25, fc='red', ec='red', label="Gaze Path" if i == 0 else "")
    plt.scatter([target_details["x"]], [target_details["y"]], color="blue", s=100, label="Target Center")
    
    # Add the target boundary (circle)
    target_radius = target_details["size"] / 2
    circle = plt.Circle(
        (target_details["x"], target_details["y"]),
        target_radius,
        color="blue",
        alpha=0.3,
        label="Target Boundary"
    )
    plt.gca().add_patch(circle)

    # Annotate plot
    id = re.sub(r"\D", "", target_id)  # Extract the numerical part of the target ID
    id = int(id) + 1
    plt.title(f"Saccade Path for Target {id}")
    plt.xlabel("Gaze X (pixels)")
    plt.ylabel("Gaze Y (pixels)")
    plt.legend()
    plt.gca().invert_yaxis()  # Invert Y-axis to match typical screen coordinates
    plt.axis("equal")
    plt.grid()

    # Save the figure
    plt.savefig(f"figs/{target_id}_saccade_path.png")
    plt.show()

# Plot target width vs. movement time
# drop the last element
target_widths.pop()
movement_times.pop()
plt.figure(figsize=(8, 6))
plt.scatter(target_widths, movement_times, color="green", label="Experimental Data")

# Perform linear regression
slope, intercept, r_value, p_value, std_err = linregress(target_widths, movement_times)
regression_line = [slope * width + intercept for width in target_widths]
plt.plot(target_widths, regression_line, color="red", linestyle="--", label=f"Fit Line (R²={r_value**2:.2f})")

# Annotate the plot
plt.title("Target Width vs. Movement Time")
plt.xlabel("Target Width (pixels)")
plt.ylabel("Movement Time (ms)")
plt.grid()
plt.legend()

# Save and show the figure
plt.savefig("figs/target_width_vs_movement_time.png")
plt.show()

