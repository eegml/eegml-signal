# note this doesn't quite work because:
# 1. the names of the signals must include the right number of spaces
# this doesn't happen for EEG FP1 and FP2

# note that in edf browser "up is positive" not negative as in EEG

headr="""<?xml version="1.0"?>
<EDFbrowser_montage>
"""
footr="""
  <pagetime>100000000</pagetime>
</EDFbrowser_montage>
"""

fp1='EEG FP1         '
f7 ='EEG F7          '
t3 ='EEG T3          '
t5 ='EEG T5          '
o1 ='EEG O1          '
f3 ='EEG F3          '
c3 ='EEG C3          '
p3 ='EEG P3          '

fp2='EEG FP2         '
f8 ='EEG F8          '
t4 ='EEG T4          '
t6 ='EEG T6          '
o2 ='EEG O2          '

f4 ='EEG F4          '
c4 ='EEG C4          '
p4 ='EEG P4          '

cz ='EEG CZ          '
fz ='EEG FZ          '
pz ='EEG PZ          '

t1 ='EEG T1          '
t2 ='EEG T2          '
x1 ='EEG X1          '
x2 ='EEG X2          '
# colors
left=10
right=9
center=7

db = [
    (fp1,f7,left),
    (f7,t3, left),
    (t3,t5, left),
    (t5,o1, left),
    
    (fp2, f8, right),
    (f8, t4, right),
    (t4, t6, right),
    (t6, o2, right),

    (fp1, f3, left),
    (f3, c3, left),
    (c3, p3, left),
    (p3, o1, left),

    (fp2, f4,right),
    (f4, c4, right),
    (c4, p4, right),
    (p4, o2, right),

    (fz, cz, center),
    (cz, pz, center),
    ]

dbplus = db + [
    (


sp = [
    
    ]

tcp = [
    ]

circle = [
    ]

ref = [
    ]


def signalcomposition(sig1,sig2,color):
    templ = """<signalcomposition>
    <num_of_signals>2</num_of_signals>
    <voltpercm>100.000000</voltpercm>
    <screen_offset>0.000000</screen_offset>
    <color>%(color)s</color>
    <filter_cnt>0</filter_cnt>
    <fidfilter_cnt>0</fidfilter_cnt>
    <signal>
      <label>%(sig1)s</label>
      <factor>1</factor>
    </signal>
    <signal>
      <label>%(sig2)s</label>
      <factor>-1</factor>
    </signal>
  </signalcomposition>
"""
    # **kw ?
    d={'sig1':sig1,'sig2':sig2,'color':color}
    return templ % d

def make_double_banana():
    print headr
    for (sig1,sig2,color) in db:
        print signalcomposition(sig1,sig2,color)
    print footr


# class EdfbrowserMontageNode(object):
#     def __init__(self):
#         self.setup_defaults()
        
#     def setup_defaults(self):
#         self.voltpercm = 100.0
#         self.screen_offset = 0.0
#         self.color = 2 # default
#         self.filter_cnt = 2
#         self.fidfilter_cnt = 2
#         self.ravg_filter_cnt = 0
#         self.signals = []


#         """
#             <signal>
#               <label>%(label)s</label>
#               <factor>%(factor)s</factor>
#             </signal>
#         """
#         self.template="""
#     <signalcomposition>
#     <num_of_signals>%(num_of_signals)s</num_of_signals>
#     <voltpercm>%(voltpercm)s</voltpercm>
#     <screen_offset>%(screen_offset)</screen_offset>
#     <color>%(color)</color>
#     <filter_cnt>%(filter_cnt)s</filter_cnt>
#     <fidfilter_cnt>%(fidfilter_cnt)s</fidfilter_cnt>
#     <ravg_filter_cnt>%(ravg_filter_cnt)s</ravg_filter_cnt>
#     %(signals)s
#     <fidfilter>
#       <type>0</type>
#       <frequency>1.0000000000000000</frequency>
#       <frequency2>2.0000000000000000</frequency2>
#       <ripple>-1.0000000000000000</ripple>
#       <order>1</order>
#       <model>0</model>
#     </fidfilter>
#     <fidfilter>
#       <type>1</type>
#       <frequency>50.0000000000000000</frequency>
#       <frequency2>56.0000000000000000</frequency2>
#       <ripple>-1.0000000000000000</ripple>
#       <order>1</order>
#       <model>0</model>
#     </fidfilter>
#   </signalcomposition>
#   """

        


if __name__=='__main__':
    make_double_banana()

