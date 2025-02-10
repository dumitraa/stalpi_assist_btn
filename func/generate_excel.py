from pathlib import Path
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QProgressBar, QPushButton, QMessageBox # type: ignore
from qgis.core import QgsProject, QgsMessageLog, Qgis  # type: ignore
from .helper_functions import HelperBase, SHPProcessor
import os
import uuid
import time
import shutil

class GenerateExcelDialog(QDialog):
    
    def __init__(self, base_dir):
        super().__init__()
        self.helper = HelperBase()
        self.base_dir = base_dir
        self.template_path = 'templates'
        self.processor = None
        self.layers = self.helper.get_layers()
        
        self.setWindowTitle("Generate Anexa")
        self.layout = QVBoxLayout()

        self.progress_bar = QProgressBar(self)
        self.layout.addWidget(self.progress_bar)

        self.run_button = QPushButton("Generate Excel File", self)
        self.run_button.clicked.connect(self.__exec__)
        self.layout.addWidget(self.run_button)

        self.setLayout(self.layout)
        
    @staticmethod
    def plugin_path(*args) -> Path:
        """ Return the path to the plugin root folder or file. """
        path = Path(__file__).resolve().parent
        for item in args:
            path = path.joinpath(item)
        return path

    def __exec__(self):
        try:
            # Process layers
            try:
                self.process_layers()
                if self.processor is None:
                    raise ValueError("No processor found.")
            except Exception as e:
                QgsMessageLog.logMessage(f"Error processing layers: {e}", "StalpiAssist", level=Qgis.Critical)
                raise

            layer_names = ['LINIE_JT', 'STALP_XML_', 'BRANSAMENT_XML_', 
                        'GRUP_MASURA_XML_', 'FIRIDA_XML_', 'DESCHIDERI_XML_', 
                        'TRONSON_predare_xml']
            layers = []
            for name in layer_names:
                found_layers = QgsProject.instance().mapLayersByName(name)
                if not found_layers:
                    raise ValueError(f"Layer {name} not found!")
                layers.append(found_layers[0])

            # Load template file
            template_file = self.plugin_path('templates', 'anexa.xlsx')
            if not template_file.exists():
                raise FileNotFoundError(f"Template file not found at {template_file}")

            # Create a temporary copy of the template file
            new_file_name = f"ANEXA_4-6_machete_de_completat_JT.xlsx"
            new_file_path = self.helper.create_valid_output(self.base_dir, new_file_name, "machete")
            self.copy_file(template_file, new_file_path)

            # Set up progress bar
            self.progress_bar.setMaximum(len(layer_names))
            self.progress_bar.setValue(0)

            # Process parsers and write to the Excel file
            for i, parser in enumerate(self.processor.parsers):
                try:
                    parser.write_to_excel_sheet(new_file_path)
                except Exception as e:
                    QgsMessageLog.logMessage(f"Error during processing: {e}", "StalpiAssist", level=Qgis.Critical)
                    raise
                self.progress_bar.setValue(i + 1)
            
        except Exception as e:
            QgsMessageLog.logMessage(f"Error during execution: {e}", "StalpiAssist", level=Qgis.Critical)
            raise

        # Notify the user when the process is complete
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Complete")
        msg_box.setText("File generation completed!")
        msg_box.setStandardButtons(QMessageBox.Ok)

        if msg_box.exec_() == QMessageBox.Ok:
            self.close()  # Close the plugin dialog

    def copy_file(self, source, destination):
        """Copy file using shutil for simplicity."""
        try:
            shutil.copyfile(source, destination)
        except Exception as e:
            QgsMessageLog.logMessage(f"Error copying file: {e} // sourse was {source}, dest was {destination}", "StalpiAssist", level=Qgis.Critical)


    def process_layers(self):
        old_layers = self.layers
        
        if not self.processor:
            try:
                self.processor = SHPProcessor(self.layers)
            except Exception as e:
                QgsMessageLog.logMessage(f"Error creating processor: {e}", "StalpiAssist", level=Qgis.Critical)
                return
        
        try:
            current_layers = self.helper.get_layers()
        except Exception as e:
            QgsMessageLog.logMessage(f"Error getting layers: {e}", "StalpiAssist", level=Qgis.Critical)
            return
        
        if current_layers != old_layers:
            self.processor = None
            
            try:
                self.processor = SHPProcessor(current_layers)
            except Exception as e:
                QgsMessageLog.logMessage(f"Error creating processor: {e}", "StalpiAssist", level=Qgis.Critical)
                return
        else:
            return