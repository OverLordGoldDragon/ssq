"""
Plot the 1D wavelet filters
===========================
Let us examine the wavelet filters used by kymatio to calculate 1D scattering
transforms. Filters are generated using the
:meth:`kymatio.scattering1d.filter_bank.scattering_filter_factory` method,
which creates both the first- and second-order filter banks.
"""

###############################################################################
# Preliminaries
# -------------
# First, we import the `scattering_filter_factory` method, which we will use
# to generate the filters.

from kymatio.scattering1d.filter_bank import scattering_filter_factory

###############################################################################
# We then import `numpy` and `matplotlib` to display the filters.

import numpy as np
import matplotlib.pyplot as plt


###############################################################################
# Filter parameters and generation
# --------------------------------
# The filters are defined for a certain support size `T` which corresponds to
# the size of the input signal. The only restriction is that `T` must be a
# power of two. Since we are not computing any scattering transforms here, we
# may pick any power of two for `T`. Here, we choose `2**13 = 8192`.

T = 2**13

###############################################################################
# The parameter `J` specifies the maximum scale of the filters as a power of
# two. In other words, the largest filter will be concentrated in a time
# interval of size `2**J`.

J = 5

###############################################################################
# The `Q` parameter controls the number of wavelets per octave in the
# first-order filter bank. The larger the value, the narrower these filters
# are in the frequency domain and the wider they are in the time domain (in
# general, the number of non-negligible oscillations in time is proportional
# to `Q`). For audio signals, it is often beneficial to have a large value for
# `Q` (between 4 and 16), since these signals are often highly oscillatory and
# are better localized in frequency than they are in time. We therefore set:

Q = 8

###############################################################################
# Note that it is currently not possible to control the number of wavelets
# per octave in the second-order filter bank, which is fixed to one.
#
# We are now ready to create the filters. These are generated by the
# `scattering_filter_factory` method, which takes the logarithm of `T` and
# the `J` and `Q` parameters. It returns the lowpass filter (`phi_f`), the
# first-order wavelet filters (`psi1_f`), and the second-order filters
# (`psi2_f`).

phi_f, psi1_f, psi2_f, _ = scattering_filter_factory(np.log2(T), J, Q)

###############################################################################
# The `phi_f` output is a dictionary where each integer key corresponds points
# to the instantiation of the filter at a certain resolution. In other words,
# `phi_f[0]` corresponds to the lowpass filter at resolution `T`, while 
# `phi_f[1]` corresponds to the filter at resolution `T/2`, and so on.
#
# While `phi_f` only contains a single filter (at different resolutions),
# the `psi1_f` and `psi2_f` outputs are lists of filters, one for each wavelet
# bandpass filter in the filter bank.

###############################################################################
# Plot the filters
# ================
# We are now ready to plot the filters. We first display the lowpass filter
# (at full resolution) in red. We then plot each of the bandpass filters in
# blue. Since we don't care about the negative frequencies, we limit the
# plot to the frequency interval :math:`[0, 0.5]`. Finally, we add some
# explanatory labels and title.

plt.figure()
plt.plot(np.arange(T)/T, phi_f[0], 'r')

for psi_f in psi1_f:
    plt.plot(np.arange(T)/T, psi_f[0], 'b')

plt.xlim(0, 0.5)

plt.xlabel(r'$\omega$', fontsize=18)
plt.ylabel(r'$\hat\psi_j(\omega)$', fontsize=18)
plt.title('First-order filters (Q = {})'.format(Q), fontsize=18)

###############################################################################
# Do the same plot for the second-order filters. Note that since here `Q = 1`,
# we obtain wavelets that have higher frequency bandwidth.

plt.figure()
plt.plot(np.arange(T)/T, phi_f[0], 'r')
for psi_f in psi2_f:
    plt.plot(np.arange(T)/T, psi_f[0], 'b')
plt.xlim(0, 0.5)
plt.ylim(0, 1.2)
plt.xlabel(r'$\omega$', fontsize=18)
plt.ylabel(r'$\hat\psi_j(\omega)$', fontsize=18)
plt.title('Second-order filters (Q = 1)', fontsize=18)

###############################################################################
# Display the plots!

plt.show()
