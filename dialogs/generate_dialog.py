import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QProgressBar, QPushButton, QFileDialog, QMessageBox
from qgis.core import QgsProject, QgsVectorLayer, QgsMessageLog, Qgis # type: ignore
from .helper_functions import HelperBase

class GenerateExcelDialog(QDialog):
    
    def __init__(self):
        super().__init__()
        self.helper = HelperBase()
        
        self.setWindowTitle("Generate Excel + XML Files")
        self.layout = QVBoxLayout()

        self.progress_bar = QProgressBar(self)
        self.layout.addWidget(self.progress_bar)

        self.run_button = QPushButton("Generate Excel + XML Files", self)
        self.run_button.clicked.connect(self.__exec__)
        self.layout.addWidget(self.run_button)

        self.setLayout(self.layout)

    def __exec__(self):
        self.process_data()        
        # Directory prompt for saving Excel files
        output_dir = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if not output_dir:
            return

        layers = []
        
        for i, parser in enumerate(self.processor.parsers):
            parser.generate_files(layers, self.base_dir)
            self.progress_bar.setValue(i + 1)  # Update progress for each parser processed

        # Notify user when all exports are complete
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Complete")
        msg_box.setText("File generation completed!")
        msg_box.setStandardButtons(QMessageBox.Ok)

        # Show the dialog and wait for the user's response
        if msg_box.exec_() == QMessageBox.Ok:
            self.close()  # Close the plugin dialog        

                
    def process_data(self):
        QgsMessageLog.logMessage("*******************************************Processing data...", "StalpiAssist", level=Qgis.Info)
        source_paths = [layer.source() for layer in QgsProject.instance().mapLayers().values() if isinstance(layer, QgsVectorLayer)]
        if not source_paths:
            QgsMessageLog.logMessage("No vector layers found in the project.", "StalpiAssist", level=Qgis.Warning)
            return

        if self.processor:
            QgsMessageLog.logMessage("Clearing existing parsers...!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", "StalpiAssist", level=Qgis.Info)
            self.processor = None  # Clear out any existing parsers to avoid duplicates
