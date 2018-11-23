import multiprocessing as mp
import time

import matplotlib.pyplot as plt


# adapted from https://matplotlib.org/gallery/misc/multiprocess_sgskip.html
# by Robert Cimrman

class PlotHelper(object):
    """
    Plot helper class, assists with multithreading
    """

    def __init__(self, args):
        """
        Set up structures for plotting
        :param args: Our global parameter dictionary
        """
        self.args = args
        self.sender, receiver = mp.Pipe()
        self.plotter = RealPlotter()
        self.plot_process = mp.Process(
            target=self.plotter, args=(receiver,), daemon=True)
        self.plot_process.start()

    def plot(self, finished=False):
        """
        Moves data into the pipe, and signals the other process that something is waiting
        :param finished: Default to false, if changed to true,
        """
        send = self.sender.send
        if finished:
            send(None)
        else:
            data = (self.args['time'], self.args['max'], self.args['mean'])
            send(data)


class RealPlotter(object):
    """
    This class plots data received from the multiprocessing pipe
    """

    def __init__(self):
        """ Dummy initializer, reserved for future use """
        pass

    def terminate(self):
        """ Signal to the plot to close """
        plt.close('all')

    def call_back(self):
        """ Callback to receive pipe data """

        # Poll the pipe
        while self.pipe.poll():
            # Look inside of the pipe and take the_box
            the_box = self.pipe.recv()

            # If the_box is empty, it's game over
            if the_box is None:
                self.terminate()
                return False

            # Otherwise, update the plot with the tools in the_box
            else:
                # Get our elapsed time
                elapsed_time = time.time() - the_box[0]

                # Add the elements to the plot
                self.ax.plot(elapsed_time, the_box[1], '.r-')
                self.ax.plot(elapsed_time, the_box[2], 'xb-')

        # Redraw the canvas
        self.fig.canvas.draw()
        return True

    def __call__(self, pipe):
        """ Support method for callback """
        self.pipe = pipe
        self.fig, self.ax = plt.subplots()
        timer = self.fig.canvas.new_timer(interval=10)
        timer.add_callback(self.call_back)
        timer.start()
        plt.show()
