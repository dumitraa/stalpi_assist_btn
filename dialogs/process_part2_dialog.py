'''
LAYERS NEEDED - ['STALP_JT', 'TRONSON_JT', 'BRANS_FIRI_GRPM_JT', 'FB pe C LES', 'FIRIDA_RETEA_JT', 'GRID_GEIOD', 'PTCZ_PTAB', 'TRONSON_XML_', 'TRONSON_ARANJARE', 'poze', 'FIRIDA_XML_', 'BRANSAMENT_XML_', 'GRUP_MASURA_XML_', 'STALP_XML_', 'DESCHIDERI_XML_', 'TRONSON_predare_xml', 'LINIE_MACHETA', 'STALPI_MACHETA', 'TRONSON_MACHETA', 'FIRIDA MACHETA', 'GRUP MASURA MACHETA', 'DESCHIDERI MACHETA', 'BRANSAMENTE MACHETA', 'LINIE_JT']

STEP 2.1. Update the path to the photos in the STALP_XML_ layer.

STEP 2.2. Run DESCHIDERI model
    > STALP_JT, TRONSON_XML_ > DESCHIDERI_XML_

STEP 2.3. OFFSET for duplicates - Update coordinates for TRONSON_XML using QAD plugin in QGIS. Create offset layers and export as TRONSON_ARANJARE. << #TODO find a way?

STEP 2.4. Run ACTUALIZARE TRONSON model
    > TROSON_ARANJAT > TRONSON_predare_xml

STEP 2.5. Generate XML files. Replace blanks with apostrophes. For LinieJT - without "fid".
    > lengths - 3 decimal points
    > coordinates stereo - 4 decimal points
    > coordinates wgs - 8 decimal points

STEP 2.6. Generate validation templates using XLS_1 and XLS_2 models in Excel. #TODO - is this just generating excels?
    > XLS_1 - LINIE_JT, STALP_XML_, TRONSON_XML_ > LINIE_MACHETA, STALPI_MACHETA, TRONSON_MACHETA
    > XLS_2 - BRANSAMENT_XML_, DESCHIDERI_XML_, FIRIDA_XML_, GRUP_MASURA_XML_, LINIE_JT > FIRIDA MACHETA, GRUP MASURA MACHETA, DESCHIDERI MACHETA, BRANSAMENTE_MACHETA

STEP 2.7. Export STALP, BRANS, TRONSON FIRIDA to dwg. Label and color-code.

STEP 2.8. Convert dwg to KMZ.
'''

import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QProgressBar, QPushButton, QFileDialog, QLabel, QListWidget, QListWidgetItem, QMessageBox # type: ignore
from qgis.core import QgsProject, QgsMessageLog, Qgis, QgsProcessingFeedback, QgsProcessingContext # type: ignore
from qgis.PyQt.QtCore import Qt # type: ignore


from .helper_functions import HelperBase
from .models.deschideri import DeschideriJTModel
from .models.tronson_aranjat import TronsonAranjatModel


class ProcessPart2Dialog(QDialog):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Process Data")

        # Set fixed dimensions for the window
        self.setFixedSize(500, 350)  # Example dimensions: 600x400 pixels

        self.layout = QVBoxLayout()
        
        # Label
        self.progress_text = QLabel("Steps to do:")
        self.layout.addWidget(self.progress_text)

        # Create a list to display the steps visually
        self.steps_list = QListWidget(self)
        
        self.steps_list.setStyleSheet("""
            QListWidget::item {
                color: black;  # Keep text color black
                background-color: #f0f0f0;  # Default background for light mode
            }
            QListWidget::item:selected {
                background-color: #d0e0f0;  # Slightly different background for selected items
            }
        """)

        self.steps = [
            "2.1. Actualizeaza calea pozelor - STALP_XML_",
            "2.2. Ruleaza model - DESCHIDERI",
            "2.3. Off-set pentru duplicate",
            "2.4. Ruleaza modelul ACTUALIZARE TRONSON",
            "2.5. Genereaza sabloane de validare - XLS_1 si XLS_2",
            "2.6. Exporta STALP, BRANS, TRONSON FIRIDA in dwg."
        ]
        
        self.unofficial_steps = [
            1, #2.1
            1, #2.2
            1, #2.3
            1, #2.4
            2, #2.5
            4 #2.6
        ]

        # Add steps to the list, making them non-interactive
        for step in self.steps:
            item = QListWidgetItem(step)
            item.setFlags(item.flags() & ~Qt.ItemIsSelectable & ~Qt.ItemIsEnabled)  # Make items non-interactive but visible
            self.steps_list.addItem(item)
            QgsMessageLog.logMessage(f"{self.steps_list}", "StalpiAssist", level=Qgis.Info)

        self.layout.addWidget(self.steps_list)

        self.progress_bar = QProgressBar(self)
        self.layout.addWidget(self.progress_bar)

        self.btn_layout = QHBoxLayout()
        
        self.run_button = QPushButton("Run", self)
        self.run_button.clicked.connect(self.__exec__)
        self.btn_layout.addWidget(self.run_button)
        
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)
        self.btn_layout.addWidget(self.close_button)
        self.layout.addLayout(self.btn_layout)
        
        self.setLayout(self.layout)

    def __exec__(self):
        QgsMessageLog.logMessage("Starting data preprocessing...", "StalpiAssist", level=Qgis.Info)
        
        # error-checking: no layers present, show a DIALOG BOX with the error message
        if not QgsProject.instance().mapLayers().values():
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Error")
            msg_box.setText("No layers are present in the project.")
            msg_box.setStandardButtons(QMessageBox.Ok)
            
            if msg_box.exec_() == QMessageBox.Ok:
                self.close()
            return
        
        self.helper = HelperBase()
        self.feedback = QgsProcessingFeedback()
        self.context = QgsProcessingContext()
        # Automated layer retrieval
        self.layers = self.get_layers()
        if not self.layers:
            QgsMessageLog.logMessage("No layers found matching the required names.", "StalpiAssist", level=Qgis.Critical)
            return
        
        # Update progress bar
        layers_valid = [layer for layer in self.layers.values() if layer is not None]
        total_steps = sum(self.unofficial_steps)
        self.progress_bar.setMaximum(total_steps)
        step = 0
        self.base_dir = QFileDialog.getExistingDirectory(None, "Select Folder")
        if not self.base_dir:
            return
        os.makedirs(self.base_dir, exist_ok=True)  # Ensure directory exists

        # Execute all processing steps
        QgsMessageLog.logMessage("-------- START OF DATA PREPROCESSING --------", "StalpiAssist", level=Qgis.Info)
        
        self.run_button.setEnabled(False)
        self.close_button.setEnabled(False)
        
# STEPS
        # NOTE 1. Update the path to the photos in the STALP_XML_ layer
        success = self.helper.copy_photos(self.base_dir)
        step += 1
        self.progress_bar.setValue(step)
        self.update_step(self.steps_list, 0, success)  # Mark step 1 as done
        
        
        # NOTE 2. Run the DESCHIDERI model
        algorithm = DeschideriJTModel()
        params = {
            'stalpi_desenati': self.layers['STALP_JT'],
            'tronson_jt': self.layers['TRONSON_XML_'],
            'DESCHIDERI_XML_': os.path.join(self.base_dir, f"DESCHIDERI_XML_.shp"),
            'SCR_DWG': os.path.join(self.base_dir, f"SCR_DWG.shp"),
        }
        success = self.helper.run_algorithm(algorithm, params, self.context, self.feedback, ["DESCHIDERI_XML_", "SCR_DWG"])
        step += 1
        self.progress_bar.setValue(step)
        self.update_step(self.steps_list, 1, success)
        
        # NOTE 3. OFFSET for duplicates - Update coordinates for TRONSON_XML using QAD plugin in QGIS. Create offset layers and export as TRONSON_ARANJARE.
        
        
        # NOTE 4. Run the ACTUALIZARE TRONSON model
        algorithm = TronsonAranjatModel()
        params = {
            'tronson_aranjat': self.layers['TRONSON_ARANJAT'],
            'TRONSON_predare_xml': os.path.join(self.base_dir, f"TRONSON_predare_xml.shp"),
        }
        success = self.helper.run_algorithm(algorithm, params, self.context, self.feedback, ["TRONSON_predare_xml"])
        step += 1
        self.progress_bar.setValue(step)
        self.update_step(self.steps_list, 3, success)
        
        # NOTE 5. Export STALP, BRANS, TRONSON FIRIDA to dwg. Label and color-code.
        
        # NOTE 6. Convert dwg to KMZ.
        
        
# FUNCTIONS