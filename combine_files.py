import os
import numpy as np
import spikeinterface as si
import spikeinterface.extractors as se




combine_files = [
    os.path.abspath('C:/Users/lwood39/Documents/VNCMP/2025_03_06/2025-03-06_13-46-24/kilosort_data/experiment2_segment1.bin'),
    os.path.abspath('C:/Users/lwood39/Documents/VNCMP/2025_02_25/2025-02-25_12-04-07/kilosort_data/experiment2_segment0.bin')
]

binaries = []
for (i,file) in enumerate(combine_files):
    rec = si.read_binary(file, num_channels=32, dtype='int16', sampling_frequency=30000)
    rec = rec.rename_channels(rec.get_channel_ids() + 32 * i)
    binaries.append(rec)