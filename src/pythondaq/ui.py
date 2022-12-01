import sys
from PySide6 import QtWidgets
from PySide6.QtCore import Slot
import pyqtgraph as pg
import numpy as np
from pythondaq.diode_experiment import *
import pandas as pd
import matplotlib.pyplot as plt
import pyvisa



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
    """
        The userinterface of the experimenmt

        Contains all the relevant buttons, widgets and experiments

    """    

    def __init__(self):     
        super().__init__()
        # measurements
        self.voltage_mean, self.current_mean, self.voltage_std, self.current_std = [], [], [], []
        # guves ports
        rm = pyvisa.ResourceManager("@py")
        self.ports = rm.list_resources()
        # default port
        self.port_name = "ASRL5::INSTR"
        self.path_plus_name = ""
        # Intilise df
        self.df = pd.DataFrame()

        # ------------------     widget spinboxes for min, max and numpoints
        self.widget_spin_box_min = QtWidgets.QDoubleSpinBox()
        self.widget_spin_box_min.setRange(0, 3.0)
        self.widget_spin_box_min.setSingleStep(0.1)

        self.widget_spin_box_max = QtWidgets.QDoubleSpinBox()
        self.widget_spin_box_max.setRange(1.0,3.3)
        self.widget_spin_box_max.setSingleStep(0.1)

        self.numpoints = QtWidgets.QSpinBox()
        self.numpoints.setRange(0,10)
        self.numpoints.setSingleStep(1)
        self.numpoints.valueChanged.connect(self.value_changed)        

        # Browse button and save button
        self.browse_button = QtWidgets.QPushButton("Browse")
        self.save_button = QtWidgets.QPushButton("save")
        self.start_button = QtWidgets.QPushButton("start")

        self.port_selector = QtWidgets.QComboBox()

        # add ports in saveports
        for a in self.ports:
            self.port_selector.addItem(a)
        self.port_selector.currentIndexChanged.connect(self.value_changed)
       

        # initiate the plot
        self.plot_widget = pg.PlotWidget()
        
        experiment = DiodeExperiment(port_name = self.port_name)
        start = 0; end =3.3; n_times = 1

        _, _, self.voltage_mean, self.current_mean, self.voltage_std, self.current_std = experiment.scan(start = convert_volt_to_bit(start), end = convert_volt_to_bit(end), times_to_repeat=n_times)
        
        # plot widget with labels
        self.plot_widget.plot(self.voltage_mean, self.current_mean, pen=None, symbol="o")
        self.plot_widget.setLabel("left", "y")
        self.plot_widget.setLabel("bottom", "x ")

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

        # add click.connect to buttons
        self.browse_button.clicked.connect(self.browse)
        self.save_button.clicked.connect(self.save)
        self.start_button.clicked.connect(self.plotter)
      
    @Slot()
    def plotter(self):
        """plot sin function

            arg: self 
        Returns:
            plot 
        """        
        self.plot_widget.clear() 
        start =self.widget_spin_box_min.value(); end = self.widget_spin_box_max.value(); n_times = self.numpoints.value()

        experiment = DiodeExperiment(port_name = self.port_name)
        # _, _, self.voltage_mean, self.current_mean, self.voltage_std, self.current_std = experiment.scan(start = convert_volt_to_bit(start), end = convert_volt_to_bit(end), times_to_repeat=n_times)
        experiment.start_scan(start = convert_volt_to_bit(start), stop= convert_volt_to_bit(end), steps=n_times)
        experiment._scan_thread.join()
        # self.experiment.voltage_mean
        zipped = list(zip(experiment.voltage_mean, experiment.current_mean, experiment.voltage_std, experiment.current_std))

        df = pd.DataFrame(zipped, columns=['voltage_mean', 'current_mean', 'voltage_std', 'current_std'])
        self.df = df

        self.plot_widget.plot(experiment.voltage_mean, experiment.current_mean, pen=None, symbol="o")
        self.plot_widget.setLabel("left", "y")
        self.plot_widget.setLabel("bottom", "x ")
        
        return df

    @Slot()
    def browse(self):
        """gives path chosen by user
        """        
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(filter="CSV files (*.csv)")
        self.path_plus_name = filename

        return filename

    @Slot()
    def save(self):
        """saves data as csv file
        """        
        self.df.to_csv(self.path_plus_name)
        return

    @Slot()
    def value_changed(self):
        """This function does nothing, 
        it is only used in order to be used as an argument 
        to make the code function properly
        """        
        return None


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())
if __name__ == "__main__":
    main()

print("gelukt")