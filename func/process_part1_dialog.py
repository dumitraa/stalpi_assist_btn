'''
LAYERS NEEDED - ['STALP_JT', 'TRONSON_JT', 'BRANS_FIRI_GRPM_JT', 'FB pe C LES', 'FIRIDA_RETEA_JT', 'GRID_GEIOD', 'PTCZ_PTAB', 'TRONSON_XML_', 'TRONSON_ARANJARE', 'poze', 'FIRIDA_XML_', 'BRANSAMENT_XML_', 'GRUP_MASURA_XML_', 'STALP_XML_', 'DESCHIDERI_XML_', 'TRONSON_predare_xml', 'LINIE_MACHETA', 'STALPI_MACHETA', 'TRONSON_MACHETA', 'FIRIDA MACHETA', 'GRUP MASURA MACHETA', 'DESCHIDERI MACHETA', 'BRANSAMENTE MACHETA', 'LINIE_JT']

STEP 1.1. Complete fields: for STALPI, fill "PROP FO CATV" and "Tip zona de amplasare". Default to "Rural" unless the area is urban.

STEP 1.2. For TRONSON, populate columns with data - UNIT_LOG_INT / S_UNIT_LOG / POST_LUC

STEP 1.3. For Stalpi: complete DESC_DET - Sucursala-gestionar (formatia de lucru)

STEP 1.4. Populate row numbers in QGIS for the following: 
    > TRONSON_JT: Populate 'NR_CRT' using @row_number
    > BRANS_FIRI_GRPM_JT: Populate 'NR_CRT' using @row_number
    > STALP_JT: Populate 'NR_CRT' using @row_number

STEP 1.5. Calculate geometry with four decimal points for linestring entities.

STEP 1.6. Run models in QGIS
    > Run TRONSON JT model - LINIE_JT, STALP_JT, TRONSON_JT > TRONSON_XML_

STEP 1.7. Verify if 'DENUM' is null in TRONSON_XML_

STEP 1.8. Populate 'NR_CRT' for the following:
    > FB on C LES: Populate 'NR_CRT' using 1000 + @row_number
    > FIRIDA RETEA: Populate 'NR_CRT' using 10000 + @row_number
    
STEP 1.9. Run BRANS FIRI GRUP MASURA model
    > BRANS_FIRI_GRPM_JT, FB pe C LES, LINIE_JT > FIRIDA_XML_, BRANSAMENT_XML_, GRUP_MASURA_XML_

STEP 1.10. Run STALPI model
    > poze, STALP_JT > STALP_XML_

STEP 1.11. Process photos using (#TODO change to add a / at the end of the path). Verify photo counts match the number of poles (stalpi * 4).
    > Choose folder with photos

STEP 1.12. - #NOTE - END PART 1. Copy verified photos to the FTP server.
'''

import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QProgressBar, QPushButton, QFileDialog, QLabel, QListWidget, QListWidgetItem, QApplication, QMessageBox
from qgis.core import QgsProject, QgsMessageLog, Qgis, QgsVectorLayer, QgsApplication, QgsProcessingFeedback, QgsProcessingContext # type: ignore
from qgis.PyQt.QtGui import QColor, QFont # type: ignore
from qgis.PyQt.QtCore import Qt # type: ignore

from .helper_functions import HelperBase
from .models.tronson_jt import TronsonJTModel
from .models.bransament import BransamentModel
from .models.stalp import StalpJTModel


class ProcessPart1Dialog(QDialog):
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
            "1.1. Populeaza coloanele cu date pentru TRONSON - UNIT_LOG_INT / S_UNIT_LOG / POST_LUC",
            "1.2. Completeaza DESC_DET pentru STALPI",
            "1.3. Adauga 'Nr. Crt' pentru TRONSON JT, BRANS_FIRI_GRPM_JT, STALPI JT",
            "1.4. Calculeaza geometria cu patru zecimale pentru entitatile de linie.",
            "1.5. Ruleaza model - TRONSON JT",
            "1.6. Verifica daca 'DENUM' este null in TRONSON_XML_",
            "1.7. Populeaza 'NR_CRT' pentru FB pe C LES si FIRIDA RETEA",
            "1.8. Ruleaza model - BRANS FIRI GRUP MASURA",
            "1.9. Ruleaza model - STALPI",
            "1.10. Proceseaza fotografiile",
        ]
        
        self.unofficial_steps = [
            3, #1.1
            1, #1.2
            3, #1.3
            1, #1.4 #all layers
            1, #1.5
            1, #1.6
            2, #1.7
            1, #1.8
            1, #1.9
            1, #1.10
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
        # get tronson - linia_jt value
        # Assuming layer is already loaded
        tronson_layer = QgsProject.instance().mapLayersByName('TRONSON_JT')[0]
        LEA_VALUE = next(tronson_layer.getFeatures())['LINIA_JT']
        QgsMessageLog.logMessage(f"LEA_VALUE: {LEA_VALUE}", "StalpiAssist", level=Qgis.Info)
        BASE_PATH = os.path.dirname(os.path.abspath(__file__))  # Path of the current script
        db1_path = os.path.join(BASE_PATH, 'db/db_1.csv')


        # NOTE 1. For TRONSON, populate columns with data - UNIT_LOG_INT / S_UNIT_LOG / POST_LUC
        success = self.helper.complete_fields_based_on_mapping({
            "layer": self.layers["TRONSON_JT"],
            "csv_file": db1_path,
            "search_value": LEA_VALUE,
            "csv_key_column": "Descrierea BDI",
            "csv_value_column": ["Unitate logistica de întretinere", "Sectie unitate logistica", "Post de lucru"],
            "field_to_complete": ["UNIT_LOG_INT", "S_UNIT_LOG", "POST_LUC"]
            })
        # QgsMessageLog.logMessage(f"Steps completed: {step}", "StalpiAssist", level=Qgis.Info)
        step += 1
        self.progress_bar.setValue(step)
        self.update_step(self.steps_list, 0, success)  # Mark step 1 as done
        
        
        # NOTE 2. For Stalpi: complete DESC_DET - Sucursala-gestionar (formatia de lucru)
        success = self.helper.complete_fields_based_on_mapping({
            "layer": self.layers["STALP_JT"],
            "csv_file": db1_path,
            "search_value": LEA_VALUE,
            "csv_key_column": "Descrierea BDI",
            "csv_value_column": ['Grup planificatori pentru serviciu clienti si intr unit log', 'Post de lucru'],
            "field_to_complete": ["DESC_DET"]
            })
        # QgsMessageLog.logMessage(f"Steps completed: {step}", "StalpiAssist", level=Qgis.Info)
        step += 1
        self.progress_bar.setValue(step)
        self.update_step(self.steps_list, 1, success)  # Mark step 2 as done
        
        
        # NOTE 3. Populate row numbers in QGIS for the following: TRONSON JT, BRANS_FIRI_GRPM_JT, STALPI JT
        success1 = self.helper.add_and_populate_nr_crt_column(self.layers["TRONSON_JT"])
        success2 = self.helper.add_and_populate_nr_crt_column(self.layers["BRANS_FIRI_GRPM_JT"])
        success3 = self.helper.add_and_populate_nr_crt_column(self.layers["STALP_JT"])
        
        if success1 and success2 and success3:
            success = True
        elif success1 is False or success2 is False or success3 is False:
            success = None
        else:
            success = False
        self.update_step(self.steps_list, 2, success)  # Mark step 3 as done
        step += 1
        # QgsMessageLog.logMessage(f"Steps completed: {step}", "StalpiAssist", level=Qgis.Info)
        self.progress_bar.setValue(step)
        
        
        # NOTE 4. Calculate geometry with four decimal points for linestring entities.
        for layer in self.layers:
            if layer is not None:
                success = self.helper.round_wkt_coordinates(layer)
                step += 1
                self.progress_bar.setValue(step)
        
        self.update_step(self.steps_list, 3, success)  # Mark step 4 as done
            
        
        # NOTE 5. Run model - TRONSON JT
        algorithm = TronsonJTModel()
        params = {
            "linie_jt_introduse": self.layers["LINIE_JT"],
            "stalpi_desenati": self.layers["STALP_JT"],
            "tronson_desenat": self.layers["TRONSON_JT"],
            "TRONSON_XML_": os.path.join(self.base_dir, f"TRONSON_XML_.shp")
        }
        success = self.helper.run_algorithm(algorithm, params, self.context, self.feedback, "TRONSON_XML_")
        step += 1
        self.progress_bar.setValue(step)
        self.update_step(self.steps_list, 5, success)  # Mark step 6 as done
        
        
        # NOTE 6. Verify if 'DENUM' is null in TRONSON_XML_
        success = self.helper.verify_null(self.layers["TRONSON_XML_"], "DENUM")
        step += 1
        self.progress_bar.setValue(step)
        self.update_step(self.steps_list, 5, success)  # Mark step 6 as done
        
        
        # NOTE 7. Populate 'NR_CRT' for the following: FB pe C LES, FIRIDA RETEA
        success1 = self.helper.populate_field_based_on_row_number(self.layers["FB pe C LES"], 1000)
        success2 = self.helper.populate_field_based_on_row_number(self.layers["FIRIDA RETEA"], 10000)
        
        if success1 and success2:
            success = True
        elif success1 is False or success2 is False:
            success = None
        else:
            success = False
        self.update_step(self.steps_list, 6, success)  # Mark step 7 as done
        step += 1
        # QgsMessageLog.logMessage(f"Steps completed: {step}", "StalpiAssist", level=Qgis.Info)
        self.progress_bar.setValue(step)
        
        
        # NOTE 8. Run BRANS FIRI GRUP MASURA model
        algorithm = BransamentModel()
        params = {
            "brans_firi_desenate": self.layers["BRANS_FIRI_GRPM_JT"],
            "fb_pe_c_les": self.layers["FB pe C LES"],
            "linie_jt_introduse": self.layers["LINIE_JT"],
            "BRANSAMENT_XML_": os.path.join(self.base_dir, f"BRANSAMENT_XML_.shp"),
            "GRUP_MASURA_XML_": os.path.join(self.base_dir, f"GRUP_MASURA_XML_.shp"),
            "FIRIDA_XML_": os.path.join(self.base_dir, f"FIRIDA_XML_.shp")
        }   
        success = self.helper.run_algorithm(algorithm, params, self.context, self.feedback, ["BRANSAMENT_XML_", "FIRIDA_XML_", "GRUP_MASURA_XML_"])
        step += 1
        self.progress_bar.setValue(step)
        self.update_step(self.steps_list, 5, success)  # Mark step 6 as done
        
        
        # NOTE 9. Run STALPI model
        algorithm = StalpJTModel()
        params = {
            "poze_geotag": self.layers["poze"],
            "stalp_in_lucru": self.layers["STALP_JT"],
            "STALP_XML_": os.path.join(self.base_dir, f"STALP_XML_.shp")
        }
        success = self.helper.run_algorithm(algorithm, params, self.context, self.feedback, "STALP_XML_")
        step += 1
        self.progress_bar.setValue(step)
        self.update_step(self.steps_list, 5, success)  # Mark step 6 as done
        
        
        # NOTE 10. Process photos
        success = self.helper.copy_photos(self.base_dir)
        self.update_step(self.steps_list, 9, success)  # Mark step 10 as done
        step += 1
        # QgsMessageLog.logMessage(f"Steps completed: {step}", "StalpiAssist", level=Qgis.Info)
        self.progress_bar.setValue(step)
        
# FUNCTIONS

    def update_step(self, steps_list, index, success=True):
        """Marks a step as done by updating the list item."""
        try:
            item = steps_list.item(index)
            # QgsMessageLog.logMessage(f"Updating step {index}: {item.text()}", "StalpiAssist", level=Qgis.Info)
            if success:
                item.setText("✓ " + item.text())  # Add a checkmark
                item.setForeground(QColor("green"))  # Change text color to green to indicate completion
            elif success is None:
                item.setText("⚠ " + item.text())
                item.setForeground(QColor("orange"))  # Change text color to orange to indicate partial completion
            else:
                item.setText("✗ " + item.text())
                item.setForeground(QColor("red"))  # Change text color to red to indicate failure
            item.setFont(QFont("Arial", 10, QFont.Bold))  # Make the completed step bold
            QApplication.processEvents()  # Force UI update after each step
        except Exception as e:
            QgsMessageLog.logMessage(f"Error updating step {index}: {e}", "StalpiAssist", level=Qgis.Critical)
            pass

    # Retrieve layers by name from the QGIS project
    def get_layers(self):
        '''
        Get layers by name from the QGIS project and add them to self.layers
        '''
        QgsMessageLog.logMessage("Retrieving layers from the QGIS project...", "StalpiAssist", level=Qgis.Info)
        layers = {}
        layer_names = ['STALP_JT', 'TRONSON_JT', 'BRANS_FIRI_GRPM_JT', 'FB pe C LES', 'FIRIDA_RETEA_JT', 'GRID_GEIOD', 'PTCZ_PTAB', 'TRONSON_XML_', 'TRONSON_ARANJARE', 'poze', 'FIRIDA_XML_', 'BRANSAMENT_XML_', 'GRUP_MASURA_XML_', 'STALP_XML_', 'DESCHIDERI_XML_', 'TRONSON_predare_xml', 'LINIE_MACHETA', 'STALPI_MACHETA', 'TRONSON_MACHETA', 'FIRIDA MACHETA', 'GRUP MASURA MACHETA', 'DESCHIDERI MACHETA', 'BRANSAMENTE MACHETA', 'LINIE_JT']

        # Get all layers in the current QGIS project (keep the layer objects)
        qgis_layers = QgsProject.instance().mapLayers().values()
        QgsMessageLog.logMessage(f"----------- QGIS LAYERS: {qgis_layers}", "StalpiAssist", level=Qgis.Info)

        # Iterate through the actual layer objects
        for layer_name in layer_names:
            layer = next((l for l in qgis_layers if l.name() == layer_name), None)
            layers[layer_name] = layer  # Add the layer if found, else None
            # QgsMessageLog.logMessage(f"Layer found: key: {layer_name}, value: {layer}", "StalpiAssist", level=Qgis.Info)

        # QgsMessageLog.logMessage(f"Layers found with IDs: {layers}", "StalpiAssist", level=Qgis.Info)
        return layers

    def add_layer_to_project(self, layer_path):
        try:
            # Get the name of the layer without the file extension and the full path
            layer_name = os.path.splitext(os.path.basename(layer_path))[0]
            
            # Load the merged layer from the output path
            merged_layer = QgsVectorLayer(layer_path, layer_name, 'ogr')
            
            # Check if the layer is valid
            if not merged_layer.isValid():
                QgsMessageLog.logMessage(f"Invalid layer: {layer_path}", "StalpiAssist", level=Qgis.Critical)
                return
            
            # Add the layer to the project with the proper name
            QgsProject.instance().addMapLayer(merged_layer)
            # QgsMessageLog.logMessage(f"Layer added to project with name '{layer_name}': {layer_path}", "StalpiAssist", level=Qgis.Info)
            
        except Exception as e:
            QgsMessageLog.logMessage(f"Error adding layer to project: {e}", "StalpiAssist", level=Qgis.Critical)