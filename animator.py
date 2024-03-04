import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import os
from datetime import datetime

class Animator:
    def __init__(
            self,
            states,
            predictions,
            times,
            max_frames = 500,
            dt = 0.1,
            save = True,
            save_path = 'data/media'      
        ) -> None:

        self.dt = dt
        num_steps = len(times)

        def compute_render_interval(num_steps, max_frames):
            render_interval = 1  # Start with rendering every frame.
            # While the number of frames using the current render interval exceeds max_frames, double the render interval.
            while num_steps / render_interval > max_frames:
                render_interval *= 2
            return render_interval
        render_interval = compute_render_interval(num_steps, max_frames)

        if predictions is not None:
            self.preds = None
            self.predictions = predictions[::render_interval,:]
        else:
            self.predictions = predictions
        
        states = states[::render_interval,:]
        self.times = times[::render_interval]

        self.save = save
        self.save_path = save_path

        # Unpack States for readability
        # -----------------------------

        self.theta = states[:,0]
        self.theta_dot = states[:,1]

        # Instantiate the figure with title, time, limits...
        # --------------------------------------------------

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot()

        # size the plot properly
        extraEachSide = 0.5
        x_min = np.min(self.theta)
        y_min = np.min(self.theta_dot)
        x_max = np.max(self.theta)
        y_max = np.max(self.theta_dot)
        maxRange = 0.5*np.array([x_max-x_min, y_max-y_min]).max() + extraEachSide
        mid_x = 0.5*(x_max+x_min)
        mid_y = 0.5*(y_max+y_min)
        self.ax.set_xlim([mid_x-maxRange, mid_x+maxRange])
        self.ax.set_ylim([mid_y-maxRange, mid_y+maxRange])
        self.ax.set_xlabel('theta')
        self.ax.set_ylabel('theta_dot')

        # placeholder for timestamp plotting
        self.titleTime = self.ax.text(0.05, 0.95, "", transform=self.ax.transAxes)

        # create the line that represents the pendulum trajectory
        self.line1, = self.ax.plot([], [], lw=2, color='black')

        self.current_pos = None

    def draw_predictions(self, prediction):
        return self.ax.plot(prediction[0], prediction[1], color='black')
    

    def update_lines(self, i):
        theta = self.theta[i]
        theta_dot = self.theta_dot[i]

        theta_from0 = self.theta[0:i]
        theta_dot_from0 = self.theta_dot[0:i]

        self.line1.set_data(theta_from0, theta_dot_from0)
        self.titleTime.set_text(u"Time = {:.2f} s".format(self.times[i]))

        if self.current_pos is not None:
            self.current_pos.remove()
        self.current_pos = self.ax.scatter(theta, theta_dot, color='magenta')

        # plot predictions

        if self.predictions is not None:
            if self.preds is not None:
                self.preds[0].remove()
            self.preds = self.draw_predictions(self.predictions[i])

        return self.line1
    
    def ini_plot(self):
        self.line1.set_data(np.empty([1]), np.empty([1]))
        return self.line1
        
    def animate(self):
        line_ani = animation.FuncAnimation(
            self.fig,
            self.update_lines,
            init_func=self.ini_plot,
            frames=len(self.times)-1,
            interval=self.dt*10,
            blit=False
        )

        if self.save is True:
            current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            print(f"save path: {os.path.abspath(self.save_path)}")
            if not os.path.exists(self.save_path):
                os.makedirs(self.save_path)
            line_ani.save(f'{self.save_path}/{current_datetime}.gif', dpi=120, fps=25)
            # Update the figure with the last frame of animation
            self.update_lines(len(self.times[1:])-1)
            # Save the final frame as an SVG for good paper plots
            self.fig.savefig(f'{self.save_path}/{current_datetime}_final_frame.svg', format='svg')

        plt.show()
        return line_ani