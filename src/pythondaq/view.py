# import pyvisa
# import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np
# import pythondaq.arduino_device
# import pythondaq.diode_experiment

# pdracht 3.5
# from pythondaq.arduino_device import list_devices, ArduinoVISADevice
# from pythondaq.diode_experiment import convert_bit_to_voltage, DiodeExperiment


from pythondaq.diode_experiment import *

from pythondaq.arduino_device import *
# helper functio

def convert_bit_to_voltage(bit):  
    voltage = (bit/1023)* 3.3
    return voltage

# alleen dit stukje moet erin



def do_commando():
    experiment = DiodeExperiment()

    current, voltage = experiment.scan(start = 0, end = 1023)
    le1 = current

    print(len(current), "len current")
    plt.plot(voltage, current)
    plt.title('I-U curve')
    plt.xlabel('I (current)')
    plt.ylabel('voltage')
    plt.show()

    # 2.13 CSV
    # maak list in een df en dan naar csv

    # data = pd.DataFrame({'I': current, 'U': voltage})
    # # print(data)
    # # data.to_csv('U-I.csv')              # kijk nog naar dit

# ---------------------------------





# 2.13 CSV
# maak list in een df en dan naar csv

# data = pd.DataFrame({'I': stroom, 'U': spanning})
# print(data)
# data.to_csv('U-I.csv')              # kijk nog naar dit


# Opdracht 5.22 (stop alles in een functie)




# # Opdracht 3.7
# # Ik heb bedacht om een monte carlor studie hiervan te maken
# # Herhaal het experiment 100+ keer en pak het mediaan voor iederen waarde en beschouw dat als je echte waarde
# # de standaard deviatie hiervan is de error voor iedere waarde
# print("o")
# matrix_voltage = []
# matrix_stroom = []
# for B in range(0, 3):
#     stroom, spanning = experiment.scan(start_bereik = 0, eind_bereik = 1023)
#     matrix_voltage.append(spanning)
#     matrix_stroom.append(stroom)

# # real_voltage = [sum(sub_list) / len(sub_list) for sub_list in zip(*matrix_voltage)]
# # real_stroom = [sum(sub_list) / len(sub_list) for sub_list in zip(*matrix_stroom)]
# real_voltage = np.array(matrix_voltage).mean(axis=0)
# real_stroom = np.array(matrix_stroom).mean(axis=0)

# real_voltage_std = np.std(np.array(matrix_voltage), axis=0)
# real_stro_std = np.std(np.array(matrix_stroom), axis=0)

# print("oo")

# # plt.scatter(real_voltage, real_stroom)

# plt.plot(real_voltage, real_stroom)

# plt.title('I-U curve')
# plt.xlabel('I (stroomsterkte)')
# plt.ylabel('Spanning')
# plt.show()
# print(len(real_stroom), len(le1))

# # print(real_voltage)