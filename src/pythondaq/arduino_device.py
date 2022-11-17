import pyvisa
import matplotlib.pyplot as plt
import pandas as pd


def list_devices():
    rm = pyvisa.ResourceManager("@py")
    ports = rm.list_resources()
    return ports

class ArduinoVISADevice:
    rm = pyvisa.ResourceManager("@py")
    ports = rm.list_resources()

    def __init__(self, port):
        # Just make a few lists
        self.port = port
        self.rm = pyvisa.ResourceManager("@py")
        self.ports = self.rm.list_resources()
        self.device_ = self.rm.open_resource(self.port, read_termination="\r\n", write_termination="\n")

    # Simply query the correct channel for each list

    def get_identification(self):
        return self.device_.query("*IDN?")

    def set_output_value(self, value):
        self.device_.query("OUT:CH0 "+str(value))

    def get_output_value(self):
        return self.device_.query("OUT:CH0?")

    def get_input_value(self, channel):
        return int(self.device_.query("MEAS:CH"+ str(channel) +"?"))

    def get_input_voltage(self, channel):
        value = int(self.device_.query("MEAS:CH"+ str(channel) +"?"))
        voltage = (value/1023) * 3.3

        return voltage