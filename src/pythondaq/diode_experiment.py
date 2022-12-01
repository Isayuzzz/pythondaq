from pythondaq.arduino_device import list_devices, ArduinoVISADevice
import numpy as np
import threading


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
            print(b+1, "/", times_to_repeat)
            # print("ON LED: ", voltage_led, "(", voltage_led_, "V)    Over resistor  (", voltage_res_, "V)")

            lists_current_arr = np.array(lists_current)
            lists_voltage_arr = np.array(lists_voltages)
            self.voltage_mean = np.mean(lists_voltage_arr, axis = 0)
            self.current_mean = np.mean(lists_current_arr, axis = 0)
            self.voltage_std = np.std(lists_voltage_arr, axis = 0)
            self.current_std = np.std(lists_current_arr, axis = 0)

            self.device.set_output_value(value=0)

        return self.current, self.voltage, self.voltage_mean, self.current_mean, self.voltage_std, self.current_std
        
        # The scan thread functie maken
    def start_scan(self, start, stop, steps):
        """Start a new thread to execute a scan."""
        self._scan_thread = threading.Thread(target=self.scan, args=(start, stop, steps))
        self._scan_thread.start()

