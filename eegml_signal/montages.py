# -*- coding: utf-8 -*-
from __future__ import print_function, division
from builtins import map
from builtins import object
double_banana="""
Fp1-F7
F7-T3
T3-T5
T5-O1

Fp2-F8
F8-T4
T4-T6
T6-O2

Fp1-F3
F3-C3
C3-P3
P3-O1

Fp2-F4
F4-C4
C4-P4
P4-O2

Fz-Cz
Cz-Pz
"""

eye_leads_ekg="""
PG1
PG2
EKG
"""


tcp = """
Fp1-F7
F7-T3
T3-T5
T5-O1

Fp2-F8
F8-T4
T4-T6
T6-O2

A1-T3
T3-C3
C3-Cz
Cz-C4
C4-T4
T4-A2

Fp1-F3
F3-C3
C3-P3

Fp2-F4
F4-C4
C4-P4
"""

# beckett # wrote his name
# electrode names in the expanded 10-10 system, by row 
# longitudinal_electrode_names10_10 = [
#     ['T2', 'a2'],  # most right lateral
#     ['f8', 'ft8', 't4', 'tp8', 't6', 'pO8'],    # right lateral chain
#     ['af8', 'f6','fc6', 'c6', 'cp6', 'p6'],     # middle-lateral chain
#     ['fp2','af4','f4','fc4','c4', 'cp4','p4','po4','o2'], # right-central "banana" chain
#     ['f2','fc2','c2','cp2','p2'], # inner parasagital
#     ["Nz", "Fpz","Afz","Fz", "Fcz", "Cz", "Cpz", "Pz", "POz", "Oz"], # midline chain
#     ['f1', 'fc1', 'c1', 'cp1', 'p1'], # left inner parasagital chain
#     ['fp1','af3', 'f3','fc3','c3','cp3', 'p3', 'po3','o1'], # left-central "banana" chain
#     ['af7','f5','fc5','c5','cp5','p5'], # left middle-lateral chain
#     ['f7', 'ft7', 't3', 'tp7', 't5','po7'], # left lateral chain
#     ['t1', 'a1'] ] # left-most lateral chain
# ELECTRODE_NAMES = []
# for ll in longitudinal_electrode_names10_10:
#     print ll
#     ll = [ii.upper() for ii in ll]
#     ELECTRODE_NAMES.append(ll)

# added T1/T2 to 10_10 
electrode_names10_10 = [['T2', 'A2'],# right most-lateral
                        ['F8', 'FT8', 'T4', 'TP8', 'T6', 'PO8'], # right lateral chain
                        ['AF8', 'F6', 'FC6', 'C6', 'CP6', 'P6'],  # middle-lateral chain
                        ['FP2', 'AF4', 'F4', 'FC4', 'C4', 'CP4', 'P4', 'PO4', 'O2'], # right-central "banana" chain
                        ['F2', 'FC2', 'C2', 'CP2', 'P2'], # right inner parasagital
                        ['NZ', 'FPZ', 'AFZ', 'FZ', 'FCZ', 'CZ', 'CPZ', 'PZ', 'POZ', 'OZ'], # midline chain
                        ['F1', 'FC1', 'C1', 'CP1', 'P1'], # left inner parasagital chain
                        ['FP1', 'AF3', 'F3', 'FC3', 'C3', 'CP3', 'P3', 'PO3', 'O1'], # left-central "banana" chain
                        ['AF7', 'F5', 'FC5', 'C5', 'CP5', 'P5'], # left middle-lateral chain
                        ['F7', 'FT7', 'T3', 'TP7', 'T5', 'PO7'], # left lateral chain
                        ['T1', 'A1']] # left-most lateral chain

other_electrodes = ["X1", "X2", "X3","X4", "PG1", "PG2", "EKG"]
import itertools
def flatten(listOfLists):
    "Flatten one level of nesting"
    return itertools.chain.from_iterable(listOfLists)

geomelectrodes = list(flatten(electrode_names10_10))

import networkx as nx
# G1020 = 10-20 + T1/T2 graph
G20 = nx.Graph()
#G.add_nodes_from(['A2', 'T4', 'T2'])

G20.add_edges_from([('T2', 'A2'), ('T2','F8')]) # T2
G20.add_edges_from([('A2', 'T2'),('A2', 'T4')])
G20.add_edges_from([('F8', 'T2'), ('F8', 'FP2'), ('F8', 'T4'), ('F8', 'F4')])
G20.add_edges_from([('T4', 'F8'), ('T4', 'C4'), ('T4', 'T6'), ('T4', 'A2')])
G20.add_edges_from([('T6', 'T4'), ('T6', 'P4'), ('T6', 'O2')])
G20.add_edges_from([('O2', 'P4'), ('O2', 'O1'), ('O2', 'T6')])
G20.add_edges_from([('FP2', 'PG2'), ('FP2', 'FP1'), ('FP2', 'F4'),('FP2', 'F8')])
G20.add_edges_from([('F4', 'FP2'), ('F4', 'FZ'), ('F4', 'C4'), ('F4', 'F8')])
G20.add_edges_from([('C4', 'F4'), ('C4', 'CZ'), ('C4', 'P4'), ('C4', 'T4')])
G20.add_edges_from([('P4', 'C4'), ('P4', 'PZ'), ('P4', 'O2'), ('P4', 'T6')])

G20.add_edges_from([('FZ', 'CZ'),('CZ', 'PZ')]) # midline chain
# now iterate clockwise
G20.add_edges_from([('P3', 'C3'), ('P3', 'PZ'), ('P3', 'O1'), ('P3', 'T5')])
G20.add_edges_from([('C3', 'F3'), ('C3', 'CZ'), ('C3', 'P3'), ('C3', 'T3')])
G20.add_edges_from([('F3', 'FP1'), ('F3', 'FZ'), ('F3', 'C3'), ('F3', 'F7')])
G20.add_edges_from([('FP1', 'PG1'), ('FP1', 'FP1'), ('FP1', 'F3'),('FP1', 'F7')])
G20.add_edges_from([('O1', 'P3'), ('O1', 'O1'), ('O1', 'T5')])
G20.add_edges_from([('T5', 'T3'), ('T5', 'P3'), ('T5', 'O1')])
G20.add_edges_from([('T3', 'F7'), ('T3', 'C3'), ('T3', 'T5'), ('T3', 'A1')])
G20.add_edges_from([('F7', 'T1'), ('F7', 'FP1'), ('F7', 'T3'), ('F7', 'F3')])
G20.add_edges_from([('A1', 'T1'), ('A1', 'T3')])
G20.add_edges_from([('T1', 'A1'), ('T1','F7')]) # T1

# if matplotlib has been imported, can draw this with:
#   nx.draw(G20)
#   figure(); nx.draw_graphviz(G20) # which islikely to look nice
#   figure(); nx.draw_spectral(G20) # which is my favorite so far

                 
# 10-10 graph
# G.add_edges_from([('F8', 'FT8'),('FT8', 'T4'),('T4', 'TP8'),('TP8', 'T6'),('T6', 'PO8')]

# read coordinates
# import csv
csdrdr = file('util/10-5-System_Mastoids_EGI129.csd')
csd10_5_coordinates_txt = [row.split() for row in csdrdr]
csd10_5_hdr = ['Label', 'Theta', 'Phi', 'Radius', 'X', 'Y', 'Z', 'off sphere surface']
csd10_5_coordinates = [[row[0]]+list(map(float,row[1:])) for row in csd10_5_coordinates_txt[2:]]
csd10_5 = dict([(row[0].upper(),list(map(float,row[1:]))) for row in csd10_5_coordinates_txt[2:]])
csd10_5['T3'] = csd10_5['T7']
csd10_5['T4'] = csd10_5['T8']
csd10_5['T5'] = csd10_5['P7']
csd10_5['T6'] = csd10_5['P8']
# now I'm going to approximate things, I should get a better value later. See util/Notes.txt
csd10_5['T1'] = csd10_5['FT9'] # think this is closest match per util/Notes.txt Oostenveld's email
csd10_5['T2'] = csd10_5['FT10']
# to draw all the electrode coordinates can do:
# I'm not sure if this is working
def display_10_5_on_sphere():
    import mayavi.mlab as mlb
    print("here are csd10_5_coordinates")
    for it in csd10_5_coordinates:
        print(it)
        # mlb.points3d(it[4], it[5], it[6],mode='sphere', scale_factor=0.05) #name = label

    lbl = 'FP1'; x,y,z = csd10_5[lbl][3], csd10_5[lbl][4], csd10_5[lbl][5]
    mlb.points3d(x,y,z, mode='sphere', scale_factor=0.05, color=(1.0,0.,0.), name=it[0])

def display_10_10_on_sphere():
    # display the 10-10 system
    import mayavi.mlab as mlb
    import time

    X = [csd10_5[it][3] for it in geomelectrodes]
    Y = [csd10_5[it][4] for it in geomelectrodes]
    Z = [csd10_5[it][5] for it in geomelectrodes]
    all_points = mlb.points3d(X,Y,Z,scale_mode='none', scale_factor=0.05)

    # for it in geomelectrodes:
    #     x,y,z = csd10_5[it][3], csd10_5[it][4], csd10_5[it][5]
    #     mlb.points3d(x,y,z, mode='sphere', scale_factor=0.05, name=it)
    #     print(it, x, y, z)    
	# time.sleep(0.1)
    mesh = mlab.pipeline.delaunay2d(all_points)
    surf = mlab.pipeline.surface(mesh)

    # mark FP1 red
    lbl = 'FP1'; x,y,z = csd10_5[lbl][3], csd10_5[lbl][4], csd10_5[lbl][5]
    mlb.points3d(x,y,z, mode='sphere', scale_factor=0.05, color=(1.0,0.,0.))


class EEGMontage(object):
    """
    This maps original chanels


    """
    def __init__(self):
        self.record = None
        self.name2index = {}
        self.gain = None # np.ones(self.record.numchan)
        self.bipolar = None # shape = (2,self.record.numchan)
        # display[ii] = gain[ii] * eeg[bipolar[0][ii]]-eeg[bipolar[1][ii]]



def parse_text_montage(mtd):
    pass

if __name__ == '__main__':
    print("with ipython 0.10 run this with ipython -wthread")
    print("with ipython 0.11 run with ipython --pylab=wx")
    print("run montages.py")
    print("display_10_10_on_sphere()")
    print("mlab.show()")
    print("""might also want to try: nx.draw_spectral(G20)""")

    import mayavi.mlab as mlab
    display_10_10_on_sphere()
    # display_10_5_on_sphere()
    mlab.show()
