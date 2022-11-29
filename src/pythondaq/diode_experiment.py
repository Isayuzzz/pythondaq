from pythondaq.arduino_device import list_devices, ArduinoVISADevice
import numpy as np

def convert_bit_to_voltage(bit):
    """convert bit to voltage

    Args:
        bit (int)

    Returns:
        voltage: float
    """
    voltage = (bit/1023)* 3.3
    return voltage

class DiodeExperiment():
    def __init__(self, port_name):
        self.current = []
        self.voltage = []
        # port = "ASRL5::INSTR"
        self.device = ArduinoVISADevice(port=port_name)

    # def scan(self, start, end):
    #     """walks trough start- end to vary manually set voltage across that range


    #     Args:
    #         start (int): 
    #         end (int): 

    #     Returns:
    #         _current and voltage
    #     """        

    #     for a in range (start, end):
    #         self.device.set_output_value(a)
    #         voltage_res = int(self.device.get_input_value(channel=2))    # in bits
    #         voltage_res_ = convert_bit_to_voltage(voltage_res)   #In Volt
    #         voltage_led = abs(int(self.device.get_input_value(channel=1)) - int(self.device.get_input_value(channel=2)))         # in bits
    #         voltage_led_ = convert_bit_to_voltage(voltage_led)        # in V

    #         stroom = voltage_res_ / 220
    #         self.current.append(stroom)
    #         self.voltage.append(voltage_led_)

    #         # results 
    #         print("ON LED: ", voltage_led, "(", voltage_led_, "V)    Over resistor  (", voltage_res_, "V)")

            
    #     self.device.set_output_value(value=0)
    #     return self.current, self.voltage
    def scan(self, start, end, times_to_repeat):
        """walks trough start- end to vary manually set voltage across that range


        Args:
            start (int): 
            end (int): 

        Returns:
            _current and voltage
        """        
        lists_current = []
        lists_voltages = []
        for b in range (times_to_repeat):
        # for a in range (start, end):
            # lists_current = []
            # lists_voltages = []

            for a in range (start, end):

                self.device.set_output_value(a)
                voltage_res = int(self.device.get_input_value(channel=2))    # in bits
                voltage_res_ = convert_bit_to_voltage(voltage_res)   #In Volt
                voltage_led = abs(int(self.device.get_input_value(channel=1)) - int(self.device.get_input_value(channel=2)))         # in bits
                voltage_led_ = convert_bit_to_voltage(voltage_led)        # in V

                stroom = voltage_res_ / 220
                self.current.append(stroom)
                self.voltage.append(voltage_led_)

                lists_current.append(self.current)
                lists_voltages.append(self.voltage)



            # results 
            print(b, "/", times_to_repeat)
            # print("ON LED: ", voltage_led, "(", voltage_led_, "V)    Over resistor  (", voltage_res_, "V)")

            lists_current_arr = np.array(lists_current)
            lists_voltage_arr = np.array(lists_voltages)
            voltage_mean = np.mean(lists_voltage_arr, axis = 0)
            current_mean = np.mean(lists_current_arr, axis = 0)
            voltage_std = np.std(lists_voltage_arr, axis = 0)
            current_std = np.std(lists_current_arr, axis = 0)

            self.device.set_output_value(value=0)
        return self.current, self.voltage, voltage_mean, current_mean, voltage_std, current_std

        