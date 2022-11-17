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

