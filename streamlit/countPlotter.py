import matplotlib.pyplot as plt
from matplotlib.figure import Figure

def countFig():
    fig = Figure()
    ax = fig.add_subplot(111)
    ax.set_title("Photon Counting")
    ax.set_xlabel("Sample")
    ax.set_ylabel("Counts (N)")
    # ax.set_xlim(0, 200)
    # ax.set_ylim(-0.5, 6)
    ax.grid(visible=True, which='major', color='#666666', linestyle='-')
    ax.minorticks_on()
    ax.grid(visible=True, which='minor', color='#666666', linestyle='-', alpha=0.2)
    return fig, ax
