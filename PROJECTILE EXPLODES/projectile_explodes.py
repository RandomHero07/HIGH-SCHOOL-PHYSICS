
import numpy as np
import matplotlib.pyplot as plt
import imageio
import os

# Constants and initial parameters
X = 10
Y = 5
Z = 5
U = 40
theta = 45 * np.pi / 180
g = 9.81
t_explode = 2
dt = 0.05

# Initial velocity components
vx = U * np.cos(theta)
vy = U * np.sin(theta)

# Compute position at explosion
x_exp = vx * t_explode
y_exp = vy * t_explode - 0.5 * g * t_explode**2
vy_at_explosion = vy - g * t_explode

# Use momentum conservation to get velocities of fragments
v1x = vx + 10
v2x = (X * vx - Y * v1x) / Z
v1y = vy_at_explosion + 5
v2y = (X * vy_at_explosion - Y * v1y) / Z

# Compute time till both fragments hit ground
def time_to_ground(y0, vy):
    return (vy + np.sqrt(vy**2 + 2*g*y0)) / g

frag1_flight = time_to_ground(y_exp, v1y)
frag2_flight = time_to_ground(y_exp, v2y)

# Buffer to ensure all peaks and landings are shown
buffer_time = 1.5
t_end = t_explode + max(frag1_flight, frag2_flight) + buffer_time

# Estimate max range and height for auto-scaling
frag1_range = x_exp + v1x * frag1_flight
frag2_range = x_exp + v2x * frag2_flight
frag1_peak = y_exp + v1y**2 / (2 * g)
frag2_peak = y_exp + v2y**2 / (2 * g)

x_limit = max(frag1_range, frag2_range) * 1.1
y_limit = max(frag1_peak, frag2_peak) * 1.2

# Precompute landing and peak points
x1_land = x_exp + v1x * frag1_flight
x2_land = x_exp + v2x * frag2_flight
x1_peak = x_exp + v1x * (v1y / g)
y1_peak = y_exp + v1y**2 / (2 * g)
x2_peak = x_exp + v2x * (v2y / g)
y2_peak = y_exp + v2y**2 / (2 * g)
t1_peak = v1y / g
t2_peak = v2y / g

# Folder for frames
os.makedirs("frames", exist_ok=True)
frames = []

t_vals = np.arange(0, t_end + dt, dt)
for i, t in enumerate(t_vals):
    plt.figure(figsize=(7, 5))
    plt.xlim(0, x_limit)
    plt.ylim(0, y_limit)
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.title("Projectile Explosion Simulation")

    if t < t_explode:
        x = vx * t
        y = vy * t - 0.5 * g * t**2
        plt.plot(x, y, 'ro')
    else:
        t_frag = t - t_explode
        x1 = x_exp + v1x * t_frag
        y1 = y_exp + v1y * t_frag - 0.5 * g * t_frag**2
        x2 = x_exp + v2x * t_frag
        y2 = y_exp + v2y * t_frag - 0.5 * g * t_frag**2

        if y1 > 0:
            plt.plot(x1, y1, 'bo', label='Frag 1')
            if abs(t_frag - t1_peak) < dt:
                plt.plot(x1_peak, y1_peak, 'b^', label='Frag 1 Peak')
        else:
            plt.plot(x1_land, 0, 'b*', label='Frag 1 Landed')
            plt.plot(x1_peak, y1_peak, 'b^', label='Frag 1 Peak')

        if y2 > 0:
            plt.plot(x2, y2, 'go', label='Frag 2')
            if abs(t_frag - t2_peak) < dt:
                plt.plot(x2_peak, y2_peak, 'g^', label='Frag 2 Peak')
        else:
            plt.plot(x2_land, 0, 'g*', label='Frag 2 Landed')
            plt.plot(x2_peak, y2_peak, 'g^', label='Frag 2 Peak')

        plt.plot(x_exp, y_exp, 'kx', label='Explosion Point')

    plt.legend(loc='lower right')
    fname = f"frames/frame_{i:03d}.png"
    plt.savefig(fname)
    frames.append(fname)
    plt.close()

# Make video
with imageio.get_writer("projectile_explosion.mp4", fps=20) as writer:
    for fname in frames:
        writer.append_data(imageio.imread(fname))

print("Video saved as projectile_explosion.mp4")