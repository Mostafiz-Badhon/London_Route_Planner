from tkinter import *
from tkinter import ttk
from itertools import groupby
import tkinter.messagebox as mb
import pandas as pd
import Algorithms as Alg
import time
import matplotlib.pyplot
closed_station = ""
start = time.time()

print(23*2.3)

end = time.time()
print(end - start)



class MainWindow:
    """
    This is the MAIN python file you must run in order to execute this program.

    'MainWindow' contains the initial window. The user can select their starting and finishing station as well as the
    time at which they wish to traverse the London Underground network.
    """
    def __init__(self, master):
        # Initialise the main window configurations.
        self.master = master
        self.master.title("London Underground Route Planner")
        self.master.geometry("800x800")
        self.frame = Frame(self.master, bg="grey")
        self.frame.pack()

        # Creates a title text label.
        self.label_title = Label(self.frame, text="London Underground Journey Planner", bg="azure", width="350",
                                 relief="ridge", height="6", bd=5, font=("Helvetica", 14, "italic")).pack(pady=20)

        # Loads the excel document.
        self.data = pd.read_excel("London Underground Data.xlsx", header=None)
        self.df = pd.DataFrame(self.data)
        self.df.plot(kind='hist')
        matplotlib.pyplot.show()
        # Removes any empty/white spaces before and after an entry to reduce errors.
        for i in range(len(self.df.columns) - 1):
            self.df[i] = self.df[i].str.strip()

        # If the 'Time' column is null, then that row is added to the nodes DataFrame and any null cells are dropped.
        self.df_nodes = self.df[pd.isna(self.df[3])].dropna(axis=1, how="all")
        self.records_nodes = list(self.df_nodes.to_records(index=False))
        # Creates a list of all unique values of stations and sorts them into alphabetical order.
        self.unique_nodes = sorted(list(self.df_nodes[1].unique()))

        # Checks all the rows and puts anything that has a value in the 'Time' (fourth) column into df_edges.
        self.df_edges = self.df[self.df[3] > 0]
        self.records_edges = list(self.df_edges.to_records(index=False))

        # Updated sped up Bakerloo line for during specified times.
        self.records_speed_edges = list(self.df_edges.to_records(index=False))
        for edge in self.records_speed_edges:
            if edge[0] == "Bakerloo":
                edge[3] = edge[3] / 2

        # Combo box and label for the starting and finishing station.
        self.label_start = Label(self.frame, text="Starting Station").pack()
        self.input_start = ttk.Combobox(self.frame, values=self.unique_nodes, width="30",
                                        state="readonly")
        self.input_start.pack(pady=10)
        self.label_finish = Label(self.frame, text="Target Station").pack()
        self.input_finish = ttk.Combobox(self.frame, values=self.unique_nodes, width="30",
                                         state="readonly")
        self.input_finish.pack(pady=10)

        # Declare input variables for time.
        self.time_hour = StringVar()
        self.time_hour.set(0)
        self.time_min = StringVar()
        self.time_min.set(0)
        # Time (hours and minutes) label and entry boxes.
        self.label_hour = Label(self.frame, text="Time (Hours: 00-24)").pack()
        self.text_hour = Entry(self.frame, textvariable=self.time_hour, width="15", bd=5)
        self.text_hour.pack(padx=10, pady=10)
        self.label_min = Label(self.frame, text="Time (Minutes: 00-60)").pack()
        self.text_min = Entry(self.frame, textvariable=self.time_min, width="15", bd=5)
        self.text_min.pack(padx=10, pady=10)

        # Continue and Exit button on the front page.
        self.process_button = Button(self.frame, text="Get Directions", height="2", width="15", bd=3, bg="grey",
                                     font=("Helvetica", 12, "bold"), command=self.entry_verification).pack(pady=10)
        self.exit_button = Button(self.frame, text="EXIT", height="2", width="10", bd=3, bg="grey",
                                  font=("Helvetica", 10, "bold"), command=self.exit_window).pack()

    # Ensures that all the entry boxes have been filled before proceeding to the algorithm and results table.
    def entry_verification(self):
        speed_up = False
        # Checks whether the input for the hour and minutes are valid.
        if str.isnumeric(self.text_hour.get()) and str.isnumeric(self.text_min.get()):
            if 0 <= int(self.text_hour.get()) <= 24 and 0 <= int(self.text_min.get()) < 60:
                # Updates whether we use the faster Bakerloo line times.
                if 9 <= int(self.text_hour.get()) < 16 or 19 <= int(self.text_hour.get()) < 24:
                    speed_up = True
                if len(self.input_start.get()) == 0 or len(self.input_finish.get()) == 0:
                    mb.showinfo("Missing Arguments", "Please ensure that all entries are filled and entered correctly.")
                elif self.input_start.get() == self.input_finish.get():
                    mb.showinfo("Error?", "The entries for the starting and finishing stations are both the same. "
                                          "You're already there!")
                else:
                    # Ensures the inputs are valid and gives the appropriate data depending on the time.
                    if self.input_start.get() and self.input_finish.get() in self.unique_nodes:
                        if speed_up:
                            self.initialise_results(self.records_speed_edges)
                        else:
                            self.initialise_results(self.records_edges)
            else:
                mb.showerror("Error!", "Invalid time parameters.")
        else:
            mb.showerror("Error!", "Time MUST contain positive numeric numbers only within the specified region.")

    # Calls the Dijkstra's path finding function, stores the values and parses it into the results table.
    def initialise_results(self, graph_edges):
        # Initialising the graph in advanced for Dijkstra's algorithm to traverse.
        graph = Alg.Graph(graph_edges, self.records_nodes)
        shortest_path, stepped_dist, stepped_line, distance = graph.dijkstra(self.input_start.get(),
                                                                             self.input_finish.get())
        self.master.destroy()
        Results(Tk(), shortest_path, stepped_dist, stepped_line, distance)

    # Method that opens a confirmation box and then terminates the program if yes.
    def exit_window(self):
        exit_ = mb.askyesno("Exit Warning!", "Are you sure you want to quit?")
        if exit_:
            self.master.destroy()


class Results:
    """
    Contains the shortest path between the two stations given, the total time required to travel to each station and the
    total accumulated time to travel from start to finish. The train lines required are also given.
    """
    def __init__(self, master, shortest_path, stepped_dist, stepped_line, distance):
        # Initialise the results window configurations that shows up after the main window.
        self.master = master
        self.master.title("Route Planner Results")
        self.master.geometry("900x500")
        self.master.config(bg='grey69')
        self.frame = Frame(self.master, bg='grey69')
        self.frame.pack()

        # Calculates the time intervals between each station.
        self.time_to_next = []
        for i in range(len(stepped_dist) - 1):
            # When calculating the travel time between stations, the 1 minute waiting time at each station is removed.
            self.time_to_next.append((stepped_dist[i + 1] - stepped_dist[i]) - 1)
        self.time_to_next.append('')

        # Creates a Treeview/Table that can display the Stations, Train Lines, Travel Time Between Stations and the
        # Total Time (Including the Idle time for passenger (dis)embarking).
        tl_cols1 = ("Station", "Train Line", "Travel Time Between Stations", "Total Time (Includes Idle Time)")
        self.box = ttk.Treeview(self.frame, columns=tl_cols1, show="headings")
        for col in tl_cols1:
            self.box.heading(col, text=col)
            self.box.column(col, anchor=CENTER)
            self.box.pack(fill=BOTH)

        # Inserts each of their respective information into the table.
        for i in range(len(shortest_path)):
            self.box.insert('', 'end', values=(shortest_path[i], stepped_line[i], self.time_to_next[i],
                                               stepped_dist[i]))

        # Journey summary label.
        self.summary_label = Label(self.frame, text="Journey Summary - Scroll down if the list is incomplete.").pack()
        self.summary1 = Text(self.frame, height=10, width=90)
        self.summary1.pack()

        # Calculates all the duplicates in train lines and finds when to switch lines.
        dupes = [(k, sum(1 for _ in g)) for k, g in groupby(stepped_line)]
        # Calculates and outputs the journey summary.
        temp_total = 0
        for i, changes in enumerate(dupes):
            start = shortest_path[max(0, temp_total - 1)]
            temp_total += changes[1]
            end = shortest_path[temp_total - 1]
            self.summary1.insert(END, changes[0] + ': ' + start + ' to ' + end + '\n')
            if i + 1 != len(dupes):
                self.summary1.insert(END, '-- Change --\n')
        self.summary1.config(state=DISABLED)

        # Displays the final distance at the bottom of the window.
        self.label_distance = Label(self.frame, text="Total Journey Time: " + str(distance) + " Minutes").pack()

        # Buttons to exit or return to the main window.
        self.back = Button(self.frame, text="Back", height="2", width="5", bd=2, font=("Helvetica", 8, "bold"),
                           bg='grey', command=self.back_main).pack(side=LEFT, fill=X, anchor=W, expand=YES)
        self.exit = Button(self.frame, text="Exit", height="2", width="5", bd=2, font=("Helvetica", 8, "bold"),
                           bg="grey", command=self.exit_window).pack(side=LEFT, fill=X, anchor=W, expand=YES)

    # Method to initialise the main window and destroy the current results table.
    def back_main(self):
        self.master.destroy()
        MainWindow(Tk())

    # Method that opens a confirmation box and then terminates the program if yes.
    def exit_window(self):
        exit_ = mb.askyesno("Exit Warning!", "Are you sure you want to quit?")
        if exit_:
            self.master.destroy()


# Initialises the main window and keeps the program running until exited.
if __name__ == '__main__':
    root = Tk()
    MainWindow(root)
    root.mainloop()