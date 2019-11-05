"""
program to downsample eeghdf encoded eeg and take TUH labels and turn them
into standard for LPCH and Stanford
"""
# to install resampy:
#     - pip install resampy
#     - conda install resampy -c conda-forge

import h5py
import eeghdf
import resampy
import numpy as np

#%%

LPCH_COMMON_1020_LABELS = [
    "Fp1",
    "Fp2",
    "F3",
    "F4",
    "C3",
    "C4",
    "P3",
    "P4",
    "O1",
    "O2",
    "F7",
    "F8",
    "T3",
    "T4",
    "T5",
    "T6",
    "Fz",
    "Cz",
    "Pz",
    "E",
    "PG1",
    "PG2",
    "A1",
    "A2",
    "T1",
    "T2",
    "X1",
    "X2",
    "X3",
    "X4",
    "X5",
    "X6",
    "X7",
    "EEG Mark1",
    "EEG Mark2",
    "Events/Markers",
]

# common 10-20 extended clinical (T1/T2 instead of FT9/FT10)
# will need to specify these as bytes I suppose (or is this ok in utf-8 given the ascii basis)
# keys should be all one case (say upper)
lpch2edf_fixed_len_labels = dict(
    FP1="EEG Fp1         ",
    F7="EEG F7          ",
    T3="EEG T3          ",
    T5="EEG T5          ",
    O1="EEG O1          ",
    F3="EEG F3          ",
    C3="EEG C3          ",
    P3="EEG P3          ",
    FP2="EEG Fp2         ",
    F8="EEG F8          ",
    T4="EEG T4          ",
    T6="EEG T6          ",
    O2="EEG O2          ",
    F4="EEG F4          ",
    C4="EEG C4          ",
    P4="EEG P4          ",
    CZ="EEG Cz          ",
    FZ="EEG Fz          ",
    PZ="EEG Pz          ",
    T1="EEG FT9         ",  # maybe I should map this to FT9/T1
    T2="EEG FT10        ",  # maybe I should map this to FT10/T2
    A1="EEG A1          ",
    A2="EEG A2          ",
    # these are often (?always) EKG at LPCH, note edfspec says use ECG instead
    # of EKG
    X1="ECG X1          ",  # is this invariant? usually referenced to A1
    # this is sometimes ECG but not usually (depends on how squirmy)
    X2="X2              ",
    PG1="EEG Pg1         ",
    PG2="EEG Pg2         ",
    # now the uncommon ones
    NZ="EEG Nz          ",
    FPZ="EEG Fpz         ",
    AF7="EEG AF7         ",
    AF8="EEG AF8         ",
    AF3="EEG AF3         ",
    AFz="EEG AFz         ",
    AF4="EEG AF4         ",
    F9="EEG F9          ",
    # F7
    F5="EEG F5          ",
    # F3 ='EEG F3          ',
    F1="EEG F1          ",
    # Fz
    F2="EEG F2          ",
    # F4
    F6="EEG F6          ",
    # F8
    F10="EEG F10         ",
    FT9="EEG FT9         ",
    FT7="EEG FT7         ",
    FC5="EEG FC5         ",
    FC3="EEG FC3         ",
    FC1="EEG FC1         ",
    FCz="EEG FCz         ",
    FC2="EEG FC2         ",
    FC4="EEG FC4         ",
    FC6="EEG FC6         ",
    FT8="EEG FT8         ",
    FT10="EEG FT10        ",
    T9="EEG T9          ",
    T7="EEG T7          ",
    C5="EEG C5          ",
    # C3 above
    C1="EEG C1          ",
    # Cz above
    C2="EEG C2          ",
    # C4 ='EEG C4          ',
    C6="EEG C6          ",
    T8="EEG T8          ",
    T10="EEG T10         ",
    # A2
    # T3
    # T4
    # T5
    # T6
    TP9="EEG TP9         ",
    TP7="EEG TP7         ",
    CP5="EEG CP5         ",
    CP3="EEG CP3         ",
    CP1="EEG CP1         ",
    CPZ="EEG CPz         ",
    CP2="EEG CP2         ",
    CP4="EEG CP4         ",
    CP6="EEG CP6         ",
    TP8="EEG TP8         ",
    TP10="EEG TP10        ",
    P9="EEG P9          ",
    P7="EEG P7          ",
    P5="EEG P5          ",
    # P3
    P1="EEG P1          ",
    # Pz
    P2="EEG P2          ",
    # P4
    P6="EEG P6          ",
    P8="EEG P8          ",
    P10="EEG P10         ",
    PO7="EEG PO7         ",
    PO3="EEG PO3         ",
    POZ="EEG POz         ",
    PO4="EEG PO4         ",
    PO8="EEG PO8         ",
    # O1
    OZ="EEG Oz          ",
    # O2
    IZ="EEG Iz          ",
)


LPCH_TO_STD_LABELS_STRIP = {
    k: v.strip() for k, v in lpch2edf_fixed_len_labels.items()
}


def normalize_tuh2lpch_signal_label(label):
    """this throws away information about the referencing, which is not good"""
    label = label.replace("-REF", "")
    label = label.replace("-LE", "")
    label = label.replace("-RE", "")
    uplabel = label.upper()

    if uplabel in LPCH_TO_STD_LABELS_STRIP:
        return LPCH_TO_STD_LABELS_STRIP[uplabel]
    else:
        return label


def resample(
    eegh5_filename, output_filename, target_sample_frequency=0.0, window="kaiser_best"
):
    hf = eeghdf.Eeghdf(eegh5_filename)
    src_fs = hf.sample_frequency
    if target_sample_frequency == src_fs:
        target_sample_frequency = 0.0
        
    if target_sample_frequency > 0.0:
        tar_fs = target_sample_frequency
    else:
        tar_fs = src_fs


    targ_dtype = hf.rawsignals.dtype

    # it could be this first approach of doing it in memory - will only work for big memory machines or small files
    if target_sample_frequency > 0.0:    
        fdig_targfs = resampy.resample(
            np.array(hf.rawsignals, dtype=np.float64), src_fs, tar_fs, window=window
        )
        dig_tarfs = np.array(fdig_targfs, dtype=targ_dtype)
    else:
        dig_tarfs = hf.rawsignals   # not sure if this will work but just want to copy over if already at correct fs





    # now need to write that to a new file

    num_channel, num_samples_per_channel = dig_tarfs.shape

    with eeghdf.EEGHDFWriter(output_filename, "w") as eegf:
        pt = hf.patient
        eegf.write_patient_info(
            patient_name=pt['patient_name'],
            patientcode=pt['patientcode'],
            gender=pt['gender'],
            birthdate_isostring=pt['birthdate'],
            gestational_age_at_birth_days=pt['gestatational_age_at_birth_days'],
            born_premature=pt['born_premature'],
            patient_additional=pt['patient_additional'],
        )

        signal_text_labels_lpch_normalized = [
            normalize_tuh2lpch_signal_label(label) for label in hf.electrode_labels
        ]
        print(f'number of samples per channel: {num_samples_per_channel}')
        rec = eegf.create_record_block(
            record_duration_seconds=hf.duration_seconds,
            start_isodatetime=hf.start_isodatetime,
            end_isodatetime=hf.end_isodatetime,
            number_channels=num_channel,
            num_samples_per_channel=num_samples_per_channel,
            sample_frequency=tar_fs,
            signal_labels=signal_text_labels_lpch_normalized,
            signal_physical_mins=hf.signal_physical_mins,
            signal_physical_maxs=hf.signal_physical_maxs,
            signal_digital_mins=hf.signal_digital_mins,
            signal_digital_maxs=hf.signal_digital_maxs,
            physical_dimensions=hf.physical_dimensions,
            patient_age_days=hf.rec0.attrs['patient_age_days'],
            signal_prefilters=hf.rec0['prefilters'],
            signal_transducers=hf.rec0['transducers'],
            bits_per_sample=hf.rec0.attrs['bits_per_sample'],
            technician=hf.rec0.attrs['technician'],
            studyadmincode=hf.rec0.attrs['studyadmincode'],
        )

        # eegf.write_annotations_b(annotations_b)  # may be should be called record annotations
        ## now copy over the annotations
        hfannot = hf.hdf["record-0"]["edf_annotations"]  # source annotations group

        edf_annots = rec.create_group("edf_annotations")
        num_annot = len(hf._annotation_start100ns)

        starts = edf_annots.create_dataset(
            "starts_100ns", (num_annot,), data=hfannot["starts_100ns"], dtype=np.int64
        )

        # curiously these durations seem to be stored as strings but of floating
        # point values "5.00000" for 5 second duration

        durations = edf_annots.create_dataset(
            "durations_char16",
            (num_annot,),
            data=hfannot["durations_char16"],
            dtype="S16",
        )  # S16 !!! check py3 compatibility

        # variable ascii string (or b'' type)

        str_dt = h5py.special_dtype(vlen=bytes)
        texts = edf_annots.create_dataset(
            "texts", (num_annot,), data=hfannot["texts"], dtype=str_dt
        )

        
        ## now copy the data
        eegdata = rec['signals']
        eegdata[:] = dig_tarfs 
        # eegdata = rec.create_dataset(
        #     "signals",
        #     # can ommit as supplying data
        #     # (number_channels, num_samples_per_channel),
        #     # dtype=dtype,
        #     data=dig_tarfs,
        #     # chunks=(number_channels,sample_frequency),
        #     # # if wanted 1 second chunks
        #     chunks=True,
        #     fletcher32=True,
        #     compression="gzip"  # most universal, even if not "best"
        #     # maxshape=(256,None)
        # )



if __name__ == '__main__':
    import argparse
    import os
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--resamplefs', type=float, default=0.0)

    parser.add_argument('--output', '-o', default='')
    
    parser.add_argument('eegh5_filename')

    args = parser.parse_args()

    print(args)
    if not args.output:
        base, ext = os.path.splitext(args.eegh5_filename)
        if args.resamplefs:
            tarfs = args.resamplefs
            output = f'{base}.fs{args.resamplefs}norm{ext}'
        else:
            output = f'{base}.norm{ext}'
    else:
        output = args.output

    assert args.resamplefs >= 0
    
    print(f'{args.eegh5_filename}, {output}, {args.resamplefs}')
    resample(args.eegh5_filename, output_filename=output, target_sample_frequency=args.resamplefs)
