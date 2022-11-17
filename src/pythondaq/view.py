from pythondaq.diode_experiment import *
from pythondaq.arduino_device import *
# helper functio

def convert_bit_to_voltage(bit):  
    """convert bit to voltage

    Args:
        bit (int)

    Returns:
        voltage: float
    """    
    voltage = (bit/1023)* 3.3
    return voltage

# alleen dit stukje moet erin



def do_commando():
    """
    summary: do the expirement by command
    
    """    

    experiment = DiodeExperiment()

    current, voltage = experiment.scan(start = 0, end = 1023)

    print(len(current), "len current")
    plt.plot(voltage, current)
    plt.title('I-U curve')
    plt.xlabel('I (current)')
    plt.ylabel('voltage')
    plt.show()

