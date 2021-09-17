from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
from scipy.io.wavfile import write
import binascii
import marshal

def read_obs(path):
    '''Read temperatures in observation files.
    '''

    data = np.load(path).T
    return data

if __name__ == '__main__':
    stations = {}
    long_squiggle = []
    for station in ['Arkham', 'Blackgate', 'Narrows']:
        data = read_obs(f'{station}.npy')
        with open(f"{station}-dump.pyo", "wb") as f:
            marshal.dump(data, f)
        print(station, data.shape)
        # plt.plot([datetime.utcfromtimestamp(d) for d in data[0]], data[1], label = station)
        print(data[0])
        print(data[1])
        print()

        long_squiggle = long_squiggle + list(data[1][~np.isnan(data[1])])

        stations[station] = data
        print(type(data[0][0]))

    scaled = np.int16(long_squiggle)

    for x in long_squiggle:

        try:
            print(binascii.unhexlify(hex(int(x))[2:]), end="\n")
        except:
            pass

    # bin_array = np.ones((8781,))
    # bin_list = []
    # ffts = []
    # for station in stations:
    #     X = stations[station][0]
    #     Y = stations[station][1]
    #
    #     N = X.shape[0]
    #     print(N)
    #     x = np.linspace(0.0, 1.0, N)
    #     y = X
    #
    #     yf = scipy.fftpack.fft(y)
    #     xf = np.linspace(0.0, 0.5, N)
    #     plt.plot(xf, yf)
    #
    #     for i, y in enumerate(Y):
    #         if np.isnan(y):
    #             #print(station, ":", i, X[i])
    #             #bin_array[i] = 0
    #             x = int(X[i])
    #             x_bin = np.binary_repr(x, width=32)
    #             bin_list.append(x_bin[-5])

    # print("".join(bin_list))
    #
    #
    # # print(bin_array[:8])
    # # print(bin_array[8:16])
    #
    # for i in range(0, 8781, 8):
    #     for x in range(i, i+8):
    #         print(int(bin_array[x]), end="")
    #
    #     print(" ", end="")

    # plt.xlabel('Date')
    # plt.ylabel('Temperature (C)')
    # plt.legend(title='Location')
    # plt.show()
