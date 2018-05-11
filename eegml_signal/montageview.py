# -*- coding: utf-8 -*-
"""
In clinical EEG a montage is what we will call a montage view (MontageView)
here. It is generally a linear combinations of the originnal electrodes chosen to
make it easier to see clinear features. Each one will have different advantages
and disadvantages. Bipolar montages are less sensitive to noise. Average or
referential montages may be more sensitive or make it easier to view generalized
discharges. One montage may make localizing temporal events easier while another
focuses on occipital events.
"""
import xarray

# Anyone may wish to define a montageview, but there are quite a few standard ones
# to define these we need a standard ordering of electrodes in which to define them.

DOUBLE_BANANA = """
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
DB_LABELS = [
    'Fp1-F7', 'F7-T3', 'T3-T5', 'T5-O1', 'Fp2-F8', 'F8-T4', 'T4-T6', 'T6-O2',
    'Fp1-F3', 'F3-C3', 'C3-P3', 'P3-O1', 'Fp2-F4', 'F4-C4', 'C4-P4', 'P4-O2',
    'Fz-Cz', 'Cz-Pz'
]

eye_leads_ekg = """
PG1
PG2
EKG
"""

TCP = """
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
TCP_LABELS = [
    'Fp1-F7', 'F7-T3', 'T3-T5', 'T5-O1', 'Fp2-F8', 'F8-T4', 'T4-T6', 'T6-O2',
    'A1-T3', 'T3-C3', 'C3-Cz', 'Cz-C4', 'C4-T4', 'T4-A2', 'Fp1-F3', 'F3-C3',
    'C3-P3', 'Fp2-F4', 'F4-C4', 'C4-P4'
]


#---------------------------------------------------------------
# raw_labels -> montage_labels
# N=len(raw_labels) >= M = len(montage_labels)
class MontageView(object):
    def __init__(self):
        self.labels  #  text names of electrodes
        elabels = self.labels
        #  standard text (i.e. with
        # label-2-standard-index enumerate them
        l2si = {elabels[ii]: ii for ii in range(len(elabels))}

    # alternatively it may make sense to simply use xarray to define the x,y coordinates
    def __call__(self, sx, sy):
        """
        matrix access via labels translate from label s1 (basis) to s2 (basis)
        """
        #sx = sx.upcase() # maybe, maybe not
        #sy = sy.upcase()
        return self.V.loc[sx, sy]


# V defaults  to 0, using clinical 10-20 system


def double_banana(raw_labels):
    """specify the double banana transformation for raw input labels
    return an xarray-like matrix V ?"""
    N = len(raw_labels)
    M = len(DB_LABELS)
    V = xarray.DataArray(
                         np.zeros(shape=(M, N)),
                         dims=('x', 'y'),
                         coords={'x': DB_LABELS,
                                 'y': raw_labels})

    V('Fp1-F7', 'Fp1') = 1
    V('Fp1-F7', 'F7') = -1
    V('F7-T3', 'F7') = 1
    V('F7-T3', 'T3') = -1
    V('T3-T5', 'T3') = 1
    V('T3-T5', 'T5') = -1
    V('T5-O1', 'T5') = 1
    V('T5-O1', 'O1') = -1

    V('Fp2-F8', 'Fp2') = 1
    V('Fp2-F8', 'F8') = -1
    V('F8-T4', 'F8') = 1
    V('F8-T4', 'T4') = -1
    V('T4-T6', 'T4') = 1
    V('T4-T6', 'T6') = -1
    V('T6-O2', 'T6') = 1
    V('T6-O2', 'O2') = -1

    V('Fp1-F3', 'Fp1') = 1
    V('Fp1-F3', 'F3') = -1
    V('F3-C3', 'F3') = 1
    V('F3-C3', 'C3') = -1
    V('C3-P3', 'C3') = 1
    V('C3-P3', 'P3') = -1
    V('P3-O1', 'P3') = 1
    V('P3-O1', 'O1') = -1

    V('Fp2-F4', 'Fp2') = 1
    V('Fp2-F4', 'F4') = -1
    V('F4-C4', 'F4') = 1
    V('F4-C4', 'C4') = -1
    V('C4-P4', 'C4') = 1
    V('C4-P4', 'P4') = -1
    V('P4-O2', 'P4') = 1
    V('P4-O2', 'O2') = -1

    V('Fz-Cz', 'Fz') = 1
    V('Fz-Cz', 'Cz') = -1
    V('Cz-Pz', 'Cz') = 1
    V('Cz-Pz', 'Pz') = -1

    return V


# EKG
# PG1
# PG2


#### TCP
def tcp(B):
    B('Fp1-F7', 'Fp1') = 1
    B('Fp1-F7', 'F7') = -1
    B('F7-T3', 'F7') = 1
    B('F7-T3', 'T3') = -1
    B('T3-T5', 'T3') = 1
    B('T3-T5', 'T5') = -1
    B('T5-O1', 'T5') = 1
    B('T5-O1', 'O1') = -1

    B('Fp2-F8', 'Fp2') = 1
    B('Fp2-F8', 'F8') = -1
    B('F8-T4', 'F8') = 1
    B('F8-T4', 'T4') = -1
    B('T4-T6', 'T4') = 1
    B('T4-T6', 'T6') = -1
    B('T6-O2', 'T6') = 1
    B('T6-O2', '02') = -1

    B('A1-T3', 'A1') = 1
    B('A1-T3', 'T3') = -1
    B('T3-C3', 'T3') = 1
    B('T3-C3', 'C3') = -1
    B('C3-Cz', 'C3') = 1
    B('C3-Cz', 'Cz') = -1
    B('Cz-C4', 'Cz') = 1
    B('Cz-C4', 'C4') = -1
    B('C4-T4', 'C4') = 1
    B('C4-T4', 'T4') = -1
    B('T4-A2', 'T4') = 1
    B('T4-A2', 'A2') = -1

    B('Fp1-F3', 'Fp1') = 1
    B('Fp1-F3', 'F3') = -1
    B('F3-C3', 'F3') = 1
    B('F3-C3', 'C3') = -1
    B('C3-P3', 'C3') = 1
    B('C3-P3', 'P3') = -1

    B('Fp2-F4', 'Fp2') = 1
    B('Fp2-F4', 'F4') = -1
    B('F4-C4', 'F4') = 1
    B('F4-C4', 'C4') = -1
    B('C4-P4', 'C4') = 1
    B('C4-P4', 'P4') = -1


####################

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
