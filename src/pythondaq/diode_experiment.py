from pythondaq.arduino_device import list_devices, ArduinoVISADevice


def convert_bit_to_voltage(bit):  
    voltage = (bit/1023)* 3.3
    return voltage

class DiodeExperiment():
    def __init__(self):
        self.current = []
        self.voltage = []
        port = "ASRL5::INSTR"
        self.device = ArduinoVISADevice(port=port)
    def scan(self, start, end):
        for a in range (start, end):
            self.device.set_output_value(a)
            voltage_res = int(self.device.get_input_value(channel=2))    # in bits
            voltage_res_ = convert_bit_to_voltage(voltage_res)   #In Volt
            voltage_led = abs(int(self.device.get_input_value(channel=1)) - int(self.device.get_input_value(channel=2)))         # in bits
            voltage_led_ = convert_bit_to_voltage(voltage_led)        # in V

            stroom = voltage_res_ / 220
            self.current.append(stroom)
            self.voltage.append(voltage_led_)

            # results 
            print("ON LED: ", voltage_led, "(", voltage_led_, "V)    Over resistor  (", voltage_res_, "V)")

            
        self.device.set_output_value(value=0)
        return self.current, self.voltage