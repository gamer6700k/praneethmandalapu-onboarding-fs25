import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dataclasses import dataclass
import numpy as np 

DELTA_T = 0.01
G = 9.81
BOUNCE_COEFF = 0.9
INITIAL_HEIGHT = 10.0
SIM_DURATION = 10.0
MAX_FRAMES = int(SIM_DURATION / DELTA_T)
ANIMATION_INTERVAL = 10
current_time = 0.0


@dataclass
class State:
    xpos: float
    ypos: float
    xvel: float
    yvel: float


s1 = State(xpos=0.0, ypos=INITIAL_HEIGHT, xvel=0.1, yvel=0.0)
s2 = State(xpos=0.0, ypos=INITIAL_HEIGHT, xvel=0.2, yvel=0.0)


def step(state: State) -> State:
    new_yvel = state.yvel - G * DELTA_T

    new_xpos = state.xpos + state.xvel * DELTA_T
    new_ypos = state.ypos + new_yvel * DELTA_T

    if new_ypos < 0.0:
        new_ypos = 0.0
        new_yvel = new_yvel * -1 * BOUNCE_COEFF

    sNew = State(
        xpos=new_xpos,
        ypos=new_ypos,
        xvel=state.xvel,
        yvel=new_yvel
    )
    return sNew


def animate(i):
    global s1, s2, current_time

    s1 = step(s1)
    s2 = step(s2)
    current_time += DELTA_T

    ax.clear()

    ax.scatter([s1.xpos], [s1.ypos], s=70, color='blue', label='Ball 1 (vx=0.1)')
    ax.scatter([s2.xpos], [s2.ypos], s=70, color='red', label='Ball 2 (vx=0.2)')

    ax.set_xlim(0, 2.5)
    ax.set_ylim(0, INITIAL_HEIGHT * 1.1)
    ax.grid(True)
    ax.axhline(0, color='black', linewidth=2)
    ax.set_title(f'Time: {current_time:.2f} s')
    ax.set_xlabel('Horizontal Position (m)')
    ax.set_ylabel('Vertical Position (m)')
    ax.legend(loc='upper left')

    return ax,


fig = plt.figure(figsize=(6, 6), dpi=150)
ax = fig.add_subplot(111)
ax.grid()
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)

plt.pause(5)

ani = animation.FuncAnimation(fig, animate, frames=MAX_FRAMES, interval=ANIMATION_INTERVAL, repeat=False)
plt.show()
