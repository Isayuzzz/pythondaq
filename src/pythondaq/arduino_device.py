import pyvisa
import matplotlib.pyplot as plt
import pandas as pd

# opsplitsen is opdracht 3.5

def list_devices():
    rm = pyvisa.ResourceManager("@py")
    ports = rm.list_resources()
    return ports

class ArduinoVISADevice:
    rm = pyvisa.ResourceManager("@py")
    ports = rm.list_resources()

    def __init__(self, port):
        # gewoon lijstjes maken voor R, U, I, P
        self.port = port
        self.rm = pyvisa.ResourceManager("@py")
        self.ports = self.rm.list_resources()
        # rm = pyvisa.ResourceManager("@py")
        # ports = rm.list_resources()
        # device_ = rm.open_resource(self.port, read_termination="\r\n", write_termination="\n")
        self.device_ = self.rm.open_resource(self.port, read_termination="\r\n", write_termination="\n")

    def get_identification(self):
        return self.device_.query("*IDN?")
    def set_output_value(self, value):
        self.device_.query("OUT:CH0 "+str(value))
    def get_output_value(self):
        # meet wat U over channel 1 is
        return self.device_.query("OUT:CH0?")
        # spanning_led = abs(int(device.query("MEAS:CH1?")) - int(device.query("MEAS:CH2?")))
    def get_input_value(self, channel):
        # channel = str(channel)
        return int(self.device_.query("MEAS:CH"+ str(channel) +"?"))
    def get_input_voltage(self, channel):
        # channel = str(channel)
        value = int(self.device_.query("MEAS:CH"+ str(channel) +"?"))
        voltage = (value/1023) * 3.3

        return voltage