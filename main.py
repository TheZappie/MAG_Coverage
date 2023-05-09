import itertools

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.collections import LineCollection, CircleCollection, PatchCollection


def mirrored_interval(step: float, n: int):
    array = np.arange(0, n * step, step)
    return array - (array[-1] / 2)

def main():
    st.title("Detection range calculator")
    alt, burial_depth, detection_range, n_sensors, spacing = get_input()

    x_ = detection_range ** 2 - (alt + burial_depth) ** 2

    # Geowing Config
    # n_sensors = 3
    # spacing = 2.5
    sensor_x = mirrored_interval(spacing, n_sensors)
    centers = [np.array([x, alt]) for x in sensor_x]
    # cl = CircleCollection(itertools.repeat(detection_range, n_sensors), offsets=centers)
    circles = [plt.Circle(center, detection_range, color='grey', fill=False, linestyle='--') for center in centers]

    # circle_M1_x = plt.Circle(center_1, detection_range, color='grey', fill=False)
    # circle_M3_x = plt.Circle(center_2, detection_range, color='grey', fill=False)
    # circle_M5_x = plt.Circle(center_3, detection_range, color='grey', fill=False)
    # ax.annotate(txt, (z[i], y[i]))

    fig, ax = plt.subplots()
    ax.axis([-12, 12, -8, 12])
    # ax.add_patch(circle_M1_x)
    # ax.add_patch(circle_M3_x)
    # ax.add_patch(circle_M5_x)
    for c in circles:
        ax.add_patch(c)
    # cl = PatchCollection(circles)
    # ax.add_collection(cl)
    # for i, (x, y) in enumerate(centers):
    #     ax.annotate(f'{i}', (x, y))

    ax.axhline(y=0, color='b', linestyle='-', label='Seafloor')
    ax.axhline(y=-burial_depth, color='r', linestyle='--', label='Burial depth')

    # ax.plot([center_1, (M1 + x_range, -burial_depth)])
    if x_ >= 0:
        x_range = np.sqrt(x_)
        left = (centers[0][0] - x_range, -burial_depth)
        right = (centers[-1][0] + x_range, -burial_depth)
        lc = LineCollection([[centers[0], left],
                             [centers[-1], right],
                             ],
                            linewidth=1.0,
                            linestyle='--'
                            )
        ax.add_collection(lc)
        lc = LineCollection([[left, right]], linewidth=3.0,)
        ax.add_collection(lc)
        ax.annotate(f'Swath: {2 * x_range:.2g} m', (0, -burial_depth+0.5), ha='center')
    ax.scatter(*np.array(centers).T)

    ax.set_xlabel("Cross-track [m]")
    ax.set_ylabel("Altitude [m]")
    # ax.set_title("Detection Range")
    ax.set_aspect('equal')
    st.pyplot(fig)


def get_input():
    DR = st.slider("Detection Range [m]", 0.0, 20.0, 7.0, step=0.1)
    BD = st.slider("Burial Depth [m]", 0.0, 10.0, 3.0, step=0.1)
    ALT = st.slider("Altitude [m]", 0.0, 30.0, 3.0, step=0.1)
    n_sensors = st.sidebar.slider('Number of sensors', 1, 5, 3, step=1)
    if n_sensors > 1:
        spacing = st.sidebar.slider('Sensor spacing', 1.0, 5.0, 2.5, step=0.1)
    else:
        spacing = 1
    return ALT, BD, DR, n_sensors, spacing


if __name__ == '__main__':
    main()