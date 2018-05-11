# IPython log file

plot([1,2,3])mpl.__builtins__helpimport enthought.mayavi.mlab as mlabA = arange(100.0)A = arange(100.0)import enthought.mayavi.mlab as mlabA.shape=(10,10)Amatshow(A)v=zeros((10,10,10))v.shapev.dtypeAfor ii in xrange(10): v[:,:,ii] = A + 0.1*iimlab.figure()src = mlab.pipeline.scalar_field(v)src.spacingget_ipython().magic("pinfo src.update_image_data")from enthought.mayavi import mlabdata = random.random((10,10,10))iso = mlab.contour3d(data)iso.parentcd ~/datasetscd ../datasets2lscd deeblsimport niftit1 = nifti.NiftiImage('T1_aligned_class_2Gray_electrodes_backup.nii.gz')a = t1.getDataArray()from enthought.mayavi import mlabmlab.contour3d(a)mlab.view()a.max()import niftit1 = nifti.NiftiImage('T1_aligned_class_2Gray_electrodes_backup.nii.gz')a = t1.getDataArray()a.shape()a.shapea = a.Taa.shapeim = a[:,:,75]imshow(im)figure()hist(im)subim = im[where(im == 6)]figure(); imshow(subim)subim.shapesubim = im.copy()subim[where(subim != 6)] = 0.0imshow(subim)subim = im.copy()subim[where(subim != 5)] = 0.0imshow(subim)subim = im.copy()subim[where(subim != 4)] = 0.0imshow(subim)subim = im.copy()subim[where(subim != 0)] = 0.0imshow(subim)subim = im.copy()subim[where(subim != 1)] = 0.0imshow(subim)subim = im.copy()subim = im.copy(); subim[where(subim !=2)] = 0.0imshow(subim)subim = im.copy(); subim[where(subim != 3)] = 0.0subim = im.copy()subim[where(subim != 3)] = 0.0imshow(subim)subim = im.copy()subim = im.copy(); subim[where(subim != 4)] = 0.0imshow(subim)subim = im.copy(); subim[where(subim > 4)] = 0.0imshow(subim)subim = im.copy(); subim[where(subim < 4)] = 0.0imshow(subim)subim = im.copy(); subim[where(subim < 5)] = 0.0imshow(subim)subim = im.copy(); subim[where(subim < 6)] = 0.0imshow(subim)subim = im.copy(); subim[where(subim < 6.5)] = 0.0imshow(subim)subim = im.copy(); subim[where(subim < 6.1)] = 0.0imshow(subim)help mlabnumpy.__version__numpy.__file__np.__version__lsa=np.load('sig.20.npy')a.shapet=arange(0,len(a))t=t/500.0plot(t,a)d=[]d.append(a)a=np.load('sig.21.npy')d.append(a)plot(d[1])plot(d[0])lsiind = range(15,30)d = {}for ii in iind: d[ii] = np.load('sig.for ii in iind: d[ii] = np.load('sig.%s.npy' % ii)dfor ii in iind: plot(t,d[ii] + ii*200)len(d)iind[0]L = len(d[15])LL/500m = zeros((L,15),dtype='float64')for ii in iind: m[:,ii] = d[ii]for ii in iind: m[:,ii] = d[ii][:]for ii in iind: print iijj = 0for ii in iind: print ii; jj+=1jjjj =0for ii in iind: m[:,jj] = d[ii][:]; jj +=1np.save('sig.15-29.npy', m)quit()import scipy.signal as signalget_ipython().magic("pinfo signal.firwin")signal.filtfiltget_ipython().magic("pinfo signal.filtfilt")get_ipython().magic("pinfo signal.firwin")help signal.filtfilthelp signal.lfilterpwdimport clmfiltersimport nitimenpts = 2048*10sigma = 1drop_transients = 1024coef = np.array([0.9, -0.5])X,v,u = utils.ar_generator(npts, sigma, coefs, drop_transients)from nitime import utilsX,v,u = utils.ar_generator(npts, sigma, coefs, drop_transients)X,v,u = utils.ar_generator(npts, sigma, coef, drop_transients)import nitime.viznitime.viz.plot_tseries(nitime.timeseries.TimeSeries(v,smaplig_rate=1000, time_unit='s'))nitime.viz.plot_tseries(nitime.timeseries.TimeSeries(v,sampling_rate=1000, time_unit='s'))from nitime import algorithms as algimport nitime.timeseries as tsget_ipython().magic("pinfo utils.ar_generator")X,v,c = utils.ar_generator(npts, 0.1, coef , drop_transients)nitime.viz.plot_tseries(ts.TimeSeries(v,sampling_rate=1000,time_unit='s'))nitime.viz.plot_tseries(ts.TimeSeries(X,sampling_rate=1000,time_unit='s'))meeg = np.load('/home/clee/datasets2/chiang/sig.15-29.npy')eeg.shapefs=500plot(eeg[4*60*fs:(4*60+10)*fs])plot(eeg[4*60*fs:(4*60+10)*fs,5])plot(eeg[4*60*fs:(4*60+10)*fs,5],hold=False)x = eeg[4*60*fs:(4*60+10)*fs,5]t = arange(0,10,1.0/fs)t.shapex.shapeplot(t,x)plot(t,x,hold=False)subplot(511)plot(t,x,hold=False)import sigproc.filterspwdimport filterslpd5 = filters.LowPassFilter(0.5,fs=500)xd5 = lpd5.filter(x)subplot(512)plot(xd5)dx = x-xd5dx.max()lp1 = filters.LowPassFilter(1.0,fs=500)x1 = lp1.filter(x)subplot(513)plot(t,x1)lp1.ratiofreload(filters)lp1 = filters.LowPassFilter(1.0,fs=500)lp1.ratiofx1 = lp1.filter(x)plot(t,x1,hold=False)lp1.ratiofimport scipy.signalget_ipython().magic("pinfo scipy.signal.lfilter")del x1lp1 = filters.LowPassFilter(1.0,fs=500)lp1.arr_coeflpd5.arr_coeflpd01 = filters.LowPassFilter(f0hz=70, fs=500)xp70 = lpd01.filter(x)subplot(514)plot(t,xp70)plot(t,x-xp70)lpd01 = filters.LowPassFilter(f0hz=70, fs=500,order=fs)lpd01 = filters.LowPassFilter(f0hz=15, fs=500,order=fs)xp15 = lpd01.filter(x)plot(t,xp15,hold=False)plot(p15[fs:],hold=False)plot(xp15[fs:],hold=False)plot(xp15,hold=False)xp15d=lpd01.filtfilt(x)reload(filters)xp15d=lpd01.filtfilt(x)lpd01 = filters.LowPassFilter(f0hz=15, fs=500,order=50)xp15d=lpd01.filtfilt(x)figure(0
)plot(xp15d)plot(x-xp15d)import scipy.signalhelp lfilterhelp signal.lfiterhelp signal.lfilterhelp scipy.signal.lfilterf = scipy.signal.firwin(n=100,cutoff=0.2, window='hamming')f = scipy.signal.firwin(100,cutoff=0.2, window='hamming')fx = scipy.signal.lfilter(f,[1], x)plot(fx)figure()plot(fx)f01 = scipy.signal.firwin(100,cutoff=0.01, window='hamming')fx = scipy.signal.lfilter(f01,[1], x)plot(fx)figure()plot(f001)plot(f01)plot(f)f01 = scipy.signal.firwin(500,cutoff=0.01, window='hamming')plot(f01)reload(filters)get_ipython().magic("logon")get_ipython().magic("logstart")ls
help signal.firwin
help scipy.signal.firwin
ls
pwd
cd ..
cd ..
cd prog-snippets/
cd scipy-filters/
ls
run examplefiltereffects.py
run examplefiltereffects.py
a = ShowFilterEffect(x,500)
run examplefiltereffects.py
a = ShowFilterEffect(x,500)
run examplefiltereffects.py
a = ShowFilterEffect(x,500)
a = ShowFilterEffect(x,500)
run examplefiltereffects.py
a = ShowFilterEffect(x,500)
a.plot()
run examplefiltereffects.py
a = ShowFilterEffect(x,500)
a = ShowFilterEffect(x,500)
a.plot()
show()
help subplot
figure()
subplot(4,1,1)
plot([1,2,3])
suplot(4,1,3)
subplot(4,1,3)
subplot(4,1,4)
subplot(4,1,5)
ls
run examplefiltereffects.py
figure()
plot(a.ys[-1])
run examplefiltereffects.py
