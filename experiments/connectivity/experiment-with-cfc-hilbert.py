Python 2.6.6 (r266:84292, Sep 15 2010, 16:22:56) 
Type "copyright", "credits" or "license" for more information.

IPython 0.10.1 -- An enhanced Interactive Python.
?         -> Introduction and overview of IPython's features.
%quickref -> Quick reference.
help      -> Python's own help system.
object?   -> Details about 'object'. ?object also works, ?? prints more.

  Welcome to pylab, a matplotlib-based Python environment.
  For more information, type 'help(pylab)'.

In [1]: import scipy.signal as signal

In [2]: signal.sawtooth?
Type:		function
Base Class:	<type 'function'>
String Form:	<function sawtooth at 0x296d500>
Namespace:	Interactive
File:		/usr/lib/python2.6/dist-packages/scipy/signal/waveforms.py
Definition:	signal.sawtooth(t, width=1)
Docstring:
    Returns a periodic sawtooth waveform with period 2*pi
    which rises from -1 to 1 on the interval 0 to width*2*pi
    and drops from 1 to -1 on the interval width*2*pi to 2*pi
    width must be in the interval [0,1]


In [4]: t=arange(0,10,0.001)

In [5]: t.shape
Out[5]: (10000,)

In [6]: saw = signal.sawtooth(t)

In [8]: plot(t,saw)
Out[8]: [<matplotlib.lines.Line2D object at 0x31a0410>]

In [9]: plot(t,saw,width=1.0/(2*pi))
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)

/media/d7e7e26e-bb28-4128-9098-0043ef93dd4e/home/clee/code/eegquant/sigproc/<ipython console> in <module>()

/usr/local/lib/python2.6/dist-packages/matplotlib/pyplot.pyc in plot(*args, **kwargs)
   2284         ax.hold(hold)
   2285     try:
-> 2286         ret = ax.plot(*args, **kwargs)
   2287         draw_if_interactive()
   2288     finally:

/usr/local/lib/python2.6/dist-packages/matplotlib/axes.pyc in plot(self, *args, **kwargs)
   3781         lines = []
   3782 
-> 3783         for line in self._get_lines(*args, **kwargs):
   3784             self.add_line(line)
   3785             lines.append(line)

/usr/local/lib/python2.6/dist-packages/matplotlib/axes.pyc in _grab_next_args(self, *args, **kwargs)
    315                 return
    316             if len(remaining) <= 3:
--> 317                 for seg in self._plot_args(remaining, kwargs):
    318                     yield seg
    319                 return

/usr/local/lib/python2.6/dist-packages/matplotlib/axes.pyc in _plot_args(self, tup, kwargs)
    302         ncx, ncy = x.shape[1], y.shape[1]
    303         for j in xrange(max(ncx, ncy)):
--> 304             seg = func(x[:,j%ncx], y[:,j%ncy], kw, kwargs)
    305             ret.append(seg)
    306         return ret

/usr/local/lib/python2.6/dist-packages/matplotlib/axes.pyc in _makeline(self, x, y, kw, kwargs)
    252                      **kw
    253                      )
--> 254         self.set_lineprops(seg, **kwargs)
    255         return seg
    256 

/usr/local/lib/python2.6/dist-packages/matplotlib/axes.pyc in set_lineprops(self, line, **kwargs)
    193             funcName = "set_%s"%key
    194             if not hasattr(line,funcName):
--> 195                 raise TypeError, 'There is no line property "%s"'%key
    196             func = getattr(line,funcName)
    197             func(val)

TypeError: There is no line property "width"

In [10]: saw = signal.sawtooth(t,width=1.0/(2*pi))

In [11]: plot(t,saw,width=1.0/(2*pi))
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)

/media/d7e7e26e-bb28-4128-9098-0043ef93dd4e/home/clee/code/eegquant/sigproc/<ipython console> in <module>()

/usr/local/lib/python2.6/dist-packages/matplotlib/pyplot.pyc in plot(*args, **kwargs)
   2284         ax.hold(hold)
   2285     try:
-> 2286         ret = ax.plot(*args, **kwargs)
   2287         draw_if_interactive()
   2288     finally:

/usr/local/lib/python2.6/dist-packages/matplotlib/axes.pyc in plot(self, *args, **kwargs)
   3781         lines = []
   3782 
-> 3783         for line in self._get_lines(*args, **kwargs):
   3784             self.add_line(line)
   3785             lines.append(line)

/usr/local/lib/python2.6/dist-packages/matplotlib/axes.pyc in _grab_next_args(self, *args, **kwargs)
    315                 return
    316             if len(remaining) <= 3:
--> 317                 for seg in self._plot_args(remaining, kwargs):
    318                     yield seg
    319                 return

/usr/local/lib/python2.6/dist-packages/matplotlib/axes.pyc in _plot_args(self, tup, kwargs)
    302         ncx, ncy = x.shape[1], y.shape[1]
    303         for j in xrange(max(ncx, ncy)):
--> 304             seg = func(x[:,j%ncx], y[:,j%ncy], kw, kwargs)
    305             ret.append(seg)
    306         return ret

/usr/local/lib/python2.6/dist-packages/matplotlib/axes.pyc in _makeline(self, x, y, kw, kwargs)
    252                      **kw
    253                      )
--> 254         self.set_lineprops(seg, **kwargs)
    255         return seg
    256 

/usr/local/lib/python2.6/dist-packages/matplotlib/axes.pyc in set_lineprops(self, line, **kwargs)
    193             funcName = "set_%s"%key
    194             if not hasattr(line,funcName):
--> 195                 raise TypeError, 'There is no line property "%s"'%key
    196             func = getattr(line,funcName)
    197             func(val)

TypeError: There is no line property "width"

In [12]: plot(t,saw)
Out[12]: [<matplotlib.lines.Line2D object at 0x31a98d0>]

In [13]: t2 = arange(10.0)

In [14]: saw2 = signal.sawtooth(t2)

In [15]: figure(); plot(saw2)
Out[15]: <matplotlib.figure.Figure object at 0x31a9990>
Out[15]: [<matplotlib.lines.Line2D object at 0x34d8610>]

In [16]: saw2 = signal.sawtooth(arange(0,200,0.01)
   ....:                        )

In [17]: plot(saw2)
Out[17]: [<matplotlib.lines.Line2D object at 0x34e3450>]

In [18]: t2 = arange(0,200,0.01)

In [19]: plot(t2,saw2,hold=False)
Out[19]: [<matplotlib.lines.Line2D object at 0x34c2f50>]

In [20]: fs = 0.01

In [21]: import filters

In [22]: filters.PassBand?
Type:		type
Base Class:	<type 'type'>
String Form:	<class 'filters.PassBand'>
Namespace:	Interactive
File:		/media/d7e7e26e-bb28-4128-9098-0043ef93dd4e/home/clee/code/eegquant/sigproc/filters.py
Docstring:
        

Constructor information:
Definition:	filters.PassBand(self)


In [29]: figure()
Out[29]: <matplotlib.figure.Figure object at 0x34dcf90>

In [30]: specgram?
Type:		function
Base Class:	<type 'function'>
String Form:	<function specgram at 0x277aed8>
Namespace:	Interactive
File:		/usr/local/lib/python2.6/dist-packages/matplotlib/pyplot.py
Definition:	specgram(x, NFFT=256, Fs=2, Fc=0, detrend=<function detrend_none at 0x2135c80>, window=<function window_hanning at 0x212fed8>, noverlap=128, cmap=None, xextent=None, pad_to=None, sides='default', scale_by_freq=None, hold=None, **kwargs)
Docstring:
    call signature::
    
      specgram(x, NFFT=256, Fs=2, Fc=0, detrend=mlab.detrend_none,
               window=mlab.window_hanning, noverlap=128,
               cmap=None, xextent=None, pad_to=None, sides='default',
               scale_by_freq=None, **kwargs)
    
    Compute a spectrogram of data in *x*.  Data are split into
    *NFFT* length segments and the PSD of each section is
    computed.  The windowing function *window* is applied to each
    segment, and the amount of overlap of each segment is
    specified with *noverlap*.
    
    Keyword arguments:
    
      *NFFT*: integer
          The number of data points used in each block for the FFT.
          Must be even; a power 2 is most efficient.  The default value is 256.
    
      *Fs*: scalar
          The sampling frequency (samples per time unit).  It is used
          to calculate the Fourier frequencies, freqs, in cycles per time
          unit. The default value is 2.
    
      *detrend*: callable
          The function applied to each segment before fft-ing,
          designed to remove the mean or linear trend.  Unlike in
          MATLAB, where the *detrend* parameter is a vector, in
          matplotlib is it a function.  The :mod:`~matplotlib.pylab`
          module defines :func:`~matplotlib.pylab.detrend_none`,
          :func:`~matplotlib.pylab.detrend_mean`, and
          :func:`~matplotlib.pylab.detrend_linear`, but you can use
          a custom function as well.
    
      *window*: callable or ndarray
          A function or a vector of length *NFFT*. To create window
          vectors see :func:`window_hanning`, :func:`window_none`,
          :func:`numpy.blackman`, :func:`numpy.hamming`,
          :func:`numpy.bartlett`, :func:`scipy.signal`,
          :func:`scipy.signal.get_window`, etc. The default is
          :func:`window_hanning`.  If a function is passed as the
          argument, it must take a data segment as an argument and
          return the windowed version of the segment.
    
      *noverlap*: integer
          The number of points of overlap between blocks.  The default value
          is 0 (no overlap).
    
      *pad_to*: integer
          The number of points to which the data segment is padded when
          performing the FFT.  This can be different from *NFFT*, which
          specifies the number of data points used.  While not increasing
          the actual resolution of the psd (the minimum distance between
          resolvable peaks), this can give more points in the plot,
          allowing for more detail. This corresponds to the *n* parameter
          in the call to fft(). The default is None, which sets *pad_to*
          equal to *NFFT*
    
      *sides*: [ 'default' | 'onesided' | 'twosided' ]
          Specifies which sides of the PSD to return.  Default gives the
          default behavior, which returns one-sided for real data and both
          for complex data.  'onesided' forces the return of a one-sided PSD,
          while 'twosided' forces two-sided.
    
      *scale_by_freq*: boolean
          Specifies whether the resulting density values should be scaled
          by the scaling frequency, which gives density in units of Hz^-1.
          This allows for integration over the returned frequency values.
          The default is True for MATLAB compatibility.
    
      *Fc*: integer
        The center frequency of *x* (defaults to 0), which offsets
        the y extents of the plot to reflect the frequency range used
        when a signal is acquired and then filtered and downsampled to
        baseband.
    
      *cmap*:
        A :class:`matplotlib.cm.Colormap` instance; if *None* use
        default determined by rc
    
      *xextent*:
        The image extent along the x-axis. xextent = (xmin,xmax)
        The default is (0,max(bins)), where bins is the return
        value from :func:`mlab.specgram`
    
      *kwargs*:
    
        Additional kwargs are passed on to imshow which makes the
        specgram image
    
      Return value is (*Pxx*, *freqs*, *bins*, *im*):
    
      - *bins* are the time points the spectrogram is calculated over
      - *freqs* is an array of frequencies
      - *Pxx* is a len(times) x len(freqs) array of power
      - *im* is a :class:`matplotlib.image.AxesImage` instance
    
    Note: If *x* is real (i.e. non-complex), only the positive
    spectrum is shown.  If *x* is complex, both positive and
    negative parts of the spectrum are shown.  This can be
    overridden using the *sides* keyword argument.
    
    **Example:**
    
    .. plot:: mpl_examples/pylab_examples/specgram_demo.py
    
    Additional kwargs: hold = [True|False] overrides default hold state


In [33]: specgram(saw2, Fs=fs)
Out[33]: 
(array([[  6.00134067e+03,   5.92682925e+02,   8.28182507e+02, ...,
          7.31593636e+03,   1.11713246e+03,   3.88078527e+02],
       [  3.35545496e+03,   6.19333362e+02,   7.38467447e+02, ...,
          4.25172563e+03,   8.84640906e+02,   5.15828474e+02],
       [  1.67025950e+01,   1.66837243e+01,   1.66845460e+01, ...,
          2.67167536e+01,   1.66855541e+01,   1.66830104e+01],
       ..., 
       [  2.60549450e-12,   2.94059099e-13,   3.94701827e-13, ...,
          9.82038985e-03,   5.18187022e-13,   2.06619688e-13],
       [  6.73639550e-13,   9.62158410e-14,   1.21357577e-13, ...,
          9.81604961e-03,   1.52205627e-13,   7.43724500e-14],
       [  1.52593318e-14,   1.52593309e-14,   1.52593309e-14, ...,
          4.90730535e-03,   1.52593309e-14,   1.52593309e-14]]),
 array([  0.00000000e+00,   3.90625000e-05,   7.81250000e-05,
         1.17187500e-04,   1.56250000e-04,   1.95312500e-04,
         2.34375000e-04,   2.73437500e-04,   3.12500000e-04,
         3.51562500e-04,   3.90625000e-04,   4.29687500e-04,
         4.68750000e-04,   5.07812500e-04,   5.46875000e-04,
         5.85937500e-04,   6.25000000e-04,   6.64062500e-04,
         7.03125000e-04,   7.42187500e-04,   7.81250000e-04,
         8.20312500e-04,   8.59375000e-04,   8.98437500e-04,
         9.37500000e-04,   9.76562500e-04,   1.01562500e-03,
         1.05468750e-03,   1.09375000e-03,   1.13281250e-03,
         1.17187500e-03,   1.21093750e-03,   1.25000000e-03,
         1.28906250e-03,   1.32812500e-03,   1.36718750e-03,
         1.40625000e-03,   1.44531250e-03,   1.48437500e-03,
         1.52343750e-03,   1.56250000e-03,   1.60156250e-03,
         1.64062500e-03,   1.67968750e-03,   1.71875000e-03,
         1.75781250e-03,   1.79687500e-03,   1.83593750e-03,
         1.87500000e-03,   1.91406250e-03,   1.95312500e-03,
         1.99218750e-03,   2.03125000e-03,   2.07031250e-03,
         2.10937500e-03,   2.14843750e-03,   2.18750000e-03,
         2.22656250e-03,   2.26562500e-03,   2.30468750e-03,
         2.34375000e-03,   2.38281250e-03,   2.42187500e-03,
         2.46093750e-03,   2.50000000e-03,   2.53906250e-03,
         2.57812500e-03,   2.61718750e-03,   2.65625000e-03,
         2.69531250e-03,   2.73437500e-03,   2.77343750e-03,
         2.81250000e-03,   2.85156250e-03,   2.89062500e-03,
         2.92968750e-03,   2.96875000e-03,   3.00781250e-03,
         3.04687500e-03,   3.08593750e-03,   3.12500000e-03,
         3.16406250e-03,   3.20312500e-03,   3.24218750e-03,
         3.28125000e-03,   3.32031250e-03,   3.35937500e-03,
         3.39843750e-03,   3.43750000e-03,   3.47656250e-03,
         3.51562500e-03,   3.55468750e-03,   3.59375000e-03,
         3.63281250e-03,   3.67187500e-03,   3.71093750e-03,
         3.75000000e-03,   3.78906250e-03,   3.82812500e-03,
         3.86718750e-03,   3.90625000e-03,   3.94531250e-03,
         3.98437500e-03,   4.02343750e-03,   4.06250000e-03,
         4.10156250e-03,   4.14062500e-03,   4.17968750e-03,
         4.21875000e-03,   4.25781250e-03,   4.29687500e-03,
         4.33593750e-03,   4.37500000e-03,   4.41406250e-03,
         4.45312500e-03,   4.49218750e-03,   4.53125000e-03,
         4.57031250e-03,   4.60937500e-03,   4.64843750e-03,
         4.68750000e-03,   4.72656250e-03,   4.76562500e-03,
         4.80468750e-03,   4.84375000e-03,   4.88281250e-03,
         4.92187500e-03,   4.96093750e-03,   5.00000000e-03]),
 array([   12800.,    25600.,    38400.,    51200.,    64000.,    76800.,
          89600.,   102400.,   115200.,   128000.,   140800.,   153600.,
         166400.,   179200.,   192000.,   204800.,   217600.,   230400.,
         243200.,   256000.,   268800.,   281600.,   294400.,   307200.,
         320000.,   332800.,   345600.,   358400.,   371200.,   384000.,
         396800.,   409600.,   422400.,   435200.,   448000.,   460800.,
         473600.,   486400.,   499200.,   512000.,   524800.,   537600.,
         550400.,   563200.,   576000.,   588800.,   601600.,   614400.,
         627200.,   640000.,   652800.,   665600.,   678400.,   691200.,
         704000.,   716800.,   729600.,   742400.,   755200.,   768000.,
         780800.,   793600.,   806400.,   819200.,   832000.,   844800.,
         857600.,   870400.,   883200.,   896000.,   908800.,   921600.,
         934400.,   947200.,   960000.,   972800.,   985600.,   998400.,
        1011200.,  1024000.,  1036800.,  1049600.,  1062400.,  1075200.,
        1088000.,  1100800.,  1113600.,  1126400.,  1139200.,  1152000.,
        1164800.,  1177600.,  1190400.,  1203200.,  1216000.,  1228800.,
        1241600.,  1254400.,  1267200.,  1280000.,  1292800.,  1305600.,
        1318400.,  1331200.,  1344000.,  1356800.,  1369600.,  1382400.,
        1395200.,  1408000.,  1420800.,  1433600.,  1446400.,  1459200.,
        1472000.,  1484800.,  1497600.,  1510400.,  1523200.,  1536000.,
        1548800.,  1561600.,  1574400.,  1587200.,  1600000.,  1612800.,
        1625600.,  1638400.,  1651200.,  1664000.,  1676800.,  1689600.,
        1702400.,  1715200.,  1728000.,  1740800.,  1753600.,  1766400.,
        1779200.,  1792000.,  1804800.,  1817600.,  1830400.,  1843200.,
        1856000.,  1868800.,  1881600.,  1894400.,  1907200.,  1920000.,
        1932800.,  1945600.,  1958400.,  1971200.,  1984000.]),
 <matplotlib.image.AxesImage object at 0x3865e90>)

In [34]: import stockwell

In [35]: stsaw2 = stockwell.st(saw2)

In [37]: import stockwell.plots

In [38]: figure(); stockwell.plots(abs(stsaw2), fs=100)
Out[40]: <matplotlib.figure.Figure object at 0x3684f10>
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)

/media/d7e7e26e-bb28-4128-9098-0043ef93dd4e/home/clee/code/eegquant/sigproc/<ipython console> in <module>()

TypeError: 'module' object is not callable

In [41]: stockwell.plots.plotspec(abs(stsaw2), fs=100)
Out[41]: <matplotlib.image.AxesImage object at 0x4244350>

In [42]: t2.max()
Out[42]: 199.99000000000001

In [43]: t2[:10]
Out[43]: array([ 0.  ,  0.01,  0.02,  0.03,  0.04,  0.05,  0.06,  0.07,  0.08,  0.09])

In [44]: ls

In [45]: reload(filters)
Out[45]: <module 'filters' from 'filters.py'>

In [46]: reload(filters)
Out[46]: <module 'filters' from 'filters.py'>

In [47]: bpf = filters.PassBand(fs=100.0, passfreqs=[4.0, 7.0], stopfreqs=[2.0, 9.0])
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)

/media/d7e7e26e-bb28-4128-9098-0043ef93dd4e/home/clee/code/eegquant/sigproc/<ipython console> in <module>()

/media/d7e7e26e-bb28-4128-9098-0043ef93dd4e/home/clee/code/eegquant/sigproc/filters.py in __init__(self, fs, passfreqs, stopfreqs, gstop, gpass, order, ftype, window)
    155             ws = [ff/nyquist for ff in stopfreqs]
    156             
--> 157         self.ba = signal.iirdesign(wp=wp, ws=ws, gstop=gstop, gpass=gpass, ftype=ftype)
    158 
    159     def lfilter(self, x):

/usr/lib/python2.6/dist-packages/scipy/signal/filter_design.pyc in iirdesign(wp, ws, gpass, gstop, analog, ftype, output)
    410         raise ValueError, "Invalid IIR filter type."
    411     except IndexError:
--> 412         raise ValueError, "%s does not have order selection use iirfilter function." % ftype
    413 
    414     wp = atleast_1d(wp)

ValueError: bessel does not have order selection use iirfilter function.

In [51]: reload(filters)
Out[51]: <module 'filters' from 'filters.py'>

In [52]: bpf = filters.PassBand(fs=100.0, passfreqs=[4.0, 7.0], stopfreqs=[2.0, 9.0])

In [53]: thetasaw2 = bpf.filtfilt(saw2)

In [54]: plot(t,thetasaw2)
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)

/media/d7e7e26e-bb28-4128-9098-0043ef93dd4e/home/clee/code/eegquant/sigproc/<ipython console> in <module>()

/usr/local/lib/python2.6/dist-packages/matplotlib/pyplot.pyc in plot(*args, **kwargs)
   2284         ax.hold(hold)
   2285     try:
-> 2286         ret = ax.plot(*args, **kwargs)
   2287         draw_if_interactive()
   2288     finally:

/usr/local/lib/python2.6/dist-packages/matplotlib/axes.pyc in plot(self, *args, **kwargs)
   3781         lines = []
   3782 
-> 3783         for line in self._get_lines(*args, **kwargs):
   3784             self.add_line(line)
   3785             lines.append(line)

/usr/local/lib/python2.6/dist-packages/matplotlib/axes.pyc in _grab_next_args(self, *args, **kwargs)
    315                 return
    316             if len(remaining) <= 3:
--> 317                 for seg in self._plot_args(remaining, kwargs):
    318                     yield seg
    319                 return

/usr/local/lib/python2.6/dist-packages/matplotlib/axes.pyc in _plot_args(self, tup, kwargs)
    292             x = np.arange(y.shape[0], dtype=float)
    293 
--> 294         x, y = self._xy_from_xy(x, y)
    295 
    296         if self.command == 'plot':

/usr/local/lib/python2.6/dist-packages/matplotlib/axes.pyc in _xy_from_xy(self, x, y)
    232         y = np.atleast_1d(y)
    233         if x.shape[0] != y.shape[0]:
--> 234             raise ValueError("x and y must have same first dimension")
    235         if x.ndim > 2 or y.ndim > 2:
    236             raise ValueError("x and y can be no greater than 2-D")

ValueError: x and y must have same first dimension

In [55]: t.shape
Out[56]: (10000,)

In [57]: t[:10]
Out[57]: 
array([ 0.   ,  0.001,  0.002,  0.003,  0.004,  0.005,  0.006,  0.007,
        0.008,  0.009])

In [58]: plot(thetasaw2)
Out[61]: [<matplotlib.lines.Line2D object at 0x43572d0>]

In [62]: figure()
Out[62]: <matplotlib.figure.Figure object at 0x3697590>

In [63]: plot(thetasaw2)
Out[63]: [<matplotlib.lines.Line2D object at 0x40fea10>]

In [64]: plot(3*thetasaw2,hold=False)
Out[64]: [<matplotlib.lines.Line2D object at 0x437d390>]

In [65]: plot(saw2)
Out[65]: [<matplotlib.lines.Line2D object at 0x40f4850>]

In [66]: bpfgamma = filters.PassBand(fs=100.0, passfreqs=[30.0, 40.0], stopfreqs=[20.0, 45.0])

In [67]: gammasaw2 = bpfgamma.filtfilt(saw2)

In [69]: 
In [71]: plot(gammasaw2)
Out[72]: [<matplotlib.lines.Line2D object at 0x4112c10>]

In [73]: figure()
Out[73]: <matplotlib.figure.Figure object at 0x4377cd0>

In [74]: psd
Out[77]: <function psd at 0x277ac08>

In [78]: psd?
Type:		function
Base Class:	<type 'function'>
String Form:	<function psd at 0x277ac08>
Namespace:	Interactive
File:		/usr/local/lib/python2.6/dist-packages/matplotlib/pyplot.py
Definition:	psd(x, NFFT=256, Fs=2, Fc=0, detrend=<function detrend_none at 0x2135c80>, window=<function window_hanning at 0x212fed8>, noverlap=0, pad_to=None, sides='default', scale_by_freq=None, hold=None, **kwargs)
Docstring:
    call signature::
    
      psd(x, NFFT=256, Fs=2, Fc=0, detrend=mlab.detrend_none,
          window=mlab.window_hanning, noverlap=0, pad_to=None,
          sides='default', scale_by_freq=None, **kwargs)
    
    The power spectral density by Welch's average periodogram
    method.  The vector *x* is divided into *NFFT* length
    segments.  Each segment is detrended by function *detrend* and
    windowed by function *window*.  *noverlap* gives the length of
    the overlap between segments.  The :math:`|\mathrm{fft}(i)|^2`
    of each segment :math:`i` are averaged to compute *Pxx*, with a
    scaling to correct for power loss due to windowing.  *Fs* is the
    sampling frequency.
    
    Keyword arguments:
    
      *NFFT*: integer
          The number of data points used in each block for the FFT.
          Must be even; a power 2 is most efficient.  The default value is 256.
    
      *Fs*: scalar
          The sampling frequency (samples per time unit).  It is used
          to calculate the Fourier frequencies, freqs, in cycles per time
          unit. The default value is 2.
    
      *detrend*: callable
          The function applied to each segment before fft-ing,
          designed to remove the mean or linear trend.  Unlike in
          MATLAB, where the *detrend* parameter is a vector, in
          matplotlib is it a function.  The :mod:`~matplotlib.pylab`
          module defines :func:`~matplotlib.pylab.detrend_none`,
          :func:`~matplotlib.pylab.detrend_mean`, and
          :func:`~matplotlib.pylab.detrend_linear`, but you can use
          a custom function as well.
    
      *window*: callable or ndarray
          A function or a vector of length *NFFT*. To create window
          vectors see :func:`window_hanning`, :func:`window_none`,
          :func:`numpy.blackman`, :func:`numpy.hamming`,
          :func:`numpy.bartlett`, :func:`scipy.signal`,
          :func:`scipy.signal.get_window`, etc. The default is
          :func:`window_hanning`.  If a function is passed as the
          argument, it must take a data segment as an argument and
          return the windowed version of the segment.
    
      *noverlap*: integer
          The number of points of overlap between blocks.  The default value
          is 0 (no overlap).
    
      *pad_to*: integer
          The number of points to which the data segment is padded when
          performing the FFT.  This can be different from *NFFT*, which
          specifies the number of data points used.  While not increasing
          the actual resolution of the psd (the minimum distance between
          resolvable peaks), this can give more points in the plot,
          allowing for more detail. This corresponds to the *n* parameter
          in the call to fft(). The default is None, which sets *pad_to*
          equal to *NFFT*
    
      *sides*: [ 'default' | 'onesided' | 'twosided' ]
          Specifies which sides of the PSD to return.  Default gives the
          default behavior, which returns one-sided for real data and both
          for complex data.  'onesided' forces the return of a one-sided PSD,
          while 'twosided' forces two-sided.
    
      *scale_by_freq*: boolean
          Specifies whether the resulting density values should be scaled
          by the scaling frequency, which gives density in units of Hz^-1.
          This allows for integration over the returned frequency values.
          The default is True for MATLAB compatibility.
    
      *Fc*: integer
        The center frequency of *x* (defaults to 0), which offsets
        the x extents of the plot to reflect the frequency range used
        when a signal is acquired and then filtered and downsampled to
        baseband.
    
    Returns the tuple (*Pxx*, *freqs*).
    
    For plotting, the power is plotted as
    :math:`10\log_{10}(P_{xx})` for decibels, though *Pxx* itself
    is returned.
    
    References:
      Bendat & Piersol -- Random Data: Analysis and Measurement
      Procedures, John Wiley & Sons (1986)
    
    kwargs control the :class:`~matplotlib.lines.Line2D` properties:
    
      agg_filter: unknown
      alpha: float (0.0 transparent through 1.0 opaque)         
      animated: [True | False]         
      antialiased or aa: [True | False]         
      axes: an :class:`~matplotlib.axes.Axes` instance         
      clip_box: a :class:`matplotlib.transforms.Bbox` instance         
      clip_on: [True | False]         
      clip_path: [ (:class:`~matplotlib.path.Path`,         :class:`~matplotlib.transforms.Transform`) |         :class:`~matplotlib.patches.Patch` | None ]         
      color or c: any matplotlib color         
      contains: a callable function         
      dash_capstyle: ['butt' | 'round' | 'projecting']         
      dash_joinstyle: ['miter' | 'round' | 'bevel']         
      dashes: sequence of on/off ink in points         
      data: 2D array (rows are x, y) or two 1D arrays         
      drawstyle: [ 'default' | 'steps' | 'steps-pre' | 'steps-mid' | 'steps-post' ]         
      figure: a :class:`matplotlib.figure.Figure` instance         
      fillstyle: ['full' | 'left' | 'right' | 'bottom' | 'top']         
      gid: an id string         
      label: any string         
      linestyle or ls: [ ``'-'`` | ``'--'`` | ``'-.'`` | ``':'`` | ``'None'`` | ``' '`` | ``''`` ]         and any drawstyle in combination with a linestyle, e.g. ``'steps--'``.         
      linewidth or lw: float value in points         
      lod: [True | False]         
      marker: [ ``'+'`` | ``'*'`` | ``','`` | ``'.'``                  | ``'1'`` | ``'2'`` | ``'3'`` | ``'4'``                  | ``'<'`` | ``'>'`` | ``'D'`` | ``'H'``                  | ``'^'`` | ``'_'`` | ``'d'`` | ``'h'``                  | ``'o'`` | ``'p'`` | ``'s'`` | ``'v'``                  | ``'x'`` | ``'|'``                  | TICKUP | TICKDOWN | TICKLEFT | TICKRIGHT                  | CARETUP | CARETDOWN | CARETLEFT | CARETRIGHT                  | ``'None'`` | ``' '`` | ``''`` | '$...$']
      markeredgecolor or mec: any matplotlib color         
      markeredgewidth or mew: float value in points         
      markerfacecolor or mfc: any matplotlib color         
      markerfacecoloralt or mfcalt: any matplotlib color         
      markersize or ms: float         
      markevery: None | integer | (startind, stride)
      picker: float distance in points or callable pick function         ``fn(artist, event)``         
      pickradius: float distance in points         
      rasterized: [True | False | None]         
      snap: unknown
      solid_capstyle: ['butt' | 'round' |  'projecting']         
      solid_joinstyle: ['miter' | 'round' | 'bevel']         
      transform: a :class:`matplotlib.transforms.Transform` instance         
      url: a url string         
      visible: [True | False]         
      xdata: 1D array         
      ydata: 1D array         
      zorder: any number         
    
    **Example:**
    
    .. plot:: mpl_examples/pylab_examples/psd_demo.py
    
    Additional kwargs: hold = [True|False] overrides default hold state


In [79]: psd(saw2)
Out[79]: 
(array([  1.60544207e+01,   1.83019419e+01,   3.66064949e+00,
         1.29291215e+00,   6.77979402e-01,   4.23302308e-01,
         2.90201727e-01,   2.11472292e-01,   1.61333030e-01,
         1.27030851e-01,   1.02429386e-01,   8.54414998e-02,
         7.11189841e-02,   6.07600040e-02,   5.24430944e-02,
         4.57055396e-02,   4.02128843e-02,   3.56696204e-02,
         3.18555785e-02,   2.86372315e-02,   2.58858817e-02,
         2.35047925e-02,   2.15089959e-02,   1.96781515e-02,
         1.81225738e-02,   1.67433516e-02,   1.55167186e-02,
         1.44254924e-02,   1.34507142e-02,   1.25734066e-02,
         1.17835418e-02,   1.10686850e-02,   1.04170091e-02,
         9.83621755e-03,   9.28941519e-03,   8.79832956e-03,
         8.34658636e-03,   7.93025583e-03,   7.54673928e-03,
         7.19298130e-03,   6.86499461e-03,   6.56105170e-03,
         6.27872050e-03,   6.01506146e-03,   5.77284848e-03,
         5.54206231e-03,   5.32888850e-03,   5.12904106e-03,
         4.94141911e-03,   4.76536151e-03,   4.60011062e-03,
         4.44441574e-03,   4.29780196e-03,   4.15960626e-03,
         4.02879848e-03,   3.90646353e-03,   3.78915600e-03,
         3.67898276e-03,   3.57453981e-03,   3.47540799e-03,
         3.38135931e-03,   3.29214567e-03,   3.20728537e-03,
         3.12659486e-03,   3.04985536e-03,   2.97663346e-03,
         2.90737712e-03,   2.84074479e-03,   2.77751116e-03,
         2.71716328e-03,   2.65950525e-03,   2.60444325e-03,
         2.55187517e-03,   2.50159452e-03,   2.45351069e-03,
         2.40754041e-03,   2.36348331e-03,   2.32152469e-03,
         2.28111085e-03,   2.24252511e-03,   2.20557415e-03,
         2.17015269e-03,   2.13621827e-03,   2.10372002e-03,
         2.07256480e-03,   2.04270118e-03,   2.01409237e-03,
         1.98664235e-03,   1.96042261e-03,   1.93520291e-03,
         1.91107556e-03,   1.88797089e-03,   1.86582782e-03,
         1.84462593e-03,   1.82433683e-03,   1.80491774e-03,
         1.78633830e-03,   1.76857937e-03,   1.75159552e-03,
         1.73540911e-03,   1.71992871e-03,   1.70517418e-03,
         1.69112397e-03,   1.67774285e-03,   1.66502006e-03,
         1.65293999e-03,   1.64148312e-03,   1.63063253e-03,
         1.62037725e-03,   1.61069737e-03,   1.60159599e-03,
         1.59304139e-03,   1.58503067e-03,   1.57755920e-03,
         1.57060960e-03,   1.56417556e-03,   1.55825032e-03,
         1.55282568e-03,   1.54789427e-03,   1.54345068e-03,
         1.53948822e-03,   1.53600518e-03,   1.53299442e-03,
         1.53045175e-03,   1.52837679e-03,   1.52676543e-03,
         1.52561541e-03,   1.52492612e-03,   7.62348223e-04]),
 array([ 0.       ,  0.0078125,  0.015625 ,  0.0234375,  0.03125  ,
        0.0390625,  0.046875 ,  0.0546875,  0.0625   ,  0.0703125,
        0.078125 ,  0.0859375,  0.09375  ,  0.1015625,  0.109375 ,
        0.1171875,  0.125    ,  0.1328125,  0.140625 ,  0.1484375,
        0.15625  ,  0.1640625,  0.171875 ,  0.1796875,  0.1875   ,
        0.1953125,  0.203125 ,  0.2109375,  0.21875  ,  0.2265625,
        0.234375 ,  0.2421875,  0.25     ,  0.2578125,  0.265625 ,
        0.2734375,  0.28125  ,  0.2890625,  0.296875 ,  0.3046875,
        0.3125   ,  0.3203125,  0.328125 ,  0.3359375,  0.34375  ,
        0.3515625,  0.359375 ,  0.3671875,  0.375    ,  0.3828125,
        0.390625 ,  0.3984375,  0.40625  ,  0.4140625,  0.421875 ,
        0.4296875,  0.4375   ,  0.4453125,  0.453125 ,  0.4609375,
        0.46875  ,  0.4765625,  0.484375 ,  0.4921875,  0.5      ,
        0.5078125,  0.515625 ,  0.5234375,  0.53125  ,  0.5390625,
        0.546875 ,  0.5546875,  0.5625   ,  0.5703125,  0.578125 ,
        0.5859375,  0.59375  ,  0.6015625,  0.609375 ,  0.6171875,
        0.625    ,  0.6328125,  0.640625 ,  0.6484375,  0.65625  ,
        0.6640625,  0.671875 ,  0.6796875,  0.6875   ,  0.6953125,
        0.703125 ,  0.7109375,  0.71875  ,  0.7265625,  0.734375 ,
        0.7421875,  0.75     ,  0.7578125,  0.765625 ,  0.7734375,
        0.78125  ,  0.7890625,  0.796875 ,  0.8046875,  0.8125   ,
        0.8203125,  0.828125 ,  0.8359375,  0.84375  ,  0.8515625,
        0.859375 ,  0.8671875,  0.875    ,  0.8828125,  0.890625 ,
        0.8984375,  0.90625  ,  0.9140625,  0.921875 ,  0.9296875,
        0.9375   ,  0.9453125,  0.953125 ,  0.9609375,  0.96875  ,
        0.9765625,  0.984375 ,  0.9921875,  1.       ]))

In [80]: psd(saw2, Fs=fs)
Out[80]: 
(array([  3.21088414e+03,   3.66038838e+03,   7.32129897e+02,
         2.58582431e+02,   1.35595880e+02,   8.46604617e+01,
         5.80403455e+01,   4.22944584e+01,   3.22666061e+01,
         2.54061702e+01,   2.04858772e+01,   1.70883000e+01,
         1.42237968e+01,   1.21520008e+01,   1.04886189e+01,
         9.14110791e+00,   8.04257687e+00,   7.13392408e+00,
         6.37111569e+00,   5.72744631e+00,   5.17717634e+00,
         4.70095851e+00,   4.30179918e+00,   3.93563030e+00,
         3.62451477e+00,   3.34867031e+00,   3.10334372e+00,
         2.88509847e+00,   2.69014283e+00,   2.51468133e+00,
         2.35670835e+00,   2.21373700e+00,   2.08340181e+00,
         1.96724351e+00,   1.85788304e+00,   1.75966591e+00,
         1.66931727e+00,   1.58605117e+00,   1.50934786e+00,
         1.43859626e+00,   1.37299892e+00,   1.31221034e+00,
         1.25574410e+00,   1.20301229e+00,   1.15456970e+00,
         1.10841246e+00,   1.06577770e+00,   1.02580821e+00,
         9.88283822e-01,   9.53072303e-01,   9.20022123e-01,
         8.88883147e-01,   8.59560393e-01,   8.31921253e-01,
         8.05759697e-01,   7.81292706e-01,   7.57831201e-01,
         7.35796551e-01,   7.14907962e-01,   6.95081597e-01,
         6.76271863e-01,   6.58429135e-01,   6.41457074e-01,
         6.25318973e-01,   6.09971072e-01,   5.95326693e-01,
         5.81475424e-01,   5.68148958e-01,   5.55502232e-01,
         5.43432656e-01,   5.31901050e-01,   5.20888651e-01,
         5.10375033e-01,   5.00318903e-01,   4.90702138e-01,
         4.81508082e-01,   4.72696662e-01,   4.64304938e-01,
         4.56222171e-01,   4.48505023e-01,   4.41114831e-01,
         4.34030537e-01,   4.27243655e-01,   4.20744005e-01,
         4.14512961e-01,   4.08540237e-01,   4.02818474e-01,
         3.97328469e-01,   3.92084523e-01,   3.87040582e-01,
         3.82215111e-01,   3.77594179e-01,   3.73165565e-01,
         3.68925187e-01,   3.64867367e-01,   3.60983549e-01,
         3.57267660e-01,   3.53715873e-01,   3.50319104e-01,
         3.47081822e-01,   3.43985741e-01,   3.41034835e-01,
         3.38224794e-01,   3.35548570e-01,   3.33004012e-01,
         3.30587999e-01,   3.28296623e-01,   3.26126506e-01,
         3.24075450e-01,   3.22139474e-01,   3.20319198e-01,
         3.18608279e-01,   3.17006134e-01,   3.15511840e-01,
         3.14121920e-01,   3.12835111e-01,   3.11650063e-01,
         3.10565136e-01,   3.09578855e-01,   3.08690135e-01,
         3.07897644e-01,   3.07201035e-01,   3.06598884e-01,
         3.06090350e-01,   3.05675357e-01,   3.05353085e-01,
         3.05123081e-01,   3.04985224e-01,   1.52469645e-01]),
 array([  0.00000000e+00,   3.90625000e-05,   7.81250000e-05,
         1.17187500e-04,   1.56250000e-04,   1.95312500e-04,
         2.34375000e-04,   2.73437500e-04,   3.12500000e-04,
         3.51562500e-04,   3.90625000e-04,   4.29687500e-04,
         4.68750000e-04,   5.07812500e-04,   5.46875000e-04,
         5.85937500e-04,   6.25000000e-04,   6.64062500e-04,
         7.03125000e-04,   7.42187500e-04,   7.81250000e-04,
         8.20312500e-04,   8.59375000e-04,   8.98437500e-04,
         9.37500000e-04,   9.76562500e-04,   1.01562500e-03,
         1.05468750e-03,   1.09375000e-03,   1.13281250e-03,
         1.17187500e-03,   1.21093750e-03,   1.25000000e-03,
         1.28906250e-03,   1.32812500e-03,   1.36718750e-03,
         1.40625000e-03,   1.44531250e-03,   1.48437500e-03,
         1.52343750e-03,   1.56250000e-03,   1.60156250e-03,
         1.64062500e-03,   1.67968750e-03,   1.71875000e-03,
         1.75781250e-03,   1.79687500e-03,   1.83593750e-03,
         1.87500000e-03,   1.91406250e-03,   1.95312500e-03,
         1.99218750e-03,   2.03125000e-03,   2.07031250e-03,
         2.10937500e-03,   2.14843750e-03,   2.18750000e-03,
         2.22656250e-03,   2.26562500e-03,   2.30468750e-03,
         2.34375000e-03,   2.38281250e-03,   2.42187500e-03,
         2.46093750e-03,   2.50000000e-03,   2.53906250e-03,
         2.57812500e-03,   2.61718750e-03,   2.65625000e-03,
         2.69531250e-03,   2.73437500e-03,   2.77343750e-03,
         2.81250000e-03,   2.85156250e-03,   2.89062500e-03,
         2.92968750e-03,   2.96875000e-03,   3.00781250e-03,
         3.04687500e-03,   3.08593750e-03,   3.12500000e-03,
         3.16406250e-03,   3.20312500e-03,   3.24218750e-03,
         3.28125000e-03,   3.32031250e-03,   3.35937500e-03,
         3.39843750e-03,   3.43750000e-03,   3.47656250e-03,
         3.51562500e-03,   3.55468750e-03,   3.59375000e-03,
         3.63281250e-03,   3.67187500e-03,   3.71093750e-03,
         3.75000000e-03,   3.78906250e-03,   3.82812500e-03,
         3.86718750e-03,   3.90625000e-03,   3.94531250e-03,
         3.98437500e-03,   4.02343750e-03,   4.06250000e-03,
         4.10156250e-03,   4.14062500e-03,   4.17968750e-03,
         4.21875000e-03,   4.25781250e-03,   4.29687500e-03,
         4.33593750e-03,   4.37500000e-03,   4.41406250e-03,
         4.45312500e-03,   4.49218750e-03,   4.53125000e-03,
         4.57031250e-03,   4.60937500e-03,   4.64843750e-03,
         4.68750000e-03,   4.72656250e-03,   4.76562500e-03,
         4.80468750e-03,   4.84375000e-03,   4.88281250e-03,
         4.92187500e-03,   4.96093750e-03,   5.00000000e-03]))

In [81]: fs
Out[81]: 0.01

In [82]: fs = 100

In [83]: psd(saw2, Fs=fs)
Out[83]: 
(array([  3.21088414e-01,   3.66038838e-01,   7.32129897e-02,
         2.58582431e-02,   1.35595880e-02,   8.46604617e-03,
         5.80403455e-03,   4.22944584e-03,   3.22666061e-03,
         2.54061702e-03,   2.04858772e-03,   1.70883000e-03,
         1.42237968e-03,   1.21520008e-03,   1.04886189e-03,
         9.14110791e-04,   8.04257687e-04,   7.13392408e-04,
         6.37111569e-04,   5.72744631e-04,   5.17717634e-04,
         4.70095851e-04,   4.30179918e-04,   3.93563030e-04,
         3.62451477e-04,   3.34867031e-04,   3.10334372e-04,
         2.88509847e-04,   2.69014283e-04,   2.51468133e-04,
         2.35670835e-04,   2.21373700e-04,   2.08340181e-04,
         1.96724351e-04,   1.85788304e-04,   1.75966591e-04,
         1.66931727e-04,   1.58605117e-04,   1.50934786e-04,
         1.43859626e-04,   1.37299892e-04,   1.31221034e-04,
         1.25574410e-04,   1.20301229e-04,   1.15456970e-04,
         1.10841246e-04,   1.06577770e-04,   1.02580821e-04,
         9.88283822e-05,   9.53072303e-05,   9.20022123e-05,
         8.88883147e-05,   8.59560393e-05,   8.31921253e-05,
         8.05759697e-05,   7.81292706e-05,   7.57831201e-05,
         7.35796551e-05,   7.14907962e-05,   6.95081597e-05,
         6.76271863e-05,   6.58429135e-05,   6.41457074e-05,
         6.25318973e-05,   6.09971072e-05,   5.95326693e-05,
         5.81475424e-05,   5.68148958e-05,   5.55502232e-05,
         5.43432656e-05,   5.31901050e-05,   5.20888651e-05,
         5.10375033e-05,   5.00318903e-05,   4.90702138e-05,
         4.81508082e-05,   4.72696662e-05,   4.64304938e-05,
         4.56222171e-05,   4.48505023e-05,   4.41114831e-05,
         4.34030537e-05,   4.27243655e-05,   4.20744005e-05,
         4.14512961e-05,   4.08540237e-05,   4.02818474e-05,
         3.97328469e-05,   3.92084523e-05,   3.87040582e-05,
         3.82215111e-05,   3.77594179e-05,   3.73165565e-05,
         3.68925187e-05,   3.64867367e-05,   3.60983549e-05,
         3.57267660e-05,   3.53715873e-05,   3.50319104e-05,
         3.47081822e-05,   3.43985741e-05,   3.41034835e-05,
         3.38224794e-05,   3.35548570e-05,   3.33004012e-05,
         3.30587999e-05,   3.28296623e-05,   3.26126506e-05,
         3.24075450e-05,   3.22139474e-05,   3.20319198e-05,
         3.18608279e-05,   3.17006134e-05,   3.15511840e-05,
         3.14121920e-05,   3.12835111e-05,   3.11650063e-05,
         3.10565136e-05,   3.09578855e-05,   3.08690135e-05,
         3.07897644e-05,   3.07201035e-05,   3.06598884e-05,
         3.06090350e-05,   3.05675357e-05,   3.05353085e-05,
         3.05123081e-05,   3.04985224e-05,   1.52469645e-05]),
 array([  0.      ,   0.390625,   0.78125 ,   1.171875,   1.5625  ,
         1.953125,   2.34375 ,   2.734375,   3.125   ,   3.515625,
         3.90625 ,   4.296875,   4.6875  ,   5.078125,   5.46875 ,
         5.859375,   6.25    ,   6.640625,   7.03125 ,   7.421875,
         7.8125  ,   8.203125,   8.59375 ,   8.984375,   9.375   ,
         9.765625,  10.15625 ,  10.546875,  10.9375  ,  11.328125,
        11.71875 ,  12.109375,  12.5     ,  12.890625,  13.28125 ,
        13.671875,  14.0625  ,  14.453125,  14.84375 ,  15.234375,
        15.625   ,  16.015625,  16.40625 ,  16.796875,  17.1875  ,
        17.578125,  17.96875 ,  18.359375,  18.75    ,  19.140625,
        19.53125 ,  19.921875,  20.3125  ,  20.703125,  21.09375 ,
        21.484375,  21.875   ,  22.265625,  22.65625 ,  23.046875,
        23.4375  ,  23.828125,  24.21875 ,  24.609375,  25.      ,
        25.390625,  25.78125 ,  26.171875,  26.5625  ,  26.953125,
        27.34375 ,  27.734375,  28.125   ,  28.515625,  28.90625 ,
        29.296875,  29.6875  ,  30.078125,  30.46875 ,  30.859375,
        31.25    ,  31.640625,  32.03125 ,  32.421875,  32.8125  ,
        33.203125,  33.59375 ,  33.984375,  34.375   ,  34.765625,
        35.15625 ,  35.546875,  35.9375  ,  36.328125,  36.71875 ,
        37.109375,  37.5     ,  37.890625,  38.28125 ,  38.671875,
        39.0625  ,  39.453125,  39.84375 ,  40.234375,  40.625   ,
        41.015625,  41.40625 ,  41.796875,  42.1875  ,  42.578125,
        42.96875 ,  43.359375,  43.75    ,  44.140625,  44.53125 ,
        44.921875,  45.3125  ,  45.703125,  46.09375 ,  46.484375,
        46.875   ,  47.265625,  47.65625 ,  48.046875,  48.4375  ,
        48.828125,  49.21875 ,  49.609375,  50.      ]))

In [84]: signal.hilbert?
Type:		function
Base Class:	<type 'function'>
String Form:	<function hilbert at 0x2c46758>
Namespace:	Interactive
File:		/usr/lib/python2.6/dist-packages/scipy/signal/signaltools.py
Definition:	signal.hilbert(x, N=None)
Docstring:
    Compute the analytic signal.
    
    The transformation is done along the first axis.
    
    Parameters
    ----------
    x : array-like
        Signal data
    N : int, optional
        Number of Fourier components. Default: ``x.shape[0]``
    
    Returns
    -------
    xa : ndarray, shape (N,) + x.shape[1:]
        Analytic signal of `x`
    
    Notes
    -----
    The analytic signal `x_a(t)` of `x(t)` is::
    
        x_a = F^{-1}(F(x) 2U) = x + i y
    
    where ``F`` is the Fourier transform, ``U`` the unit step function,
    and ``y`` the Hilbert transform of ``x``. [1]
    
    References
    ----------
    .. [1] Wikipedia, "Analytic signal".
           http://en.wikipedia.org/wiki/Analytic_signal


In [86]: hilthetasaw2 = signal.hilbert(thetasaw2)

In [90]: hilthetasaw2[0]
Out[91]: (0.0016560446902480479-0.001839644388550299j)

In [92]: rehil = real(hiltheatasaw2)
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)

/media/d7e7e26e-bb28-4128-9098-0043ef93dd4e/home/clee/code/eegquant/sigproc/<ipython console> in <module>()

NameError: name 'hiltheatasaw2' is not defined

In [93]: rehil = real(hilthetasaw2)

In [96]: imhil = imag(hilthetasaw2)

In [99]: plot(rehil)
Out[99]: [<matplotlib.lines.Line2D object at 0x41148d0>]

In [100]: figure(4)
Out[100]: <matplotlib.figure.Figure object at 0x4377cd0>

In [101]: figure()
Out[101]: <matplotlib.figure.Figure object at 0x4c39c90>

In [102]: plot(rehil)
Out[102]: [<matplotlib.lines.Line2D object at 0x77d3350>]

In [103]: plot(imhil)
Out[105]: [<matplotlib.lines.Line2D object at 0x4c41e90>]

In [106]: import scipy.fftpack

In [107]: hil2 = scipy.fftpack.hilbert(thetasaw2)

In [110]: figure()
Out[110]: <matplotlib.figure.Figure object at 0x77dafd0>

In [111]: hil2[0:5]
Out[111]: array([ 0.00183964,  0.00071797,  0.000341  , -0.00038609, -0.00085497])

In [112]: plot(hil2)
Out[112]: [<matplotlib.lines.Line2D object at 0x7fee450>]

In [113]: plot(thetasaw2)
Out[113]: [<matplotlib.lines.Line2D object at 0x77da4d0>]

In [114]: 