import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.collections import LineCollection


def main():
    st.title("Detection Range")
    alt, burial_depth, detection_range = get_input()

    x_ = detection_range ** 2 - (alt + burial_depth) ** 2

    x_range = np.sqrt(x_)

    # Geowing Config
    M1 = -2.5
    M3 = 0
    M5 = 2.5

    center_1 = (M1, alt)
    center_2 = (M3, alt)
    center_3 = (M5, alt)
    circle_M1_x = plt.Circle(center_1, detection_range, color='grey', fill=False)
    circle_M3_x = plt.Circle(center_2, detection_range, color='grey', fill=False)
    circle_M5_x = plt.Circle(center_3, detection_range, color='grey', fill=False)


    fig, ax = plt.subplots()
    ax.axis([-10, 10, -8, 7])
    ax.add_patch(circle_M1_x)
    ax.add_patch(circle_M3_x)
    ax.add_patch(circle_M5_x)
    ax.axhline(y=0, color='b', linestyle='-')
    ax.axhline(y=-burial_depth, color='r', linestyle='-', )

    # ax.plot([center_1, (M1 + x_range, -burial_depth)])
    if x_ > 0:
        left = (M1 - x_range, -burial_depth)
        right = (M5 + x_range, -burial_depth)
        lc = LineCollection([[center_1, left],
                             [center_3, right],
                             [left, right],
                             ],
                            linewidth=3.0,
                            )
        ax.add_collection(lc)
    ax.scatter(*np.array([center_1, center_2, center_3]).T)

    ax.set_xlabel("Cross-track [m]")
    ax.set_ylabel("Altitude [m]")
    ax.set_title("Detection Range")
    ax.set_aspect('equal')
    st.pyplot(fig)



def get_input():
    DR = st.slider("Detection Range [m]", 0.0, 20.0, 7.0, step=0.1)
    BD = st.slider("Burial Depth [m]", 0.0, 10.0, 3.0, step=0.1)
    ALT = st.slider("Altitude [m]", 0.0, 30.0, 4.5, step=0.1)
    return ALT, BD, DR


if __name__ == '__main__':
    main()