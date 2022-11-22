import click
from pythondaq.arduino_device import list_devices, ArduinoVISADevice
from pythondaq.diode_experiment import *
import pandas as pd
import matplotlib.pyplot as plt

def convert_volt_to_bit(volt):
    """converts volts to bit


    """    
    bit = (volt/3.3)* 1023
    return int(bit)



@click.group()
def cmd_group():
    """_summary_ 
    """    
    pass

# @click.option("-p", "--port")


@cmd_group.command()
def list():
    """gives the ports

    """    
    ports = list_devices()
    print(ports)
    return ports


@cmd_group.command()
@click.option("-s", "--start", default=0,)
@click.option("-e", "--end", default=3.3,)
@click.option("-o", "--output")
@click.option("-n", "--n_times", default = 3)
@click.option("-p", "--port", default = "ASRL5::INSTR")
@click.option("--graph/--no_graph", default = False)
@click.option("--csv/--no_csv", default = False)


def scan(start, end, output, n_times, port, graph, csv):
    """Does the experiment

        conditional if you want to download csv or plot data


    """    

    experiment = DiodeExperiment(port_name = port)
    current, voltage, voltage_mean, current_mean, voltage_std, current_std = experiment.scan(start = convert_volt_to_bit(start), end = convert_volt_to_bit(end), times_to_repeat=n_times)
    if csv:
        df = pd.DataFrame({'current': current_mean, 'current std': current_std, 'voltage': voltage_mean,'voltage std': voltage_std,})
        df.to_csv(output)
    print("gelukt", current_std)

    if graph:
        # plt.plot(voltage_mean, current_mean)

        # TODO voltage is te klein, er zit dus een error, hierdoor komt er geen error bar.
        plt.errorbar(voltage_mean, current_mean, yerr=current_std, fmt='o')
        plt.title('I-U curve')
        plt.xlabel('I (current)')
        plt.ylabel('voltage')
        plt.show()

    return voltage_mean, current_mean, voltage_std, current_std

@cmd_group.command()
@click.option("-p", "--port", default = "ASRL5::INSTR")

def info(port):
    """gives identification of device

    Args:
        port

    Returns:
        Identification device
    """    
    info = ArduinoVISADevice(port).get_identification()
    print(info)
    return info


if __name__ == "__main__":
    cmd_group()

