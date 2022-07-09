import sys
import random
from random import uniform
from collections import defaultdict
from xml.etree.ElementTree import ElementTree

class Data_Helper():

    def __init__(self, work_dir=''):
        self.work_dir = work_dir

    def get_elem_with_attr(self, xml_file, elem_name, attr_list=[]):
        elem_list = []
        tree = ElementTree(file=xml_file)
        for node in tree.iterfind(elem_name):
            flag = True
            for attr in attr_list:
                if '=' in attr:
                    if node.get(attr.split('=')[0]) != attr.split('=')[1]:
                        flag = False
                        continue
                else:
                    if node.get(attr) is None:
                        flag = False
                        continue
            if flag:
                elem_list.append(node)
        return elem_list

    def random_routes(self, net_file, route_file, n_vehicle=10000, max_edge_num=30, start_time=1, max_intv=1):
        dead_end_ids = list(map(lambda x: x.get('id'), self.get_elem_with_attr(net_file, 'junction', ['type=dead_end'])))
        traffic_light_ids = list(map(lambda x: x.get('id'), self.get_elem_with_attr(net_file, 'junction', ['type=traffic_light'])))
        all_edges = self.get_elem_with_attr(net_file, 'edge')
        start_edges = []
        end_edges = []
        middle_edges = []
        for e in all_edges:
            if e.get('from') in dead_end_ids:
                start_edges.append(e.get('id'))
            if e.get('to') in dead_end_ids:
                end_edges.append(e.get('id'))
            if e.get('from') in traffic_light_ids and e.get('to') in traffic_light_ids:
                middle_edges.append(e.get('id'))
        all_connections = self.get_elem_with_attr(net_file, 'connection')
        edge_dict = defaultdict(list)
        valid_edges = start_edges + end_edges + middle_edges
        for c in all_connections:
            if c.get('from') in valid_edges and c.get('to') in valid_edges:
                if c.get('to') not in edge_dict[c.get('from')]:
                    edge_dict[c.get('from')].append(c.get('to'))
        routes = []
        c = 0
        while c < n_vehicle:
            route = []
            last_edge = random.choice(start_edges)
            route.append(last_edge)
            e_count = 1
            while True:
                invalid = False
                next_edge = random.choice(edge_dict[last_edge])
                e_count += 1
                if e_count > max_edge_num:
                    invalid = True
                    break
                elif next_edge in end_edges:
                    route.append(next_edge)
                    break
                else:
                    route.append(next_edge)
                    last_edge = next_edge
            if invalid:
                continue
            routes.append(route)
            c += 1
        with open(route_file, 'w', encoding='utf-8') as f:
            prefix = ''
            new_line = '\n'
            f.write(prefix)
            f.write('<?xml version="1.0" encoding="UTF-8"?>')
            f.write(new_line)
            f.write(prefix)
            f.write(
                '<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">')
            f.write(new_line)
            prefix += '\t'
            f.write(prefix)
            f.write('<vType id="passenger" speedFactor="normc(1.00,0.10,0.20,2.00)" vClass="passenger"/>')
            f.write(new_line)
            prev_depart = start_time
            for idx, r in enumerate(routes):
                this_depart = prev_depart + uniform(0, max_intv)
                f.write(prefix)
                f.write('<vehicle id="veh' + str(idx) + '" type="passenger" depart="' + str(
                    round(this_depart, 2)) + '" departLane="best">')
                f.write(new_line)
                prefix += '\t'
                f.write(prefix)
                f.write('<route edges="' + ' '.join(r) + '"/>')
                f.write(new_line)
                prefix = prefix[0:-1]
                f.write(prefix)
                f.write('</vehicle>')
                f.write(new_line)
                prev_depart = this_depart
            prefix = prefix[0:-1]
            f.write(prefix)
            f.write('</routes>')

if __name__ == '__main__':
    net_file = r'data/exp.net.xml'
    route_file = r'data/exp.rou.xml'
    data_helper = Data_Helper()
    data_helper.random_routes(net_file, route_file)