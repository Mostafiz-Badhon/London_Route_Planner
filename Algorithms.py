from DoublyLinkedList import DoublyLinkedList as DDList
from collections import namedtuple
from operator import attrgetter


class Station:
    """
    Creates a station class object which contains the necessary attribute to perform the Dijkstra algorithm.
    """
    def __init__(self, station_name, train_line):
        self.station_name = station_name
        self.train_line = train_line
        self.distance = float("inf")
        self.neighbours = DDList()
        self.previous = None
        self.via_line = None

    def add_neighbour(self, station):
        self.neighbours.add_first(station)

    def return_neighbours(self):
        return self.neighbours.traverse_all()


class Graph:
    """
    Creates a Graph with the provided information (edges and nodes) and contains a function that calculates the shortest
    path between two given stations/nodes.
    """
    def __init__(self, edges, nodes):
        # Allows us to correctly read the parsed data from the table and stores each record as tuples in a list.
        self.Edge = namedtuple('Edge', ['line', 'start', 'end', 'weight'])
        self.Node = namedtuple('Node', ['line', 'station'])
        self.edges = [self.Edge(*edge) for edge in edges]
        self.nodes = [self.Node(*node) for node in nodes]
        # Creates a list of all the station names.
        self.stations = [n.station for n in self.nodes]

    def dijkstra(self, start, finish):
        # Check if the starting node is in the data set.
        assert start in self.stations
        assert finish in self.stations
        # Create a list to store all the station nodes (Doubly Linked List 1)
        station_data = DDList()
        for station in range(len(self.stations)):
            current_prev = Station(self.nodes[station].station, self.nodes[station].line)
            if self.stations[station] == start:
                current_prev.distance = 0
            station_data.add_first(current_prev)
        # Searches through the edges list and updates each station with their relevant neighbours. - bi-directional.
        for line, start, end, weight in self.edges:
            station1 = next((x for x in station_data.traverse_all() if x.station_name == start), None)
            station1.add_neighbour((end, weight, line))
            station2 = next((x for x in station_data.traverse_all() if x.station_name == end), None)
            station2.add_neighbour((start, weight, line))

        all_station_data = station_data.traverse_all()
        # Create a queue and add all the stations to be processed. - Gives back a list containing station objects.
        queue = station_data.traverse_all()
        while queue:
            # Grabs the shortest path of the available nodes in the queue. Initially, it'll choose the start.
            current_smallest = min(queue, key=attrgetter("distance"))
            queue.remove(current_smallest)
            # If there are no more shortest connected neighbours or it has reached its target, then break.
            if current_smallest.distance == float("inf") or current_smallest.station_name == finish:
                break
            # Check the neighbours of the current node and update their distances/values if a shorter route is found.
            for neighbours in current_smallest.return_neighbours():
                node, weight, line = neighbours
                next_path = current_smallest.distance + weight
                for station in station_data.traverse_all():
                    if station.station_name == node and next_path < station.distance:
                        # The '+ 1' takes into account of the time needed to wait at each station.
                        station.distance = next_path + 1
                        station.previous = current_smallest.station_name
                        station.via_line = line
        # Creates Doubly Linked List containers for shortest path, sum of the time after arriving at each station and
        # the train line at each station.
        shortest_path = DDList()
        stepped_dist = DDList()
        stepped_line = DDList()

        # Sets the initial value to trace back as the final station.
        current_prev = finish
        # Identifies the initial previous value of the final station.
        temp_value = next((x for x in all_station_data if x.station_name == current_prev), None)
        current_prev = temp_value.previous
        # Adds the first sets of initial values.
        shortest_path.add_last(finish)
        finish_ = next((x for x in all_station_data if x.station_name == finish), None)
        stepped_dist.add_last(finish_.distance)
        stepped_line.add_last(finish_.via_line)
        # Traverses backwards from the target node to locate and store the shortest path.
        while True:
            if current_prev is None:
                break
            station1 = next((x for x in all_station_data if x.station_name == current_prev), None)
            shortest_path.add_first(current_prev)
            stepped_dist.add_first(station1.distance)
            if station1.via_line is not None:
                stepped_line.add_first(station1.via_line)
            else:
                stepped_line.add_first(stepped_line.get_head())
            current_prev = station1.previous

        return shortest_path.traverse_all(), stepped_dist.traverse_all(), stepped_line.traverse_all(), finish_.distance
