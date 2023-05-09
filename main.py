import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from matplotlib.collections import LineCollection, CircleCollection, PatchCollection
from matplotlib.lines import Line2D
from matplotlib.patches import Circle

def mirrored_interval(step: float, n: int):
    array = np.arange(0, n * step, step)
    return array - (array[-1] / 2)

def main():
    st.title("MAG Coverage")
    alt, burial_depth, detection_range, n_sensors, spacing = get_input()

    x_ = detection_range ** 2 - (alt + burial_depth) ** 2

    # Geowing Config
    # n_sensors = 3
    # spacing = 2.5
    sensor_x = mirrored_interval(spacing, n_sensors)
    centers = [np.array([x, alt]) for x in sensor_x]
    # cl = CircleCollection(itertools.repeat(detection_range, n_sensors), offsets=centers)
    circles = [Circle(center, detection_range, color='grey', fill=False, linestyle='--') for center in centers]


    fig, ax = plt.subplots()
    bounds = [-12, 12, -8, 12]
    ax.axis(bounds)
    ax.annotate('Burial Depth', (bounds[0]+0.1, -burial_depth-0.1), color='red', size=8, va='top')
    ax.annotate('Seafloor', (bounds[0]+0.1, +0.1), color='blue', size=8, va='bottom')
    circle_patch_collection = PatchCollection(circles, match_original=True, label='fre')
    ax.add_collection(circle_patch_collection)
    ax.axhline(y=0, color='b', linestyle='-')
    ax.axhline(y=-burial_depth, color='r', linestyle='--')

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
        swath = 2 * x_range - sensor_x[0] + sensor_x[-1]
        # (2×{x_range:.1f} + {sensor_x[-1]- sensor_x[0]:.1f})
        ax.annotate(f'Swath: {swath :.1f} m \n'
                    f'DC: {x_range:.1f} m', (0, -7), ha='center')
    sensor_artist = ax.scatter(*np.array(centers).T, label='Sensors')

    ax.set_xlabel("Cross-track [m]")
    ax.set_ylabel("Altitude [m]")
    ax.set_aspect('equal')

    import matplotlib.artist as martist
    circle_proxy = Line2D([0], [0], linestyle='--', alpha=0.7, color='grey', label='Detection range')
    ax.legend(handles=[circle_proxy, sensor_artist])
    st.pyplot(fig)


def get_input():
    DR = st.slider("Detection Range [m] (@ 2 nT)", 0.0, 20.0, 7.0, step=0.1)
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