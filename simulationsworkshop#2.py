import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dataclasses import dataclass
import numpy as np

DELTA_T = 0.01 
CAR_MASS = 1000.0
CD_A = 1.1 
AIR_DENSITY = 1.225
ACCEL_RATE = 2.0 
BRAKE_RATE = 4.0 
SIM_DURATION = 30.0 
MAX_FRAMES = int(SIM_DURATION / DELTA_T)
ANIMATION_INTERVAL = 10 
current_time = 0.0 

@dataclass
class State:
    xpos : float
    xvel : float

car_state = State(xpos = 0.0, xvel = 0.0)

def step (state:State) -> State:
    global current_time
    v = state.xvel
    drag_force = 0.5 * CD_A * AIR_DENSITY * v**2
    drag_accel = -drag_force / CAR_MASS
    
    if current_time <= 10.0:
        ideal_accel = ACCEL_RATE
        
    elif v > 0.0:
        ideal_accel = -BRAKE_RATE
        
    else:
        ideal_accel = 0.0
        
    net_accel = ideal_accel + drag_accel
    
    new_xvel = state.xvel + net_accel * DELTA_T
    
    if state.xvel <= 0.0 and net_accel < 0:
        new_xvel = 0.0
    elif state.xvel > 0.0 and new_xvel < 0.0 and current_time > 10.0:
        new_xvel = 0.0
        
    new_xpos = state.xpos + new_xvel * DELTA_T
        
    sNew = State(
        xpos = new_xpos,
        xvel = new_xvel
    )
    return sNew

def animate (i):
    global car_state, current_time, ani
    
    if current_time >= SIM_DURATION:
        try:
            ani.event_source.stop() 
        except NameError:
            pass
        return ax,   
    car_state = step(car_state)
    current_time += DELTA_T
    ax.clear()
    ax.scatter([car_state.xpos], [1.0], s=200, marker='s', color='darkgreen')
    ax.set_yticks([])
    ax.set_xlim(car_state.xpos - 20, car_state.xpos + 20)
    
    ax.grid(True, axis='x', linestyle='--')
    ax.set_ylim(0.5, 1.5)
    
    
    
    return ax,

fig = plt.figure(figsize=(10,4), dpi=100)
ax = fig.add_subplot(111)
ax.grid()
ax.set_xlim(-5, 5)
ax.set_ylim(0, 2)
plt.pause(5)
ani = animation.FuncAnimation(fig, animate, frames=MAX_FRAMES, interval=ANIMATION_INTERVAL, repeat=False)
plt.show()
