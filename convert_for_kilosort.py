import os
import shutil
import numpy as np
import spikeinterface as si
import spikeinterface.extractors as se
import spikeinterface.preprocessing as spre

overwrite_previous = False
data_dir = os.path.normpath('C:/Users/lwood39/Documents/VNCMP')

moth_dirs = [f.path for f in os.scandir(data_dir) if not ('previous' in f.path) if f.is_dir()]

# Generate A32 probe, use for arranging by depth
num_columns = 7
xpitch, ypitch = 14, 35
num_contact_per_column = [1, 6, 6, 6, 6, 6, 1]
y_shift_per_column = 35*np.array([0, -5.5, -6, -6.5, -6, -5.5, 0]) + 30
# Rearranges positions from order they are generated in to order given on channel map of probe
# Index of each number implicitly defines the map
# Ex: If the 0th entry of this array is the number '2', that means site at index 2 now is assigned to be site 0
# (index -> value) encodes (new position/order -> old position/order)
rearrange_indices = np.array([1,0,2,3,4,5,6,8,9,10,11,12,7,13,15,17,18,16,14,19,24,23,22,21,20,30,29,28,27,26,31,25])
# Map from probe -> adaptor
rearrange_to_adaptor = np.array([15,5,4,14,3,6,2,7,1,8,0,9,13,12,11,10,21,20,19,18,22,24,23,17,25,16,26,28,27,30,29,31])
# Map from adaptor -> headstage amplifier
rearrange_to_headstage = np.array([19,28,20,27,21,26,22,25,23,24,16,31,18,29,17,30,14,1,13,2,15,0,8,7,9,6,10,5,11,4,12,3])
device_indices = rearrange_to_headstage[rearrange_to_adaptor]
# Generate positions
positions = []
for i in range(num_columns):
    x = np.ones(num_contact_per_column[i]) * xpitch * i
    y = np.arange(num_contact_per_column[i]) * ypitch + y_shift_per_column[i]
    positions.append(np.hstack((x[:, None], y[:, None])))
positions = np.vstack(positions)
newpositions = positions[rearrange_indices, :]
device_inds = np.argsort(device_indices)
newpositions = newpositions[device_inds,:]
depth_inds = np.lexsort((newpositions[:,1], newpositions[:,0]))

# --- Loop over moths
for start_dir in moth_dirs:
    print(start_dir)
    # Find level of nesting that Record Node files start at
    found_directory = None
    for root, dirs, files in os.walk(start_dir):
        for dir_name in dirs:
            if 'Record Node' in dir_name:
                found_directory = os.path.join(root, dir_name)
                break
        if found_directory is not None:
            break
    if found_directory is None:
        print('No open-ephys directory with Record Nodes found in ' + start_dir)
        continue
    # Set up output folder
    sortfiles_dir = os.path.join(found_directory, '..', 'kilosort_data')
    if os.path.isdir(sortfiles_dir) and not overwrite_previous:
        continue
    elif not os.path.isdir(sortfiles_dir):
        os.mkdir(sortfiles_dir)
    # If the folder exists and we want overwrite, delete all files 
    else:
        for filename in os.listdir(sortfiles_dir):
            file_path = os.path.join(sortfiles_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
    # Read open-ephys data
    # Determine how many blocks to run
    n_blocks = len([f for f in os.scandir(found_directory) if f.is_dir()])
    for block in range(n_blocks):
        print(f'block {block+1}')
        # Read each block and segment, save to .bin
        # Assumes there's just one stream id
        recording = se.read_openephys(found_directory, block_index=block, stream_id='0')
        # Remove EMG headstage
        recording = recording.remove_channels([x for x in recording.get_channel_ids() if int(x[2:]) > 32])
        # recording = spre.bandpass_filter(recording, freq_min=300, freq_max=14999)
        for seg in range(len(recording._recording_segments)):
            subrecording = si.SelectSegmentRecording(recording, seg)
            si.write_binary_recording(
                subrecording,#.select_channels(subrecording.get_channel_ids()[depth_inds]), 
                os.path.join(sortfiles_dir, 'experiment' + str(block+1) + '_segment' + str(seg) + '.bin'),
                dtype='int16')