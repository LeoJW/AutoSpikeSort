"""
generate_probe_files.py

Created 2023/03/01
@author: Leo

Generates json files for all of the main probes used by Sponberg lab
Includes device indices from plugging into intan RHD32 headstage

Please add new probes as you start using them!
"""
import numpy as np
import probeinterface as pi
import os

os.chdir(os.path.dirname(os.path.realpath(__file__)))

#----- CM32 package of A1x32-Poly5-6mm-35s-100
num_columns = 7
xpitch, ypitch = 14, 35
num_contact_per_column = [1, 6, 6, 6, 6, 6, 1]
y_shift_per_column = 35*np.array([0, -5.5, -6, -6.5, -6, -5.5, 0]) + 30
rearrange_indices = [1,0,2,3,4,5,6,
                     8,9,10,11,12,7,
                     13,15,17,18,16,14,
                     19,24,23,22,21,20,
                     30,29,28,27,26,31,25]
device_indices = [29,28,18,27,19,26,20,25,21,24,22,23,17,16,30,31,0,1,15,14,8,9,7,10,6,11,5,12,4,13,3,2]

# Generate positions
positions = []
for i in range(num_columns):
    x = np.ones(num_contact_per_column[i]) * xpitch * i
    y = np.arange(num_contact_per_column[i]) * ypitch + y_shift_per_column[i]
    positions.append(np.hstack((x[:, None], y[:, None])))
positions = np.vstack(positions)
newpositions = positions[rearrange_indices, :]

# Generate probe
probe = pi.Probe(ndim=2, si_units='um')
probe.set_contacts(positions=newpositions, shapes='circle', shape_params={'radius' : np.sqrt(100/np.pi)})
probe.create_auto_shape(probe_type='tip', margin=20)


probe.set_device_channel_indices(device_indices)
probe.annotations['manufacturer'] = 'neuronexus'
probe.annotations['name'] = 'A1x32-Poly5-6mm-35s-100'
probe.annotations['package'] = 'CM32'

probegroup = pi.ProbeGroup()
probegroup.add_probe(probe)
pi.write_probeinterface('CM32_A1x32-Poly5-6mm-35s-100.json', probegroup)

#----- A32 acute package of A1x32-Poly5-6mm-35s-100
num_columns = 7
xpitch, ypitch = 14, 35
num_contact_per_column = [1, 6, 6, 6, 6, 6, 1]
y_shift_per_column = 35*np.array([0, -5.5, -6, -6.5, -6, -5.5, 0]) + 30
rearrange_indices = [1,0,2,3,4,5,6,
                     8,9,10,11,12,7,
                     13,15,17,18,16,14,
                     19,24,23,22,21,20,
                     30,29,28,27,26,31,25]
device_indices = [30,26,21,17,27,22,20,25,28,23,19,24,29,18,31,16,0,15,2,13,8,9,7,1,6,14,10,11,5,12,4,3]

# Generate positions
positions = []
for i in range(num_columns):
    x = np.ones(num_contact_per_column[i]) * xpitch * i
    y = np.arange(num_contact_per_column[i]) * ypitch + y_shift_per_column[i]
    positions.append(np.hstack((x[:, None], y[:, None])))
positions = np.vstack(positions)
newpositions = positions[rearrange_indices, :]

# Generate probe
probe = pi.Probe(ndim=2, si_units='um')
probe.set_contacts(positions=newpositions, shapes='circle', shape_params={'radius' : np.sqrt(100/np.pi)})
probe.create_auto_shape(probe_type='tip', margin=20)


probe.set_device_channel_indices(device_indices)
probe.annotations['manufacturer'] = 'neuronexus'
probe.annotations['name'] = 'A1x32-Poly5-6mm-35s-100'
probe.annotations['package'] = 'A32'

probegroup = pi.ProbeGroup()
probegroup.add_probe(probe)
pi.write_probeinterface('A32_A1x32-Poly5-6mm-35s-100.json', probegroup)
