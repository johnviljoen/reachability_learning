import numpy as np

# pendulum dynamics
def f(x, damping=1):
    """x = {theta, theta_dot}"""
    return np.hstack([x[1], - damping * x[1] - np.sin(x[0])])

if __name__ == "__main__":
    x = np.array([0,1.])
    Ts = 0.1
    for i in range(100):
        x += f(x) * Ts
        print(x)
