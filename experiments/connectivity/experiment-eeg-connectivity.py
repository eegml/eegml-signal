# This is an effort to reproduce the methods of PetersJM "Brain functional networks in syndromic and non-syndromic autism---a graph theoretic study of EEG connectivity"

methods = """
1. create average reference
2. spatially down-sampled to the standard clinical 19 electrodes
3. EEGlab was used for
 a. band-pass filtering (FIR filter 1-70Hz
 b. rejection of artfact-ridden epochs and selection of awake task-free data segments with a minimum of 2 minutes
 c. epochs with evidence of muscle artifact were, where ossible, rejected
 d. ICA was used for semi-automated artifact rejection of eye blinks and lateral eye movements see ref 38
4. The average reference was used for calculation of connectivity
  a. coherence was calcuated for each segment individually
  b. the connectivity measure was by computing the average of these coherences weighted by segment length

  Coherence Coh(S_i, f) for frequency $f$
  Frequency band \phi of interest
  S_i(t) is the signal in the i-th segments

  Connectivity measure C = \int_{\phi} \frac{\sum_{i=1}^N L_i Coh(S_i, f){\sum{i=1}^N L_i} df


  The ~theta band (4-8 hz) and lower and upper alpha bands 8-10Hz, 10-12Hz were chosen on the basis of previous findings in disconnection syndromes [ref 14, 45, 46] and avoiding muscle artifact contamination in higher frquencies


  Graph analysis


  Note: mne-python/mne/connectivity/spectral.py spectral_connectivity in mne does some of this


      Supported Connectivity Measures:

    The connectivity method(s) is specified using the "method" parameter. The
    following methods are supported (note: E[] denotes average over epochs).
    Multiple measures can be computed at once by using a list/tuple, e.g.
    "['coh', 'pli']" to compute coherence and PLI.

    'coh' : Coherence given by

                 | E[Sxy] |
        C = ---------------------
            sqrt(E[Sxx] * E[Syy])

    'cohy' : Coherency given by

                   E[Sxy]
        C = ---------------------
            sqrt(E[Sxx] * E[Syy])

    'imcoh' : Imaginary coherence [1] given by

                  Im(E[Sxy])
        C = ----------------------
            sqrt(E[Sxx] * E[Syy])

    'plv' : Phase-Locking Value (PLV) [2] given by

        PLV = |E[Sxy/|Sxy|]|

    'ppc' : Pairwise Phase Consistency (PPC), an unbiased estimator of squared
            PLV [3].

    'pli' : Phase Lag Index (PLI) [4] given by

        PLI = |E[sign(Im(Sxy))]|

    'pli2_unbiased' : Unbiased estimator of squared PLI [5].

    'wpli' : Weighted Phase Lag Index (WPLI) [5] given by

                  |E[Im(Sxy)]|
        WPLI = ------------------
                  E[|Im(Sxy)|]

    'wpli2_debiased' : Debiased estimator of squared WPLI [5].

    References
    ----------

    [1] Nolte et al. "Identifying true brain interaction from EEG data using
        the imaginary part of coherency" Clinical neurophysiology, vol. 115,
        no. 10, pp. 2292-2307, Oct. 2004.

    [2] Lachaux et al. "Measuring phase synchrony in brain signals" Human brain
        mapping, vol. 8, no. 4, pp. 194-208, Jan. 1999.

    [3] Vinck et al. "The pairwise phase consistency: a bias-free measure of
        rhythmic neuronal synchronization" NeuroImage, vol. 51, no. 1,
        pp. 112-122, May 2010.

    [4] Stam et al. "Phase lag index: assessment of functional connectivity
        from multi channel EEG and MEG with diminished bias from common
        sources" Human brain mapping, vol. 28, no. 11, pp. 1178-1193,
        Nov. 2007.

    [5] Vinck et al. "An improved index of phase-synchronization for electro-
        physiological data in the presence of volume-conduction, noise and
        sample-size bias" NeuroImage, vol. 55, no. 4, pp. 1548-1565, Apr. 2011.


"""  

