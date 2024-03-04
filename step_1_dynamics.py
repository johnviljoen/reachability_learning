import numpy as np
from animator import Animator

# pendulum dynamics
def f(x, damping=1):
    """x = {theta, theta_dot}"""
    return np.hstack([x[1], - damping * x[1] - np.sin(x[0])])

# 
if __name__ == "__main__":
    x = np.array([10,1.])
    Ti, Tf, Ts = 0.0, 10.0, 0.1
    times = np.arange(Ti,Tf,Ts)
    data = {'states': []}

    for t in times:
        x += f(x) * Ts
        data['states'].append(np.copy(x))
    data['states'] = np.vstack(data['states'])

    animator = Animator(
            states = data['states'],
            predictions = None,
            times = times,
            max_frames = 500,
            save = True,
            save_path = 'data/media'            
        )
    
    animator.animate()
