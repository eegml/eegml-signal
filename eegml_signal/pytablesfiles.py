# -*- coding: utf-8 -*-
from __future__ import print_function, division
from builtins import range
from builtins import object
import tables # could use h5py instead


class H5EegFile(object):
    def open(self,fn):
        datafile = tables.openFile(fn)
        self.datafile = datafile
        return datafile

    def read_into_memory(self):
        """reads everyting into memory and creates convenience structures"""
        
        h5f = self.datafile

        sig = h5f.getNode("/signals").read()
        fss = h5f.getNode("/signal_sample_freqs").read()
        labels= h5f.getNode('/signal_text_labels').read()

        self.sig = sig
        self.fss = fss
        self.labels = labels

        self._make_convenience_structures()

    def _make_convenience_structures(self):
        labels = self.labels
        # make convenience functions for mapping labels to channel number
        self.nilabels = [[ii,labels[ii]] for ii in range(len(labels))]
        self.inlabels = [[labels[ii],ii] for ii in range(len(labels))]
        # ordered dict would be useful
        self.dnilabels = dict(self.nilabels)
        self.dinlabels = dict(self.inlabels)
        
        
