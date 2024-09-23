"""
generate_probe_files.py

Created 2023/03/01
@author: Leo

Generates json files for all of the main probes used by Sponberg lab
Includes device indices from plugging into intan RHD32 headstage

Note about Neuronexus probe names: 
A1x32 - Poly5 - 6mm - 35s - 100
{type}{#shanks}x{#sites/shank} - {site layout} - {shank length} {site spacing um, center-to-center} - {shank spacing, um, optional} - {site area um^2}

So A4x8-5mm-50-400-413 is:
1 or 2 dimensional probe (A), 4 shanks, 8 sites each, 5mm long shanks, 50um between sites, 400um between shanks, each site is 413um^2

Please add new probes as you start using them!
"""
import numpy as np
import probeinterface as pi
import os

os.chdir(os.path.dirname(os.path.realpath(__file__)))

#----- A1x32-Poly5-6mm-35s-100, CM32 package
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
pi.write_probeinterface('A1x32-Poly5-6mm-35s-100_CM32.json', probegroup)


#----- A1x32-Poly5-6mm-35s-100, A32 acute package
num_columns = 7
xpitch, ypitch = 14, 35
num_contact_per_column = [1, 6, 6, 6, 6, 6, 1]
y_shift_per_column = 35*np.array([0, -5.5, -6, -6.5, -6, -5.5, 0]) + 30
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
pi.write_probeinterface('A1x32-Poly5-6mm-35s-100_A32.json', probegroup)


#----- A4x8-5mm-50-400-413-A32, A32 acute package
num_shank = 4
num_site_per_shank = 8
spacing = 50
shank_spacing = 400
rearrange_indices = [
    0, 2, 4, 6, 7, 5, 3, 1,
    8, 10, 12, 14, 15, 13, 11, 9,
    16, 18, 20, 22, 23, 21, 19, 17,
    24, 26, 28, 30, 31, 29, 27, 25]
# Map from probe -> adaptor
rearrange_to_adaptor = np.array([15,5,4,14,3,6,2,7,1,8,0,9,13,12,11,10,21,20,19,18,22,24,23,17,25,16,26,28,27,30,29,31])
# Map from adaptor -> headstage amplifier
rearrange_to_headstage = np.array([19,28,20,27,21,26,22,25,23,24,16,31,18,29,17,30,14,1,13,2,15,0,8,7,9,6,10,5,11,4,12,3])
device_indices = rearrange_to_headstage[rearrange_to_adaptor]

# Generate probe
probe = pi.generate_multi_shank(
    num_shank=num_shank, shank_pitch=[shank_spacing,0], num_columns=1, num_contact_per_column=num_site_per_shank, ypitch=spacing)
shank_ids = np.hstack([np.ones(num_site_per_shank) * s for s in range(4)])
probe.set_contacts(
    positions=probe.contact_positions[rearrange_indices,:],
    shank_ids=shank_ids[rearrange_indices],
    shapes='circle', shape_params={'radius' : np.sqrt(413/np.pi)})
probe.set_contact_ids(np.arange(32))
probe.set_device_channel_indices(device_indices)
probe.annotations['manufacturer'] = 'neuronexus'
probe.annotations['name'] = 'A4x8-5mm-50-400-413'
probe.annotations['package'] = 'A32'
probegroup = pi.ProbeGroup()
probegroup.add_probe(probe)
pi.write_probeinterface('A4x8-5mm-50-400-413_A32.json', probegroup)

