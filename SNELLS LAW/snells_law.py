############# GO TO END OF FILE FOR SIMULATING DIRECTLY FOR WANTED N1 AND N2 :-)
import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import os
############## USING SNELL'S LAW TO CALCULATE APPROPRIATE ANGLES
def snell_law(n1, n2, theta1_deg):
    theta1 = np.radians(theta1_deg)
    sin_theta2 = n1 / n2 * np.sin(theta1)
    if abs(sin_theta2) > 1:
        return None  # Total internal reflection
    theta2 = np.arcsin(sin_theta2)
    return np.degrees(theta2)
############## FUNCTION TO DRAW THE RAY (ax.arrow is used with 0 body to show which way the light ray is pointing)
def draw_ray(ax, origin, angle_deg, length, color, label=None):
    angle_rad = np.radians(angle_deg)
    x = [origin[0], origin[0] + length * np.sin(angle_rad)]
    y = [origin[1], origin[1] + length * np.cos(angle_rad)]
    ax.plot(x, y, color=color, label=label, linewidth=2)
    ax.arrow(x[1], y[1], 0, 0, head_width=0.15, head_length=0.25, fc=color, ec=color)
############### FUNCTION TO SIMULATE (show) WHOLE SETUP (INCIDENT - REFREACTED/REFLECTED RAYS ,LEGEND etc...)
def simulate_frame(n1, n2, angle_of_incidence_deg, filename):
    ##setting up the canvas
    fig, ax = plt.subplots()
    ax.set_xlim(-5, 5)
    ax.set_ylim(-3, 6)
    ax.set_aspect('equal')
    ax.axhline(0, color='black', linestyle='--')
    ax.text(-4.8, 0.2, 'Interface', fontsize=10)
    ## DRAWING THE INCIDENT RAY
    length = 2.5
    theta_rad = np.radians(angle_of_incidence_deg)
    start_x = -length * np.sin(theta_rad)
    start_y = -length * np.cos(theta_rad)
    draw_ray(ax, origin=(start_x, start_y), angle_deg=angle_of_incidence_deg, length=length, color='blue', label='Incident Ray')
    theta2 = snell_law(n1, n2, angle_of_incidence_deg)
    ## DRAWING THE REFLECTED/REFRACTED RAY
    if theta2 is None:
        reflected_angle = 180 - angle_of_incidence_deg
        draw_ray(ax, origin=(0, 0), angle_deg=reflected_angle, length=2.5, color='red', label='TIR Ray')
        ax.text(-4.5, 5.3, 'Total Internal Reflection!', fontsize=12, color='red')
    else:
        draw_ray(ax, origin=(0, 0), angle_deg=theta2, length=3, color='green', label='Refracted Ray')

    ax.legend()
    ax.set_title(f"n1 = {n1}, n2 = {n2}, Incident Angle = {angle_of_incidence_deg}°")
    plt.grid(True)
    plt.savefig(filename)
    plt.close()
########SAVING FILE/ PLOT IMAGES TO VIDEO FILE
def create_video(n1, n2, output_file='refraction_video.mp4'):
    filenames = []
    for angle in range(1, 91):  # 1° to 90°
        fname = f"frame_{angle:03d}.png"
        simulate_frame(n1, n2, angle, fname)
        filenames.append(fname)

    with imageio.get_writer(output_file, fps=10) as writer:
        for fname in filenames:
            image = imageio.imread(fname)
            writer.append_data(image)
    for fname in filenames:
        os.remove(fname)

    print(f"Video saved to {output_file}")

####################### HERE!!!!!!!!!!!!!!!!!!! Call this to generate the video
create_video(n1=1.732, n2=1.0)