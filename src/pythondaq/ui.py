import sys
from PySide6 import QtWidgets
from PySide6.QtCore import Slot
import pyqtgraph as pg
import numpy as np
from pythondaq.diode_experiment import *
import pandas as pd
import matplotlib.pyplot as plt
import pyvisa
import threading



#    self.rm = pyvisa.ResourceManager("@py")
#         self.ports = self.rm.list_resources()
#         self.device_ = self.rm.open_resource(self.port, read_termination="\r\n", write_termination="\n")


# PyQtGraph global options
pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")

def convert_volt_to_bit(volt):
    """converts volts to bit

    """    
    bit = (volt/3.3)* 1023
    return int(bit)



class UserInterface(QtWidgets.QMainWindow):
    """User Interface to plot a sin function 

        ARg: Q main window

        Return: User interface of a sin function with spinboxes to vary min, max, number of steps

    """    

    def __init__(self):
        super().__init__()

        self.voltage_mean, self.current_mean, self.voltage_std, self.current_std = [], [], [], []

        rm = pyvisa.ResourceManager("@py")
        self.ports = rm.list_resources()
        self.port_name = "ASRL5::INSTR"
        self.path_plus_name = ""
        self.df = pd.DataFrame()
        print(self.ports)

        # ------------------     widget spinboxes for min, max and numpoints
        self.widget_spin_box_min = QtWidgets.QDoubleSpinBox()
        self.widget_spin_box_min.setRange(0, 3.0)
        self.widget_spin_box_min.setSingleStep(0.1)
        # self.widget_spin_box_min.valueChanged.connect(self.value_changed)

        self.widget_spin_box_max = QtWidgets.QDoubleSpinBox()
        self.widget_spin_box_max.setRange(1.0,3.3)
        self.widget_spin_box_max.setSingleStep(0.1)
        # self.widget_spin_box_max.valueChanged.connect(self.value_changed)

        self.numpoints = QtWidgets.QSpinBox()
        self.numpoints.setRange(0,10)
        self.numpoints.setSingleStep(1)
        self.numpoints.valueChanged.connect(self.value_changed)        

        self.browse_button = QtWidgets.QPushButton("Browse")
        self.save_button = QtWidgets.QPushButton("save")
        self.start_button = QtWidgets.QPushButton("start")

        self.port_selector = QtWidgets.QComboBox()
        for a in self.ports:
            self.port_selector.addItem(a)
        self.port_selector.currentIndexChanged.connect(self.value_changed)
        
        

        # self.port_selector.valueChanged.connect(self.new_port)
        # # ------------------

        # initiate the plot
        self.plot_widget = pg.PlotWidget()
        
        experiment = DiodeExperiment(port_name = self.port_name)
        start = 0; end =3.3; n_times = 1

        _, _, self.voltage_mean, self.current_mean, self.voltage_std, self.current_std = experiment.scan(start = convert_volt_to_bit(start), end = convert_volt_to_bit(end), times_to_repeat=n_times)


        self.plot_widget.plot(self.voltage_mean, self.current_mean, pen=None, symbol="o")
        self.plot_widget.setLabel("left", "y")
        self.plot_widget.setLabel("bottom", "x ")
        


        # TODO voltage is te klein, er zit dus een error, hierdoor komt er geen error bar.
        # plt.errorbar(voltage_mean, current_mean, yerr=current_std, fmt='o')
     

        # title
        self.setWindowTitle("My sine function")
        # start central widget
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        # create vbox
        vbox = QtWidgets.QVBoxLayout(central_widget)
        vbox.addWidget(self.plot_widget)

        # labels
        self.l1 = QtWidgets.QLabel()
        self.l2 = QtWidgets.QLabel()
        self.l3 = QtWidgets.QLabel()
        self.l1.setText("Start Voltage")
        self.l2.setText("End Voltage")
        self.l3.setText("Number of experiments")
        # hbox for labels
        hbox0 = QtWidgets.QHBoxLayout()
        hbox0.addWidget(self.l1)
        hbox0.addWidget(self.l2)
        hbox0.addWidget(self.l3)
        vbox.addLayout(hbox0)
        # create H box for the windget spinners and add it to layout

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.widget_spin_box_min)
        hbox.addWidget(self.widget_spin_box_max)
        hbox.addWidget(self.numpoints)
        # hbox.addWidget(self.filename)

        vbox.addLayout(hbox)
        
        # button for browse and save options
        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addWidget(self.browse_button)
        hbox2.addWidget(self.save_button)
        hbox2.addWidget(self.start_button)
        hbox2.addWidget(self.port_selector)
        vbox.addLayout(hbox2)

        self.browse_button.clicked.connect(self.browse)
        self.save_button.clicked.connect(self.save)
        self.start_button.clicked.connect(self.plotter)
        # self.port_selector.clicked.connect(self.new_port)
        # TODO save button nog erbij krijgen; probleem ligt bij het feit dat je nog geen argumenten mag geven
        # self.save_button.clicked.connect(self.save, arguments= (self.browse(), self.plotter(self.widget_spin_box_min.value, self.widget_spin_box_max.value, self.numpoints.value)))



    @Slot()
    def plotter(self):
        """plot sin function

            arg: self 
        Returns:
            plot 
        """        
        self.plot_widget.clear() 
        # start = 0; end =3.3; n_times = 1
        start =self.widget_spin_box_min.value(); end = self.widget_spin_box_max.value(); n_times = self.numpoints.value()
        experiment = DiodeExperiment(port_name = self.port_name)
        _, _, self.voltage_mean, self.current_mean, self.voltage_std, self.current_std = experiment.scan(start = convert_volt_to_bit(start), end = convert_volt_to_bit(end), times_to_repeat=n_times)
        zipped = list(zip(self.voltage_mean, self.current_mean, self.voltage_std, self.current_std))


        df = pd.DataFrame(zipped, columns=['voltage_mean', 'current_mean', 'voltage_std', 'current_std'])
        self.df = df

        self.plot_widget.plot(self.voltage_mean, self.current_mean, pen=None, symbol="o")
        self.plot_widget.setLabel("left", "y")
        self.plot_widget.setLabel("bottom", "x ")
        
        return df
    @Slot()
    def browse(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(filter="CSV files (*.csv)")
        self.path_plus_name = filename
        return filename

    @Slot()
    def save(self):
        self.df.to_csv(self.path_plus_name)
        return
    @Slot()
    def value_changed(self):
        # self.widget_spin_box_min = self.widget_spin_box_min.value()
        # self.widget_spin_box_max = self.widget_spin_box_max.value()
        # self.numpoints = self.numpoints.value()
        return None

    # @Slot
    # def port_value_changed(self):
        


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())
if __name__ == "__main__":
    main()

print("gelukt")