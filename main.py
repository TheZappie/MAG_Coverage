import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def main():
    st.title("Detection Range")

    DR = st.slider("DR", 0.0, 20.0, 7.0, step=0.1)
    BD = st.slider("BD", 0.0, 10.0, 3.0, step=0.1)
    MAX_ALT = 30.0
    ALT = st.slider("ALT", 0.0, MAX_ALT, 4.5, step=0.1)

    DC = np.sqrt(abs(DR ** 2 - (ALT + BD) ** 2))

    deg = np.arange(0, 360.01, 0.01)
    rad = np.deg2rad(deg)

    # Geowing Config
    M1 = -2.5
    M3 = 0
    M5 = 2.5

    M1_x = DR * np.sin(rad) + M1
    M3_x = DR * np.sin(rad) + M3
    M5_x = DR * np.sin(rad) + M5
    My = DR * np.cos(rad) + ALT

    DC3 = [-DC]

    # seabed
    Sea_y = np.zeros(201)
    # burial depth
    BD_y = -BD + np.zeros(201)
    Aux_y = np.vstack((BD_y, Sea_y))
    Aux_x = np.arange(-10, 10.1, 0.1)

    Mx = np.vstack((M1_x, M3_x, M5_x)).T

    # plot
    fig, ax = plt.subplots()
    ax.axis([-10, 10, -5, 15])
    ax.plot(Mx, My)
    ax.plot(M1, ALT)
    # , "1", M3, ALT, "2", M5, ALT, "3", Aux_x, Sea_y, "k", Aux_x, BD_y, "m")
    ax.set_xlabel("Easting [m]")
    ax.set_ylabel("m")
    ax.set_title("Detection Range")
    ax.set_aspect('equal')
    st.pyplot(fig)

if __name__ == '__main__':
    main()