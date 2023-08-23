import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# imports EvoSim class
from EvoSim import EvoSim

class GraphSim:
    def __init__(self, root):
        self.root = root
        self.parameters = [500, 1000, 10, 3000, 100, 0.9, 0.1, 0.1, 500, 0.1]  # Initializes parameter list
        
        # Erstellen Sie Schieberegler mit Echtzeit-Aktualisierung
        slider_info = [
            ("Population Size:", 1, 1000),
            ("Generations:", 1, 1000),
            ("Runs:", 1, 100),
            ("Capacity:", 1, 2000),
            ("Initial Mutants:", 0, 100),
            ("Growth Rate:", 0, 1),
            ("Mutation Benefit:", 0, 1),
            ("Bottleneck Timestamp:", 1, 1500),
        ]
        #("Decimation Factor:", 0.1, 0.9)
        self.slider_list = []

        for label_text, min_value, max_value in slider_info:
            label = ttk.Label(self.root, text=label_text)
            label.pack()
            slider = ttk.Scale(self.root, from_=min_value, to=max_value, orient="horizontal")
            slider.set(self.parameters[self.slider_list.__len__()])
            slider.pack()
            slider.configure(command=lambda value, slider=slider: self.update_parameters(slider))
            self.slider_list.append(slider)
        
        # self.create_graph()
        self.simulation = EvoSim(self.parameters)  # creates EvoSim instance
        self.update_parameters(slider)
        
        
    # def create_graph(self):
    #     self.figure, self.ax = plt.subplots(figsize=(8, 6))
    #     self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
    #     self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def update_parameters(self, slider):
        self.parameters = [slider.get() for slider in self.slider_list]
        self.simulation.parameters = self.parameters
        simulation_results = self.run_simulation()
        self.draw_graph(simulation_results)

    def draw_graph(self,simulation_results):
        self.ax.clear()
        self.ax.set_xlabel("Generations")
        self.ax.axvline(x=self.parameters[7], color='r', linestyle='--')
        self.ax.set_ylabel("p")

        for simulation in simulation_results[0]:
            self.ax.plot(simulation[0], simulation[1], color="green")

        plt.suptitle("WRIGHT FISHER")
        subtext = f"initialMutants = {str(self.parameters[4])}; population = {str(self.parameters[0])}; fitnessBenefit ={str(self.parameters[6] * 100)}%; maxGenerations = {str(self.parameters[1])}; runs ={str(self.parameters[2])}"
        plt.legend(title='Legend')
        plt.title(subtext, fontsize=10, color='gray')
        self.canvas.draw()  
        
    def run_simulation(self):
        return self.simulation.combinedSimulation()

def main():
    root = tk.Tk()
    root.title("Simulation of the Wright-Fisher-Model")
    gui = GraphSim(root)
    root.mainloop()

if __name__ == "__main__":
    main()