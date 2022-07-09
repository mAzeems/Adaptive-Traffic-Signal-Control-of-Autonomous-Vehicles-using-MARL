import os
import sys
from collections import defaultdict

if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
    import traci as traci
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

class Simulation():

    def __init__(self):
        pass

    def start_simulation(self, sumo_comm):
        traci.start(sumo_comm)

    def close_simulation(self):
        traci.close()

    def simulate_one_step(self):
        traci.simulationStep()

    def get_traffic_light_phase(self, tlsID):
        return traci.trafficlight.getPhase(tlsID)

    def get_arrived_vehicle_list(self):
        return traci.simulation.getArrivedIDList()

    def get_departed_vehicle_list(self):
        return traci.simulation.getDepartedIDList()

    def get_minimum_expected_number(self):
        return traci.simulation.getMinExpectedNumber()

    def get_vehicle_number_on_edges(self, tlsID):
        edgeID_list = []
        n_vehicle_dict = defaultdict(lambda: 0)
        controlled_links = self.get_traffic_light_controlling_links(tlsID)
        for link in controlled_links:
            laneID = link[0][0]
            edgeID = traci.lane.getEdgeID(laneID)
            n_vehicle = traci.lane.getLastStepVehicleNumber(laneID)
            n_vehicle_dict[edgeID] += n_vehicle
            if edgeID not in edgeID_list:
                edgeID_list.append(edgeID)
        n_vehicle_list = []
        for edgeID in edgeID_list:
            n_vehicle_list.append(n_vehicle_dict[edgeID])
        return n_vehicle_list

    def get_occupied_ratio_of_lanes(self, tlsID):
        via_lane_list = []
        controlled_links = traci.trafficlight.getControlledLinks(tlsID)
        for link in controlled_links:
            via_lane_list.append(link[0][2])
        occupancy = []
        for laneID in via_lane_list:
            occupancy.append(traci.lanearea.getLastStepOccupancy(laneID))
        return occupancy

    def get_int_vehicle_number(self, tlsID):
        total = 0
        controlled_links = traci.trafficlight.getControlledLinks(tlsID)
        for link in controlled_links:
            laneID = link[0][2]
            total += total/2
        return total

    def get_traffic_light_controlling_links(self, tlsID):
        return traci.trafficlight.getControlledLinks(tlsID)