import os
import xml.etree.ElementTree as ET
import gc
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QProgressBar, QPushButton, QMessageBox
from xml.dom import minidom
from qgis.core import QgsProject, QgsMessageLog, Qgis  # type: ignore
from .helper_functions import HelperBase
from PyQt5.QtCore import QThread, pyqtSignal

class GenerateXMLDialog(QDialog):
    
    def __init__(self, base_dir):
        super().__init__()
        self.helper = HelperBase()
        self.base_dir = base_dir
        self.template_path = 'templates'
        
        self.setWindowTitle("Generate XML Files")
        self.layout = QVBoxLayout()

        self.progress_bar = QProgressBar(self)
        self.layout.addWidget(self.progress_bar)

        self.run_button = QPushButton("Generate XML Files", self)
        self.run_button.clicked.connect(self.__exec__)
        self.layout.addWidget(self.run_button)

        self.setLayout(self.layout)

    def __exec__(self):
        try:
            layers = [
                QgsProject.instance().mapLayersByName('LINIE_JT')[0],
                QgsProject.instance().mapLayersByName('STALP_XML_')[0],
                QgsProject.instance().mapLayersByName('BRANSAMENT_XML_')[0],
                QgsProject.instance().mapLayersByName('GRUP_MASURA_XML_')[0],
                QgsProject.instance().mapLayersByName('FIRIDA_XML_')[0],
                QgsProject.instance().mapLayersByName('DESCHIDERI_XML_')[0],
                QgsProject.instance().mapLayersByName('TRONSON_predare_xml')[0]
            ]

            self.progress_bar.setMaximum(len(layers))
            self.progress_bar.setValue(0)

            # Use a separate thread for generation to prevent UI freezing
            self.worker_thread = GenerateXMLWorker(layers, self.base_dir, self.template_path)
            self.worker_thread.progress_updated.connect(self.progress_bar.setValue)
            self.worker_thread.finished.connect(self.on_generation_complete)
            self.worker_thread.start()
        except IndexError as e:
            QgsMessageLog.logMessage(f"Error accessing layers: {str(e)}", level=Qgis.Critical)
            QMessageBox.critical(self, "Error", f"Could not find one or more layers. Please check layer names.")
        except Exception as e:
            QgsMessageLog.logMessage(f"Unexpected error: {str(e)}", level=Qgis.Critical)
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def on_generation_complete(self):
        # Notify user when all exports are complete
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Complete")
        msg_box.setText("File generation completed!")
        msg_box.setStandardButtons(QMessageBox.Ok)

        # Show the dialog and wait for the user's response
        if msg_box.exec_() == QMessageBox.Ok:
            self.close()  # Close the plugin dialog

class GenerateXMLWorker(QThread):
    progress_updated = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, layers, base_dir, template_path):
        super().__init__()
        self.layers = layers
        self.base_dir = base_dir
        self.template_path = template_path

    def run(self):
        self.generate_xml(self.layers)
        self.finished.emit()

    def generate_xml(self, layers):
        """
        Generates XML files for the columns of given layers, using predefined templates if available.
        Replaces blanks in column names with apostrophes.

        :param layers: List of QgsVectorLayer objects.
        """
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

        file_name_mapping = {
            "LINIE_JT": "linie_jt",
            "STALP_XML_": "stalp",
            "BRANSAMENT_XML_": "bransament",
            "GRUP_MASURA_XML_": "grup_masura",
            "FIRIDA_XML_": "firida",
            "DESCHIDERI_XML_": "deschidere",
            "TRONSON_predare_xml": "tronson_jt"
        }

        progress = 0
        for layer in layers:
            try:
                layer_name = layer.name()
                safe_layer_name = file_name_mapping.get(layer_name, layer_name)

                # Define paths
                xml_template_path = os.path.join(self.template_path, f"{safe_layer_name}.xml")
                xml_path = os.path.join(self.base_dir, f"{safe_layer_name}.xml")

                # Use XML template if available
                if os.path.exists(xml_template_path):
                    self.populate_xml_template(xml_template_path, xml_path, layer)
                else:
                    self.export_to_default_xml(xml_path, layer, safe_layer_name)
                
                progress += 1
                self.progress_updated.emit(progress)

                # Explicit garbage collection to prevent memory overflow
                gc.collect()
            except Exception as e:
                QgsMessageLog.logMessage(f"Error processing layer '{layer.name()}': {str(e)}", level=Qgis.Critical)

    def populate_xml_template(self, xml_template_path, xml_output_path, layer):
        """
        Populates an XML template with data from the given layer.
        
        :param xml_template_path: Path to the XML template file.
        :param xml_output_path: Path to save the populated XML file.
        :param layer: The QGIS vector layer containing the data.
        """
        try:
            tree = ET.parse(xml_template_path)
            root = tree.getroot()

            # Assuming the XML template has a repeating element that we need to populate with layer features
            repeating_element_tag = list(root)[0].tag  # Get the tag of the first repeating element
            parent = root

            # Remove existing entries (to refresh with new data)
            for child in root.findall(repeating_element_tag):
                parent.remove(child)

            # Populate with new data from the QGIS layer
            for feature in layer.getFeatures():
                new_element = ET.Element(repeating_element_tag)
                for field in layer.fields():
                    field_name = field.name()
                    field_value = feature[field_name]
                    if field_value in [None, "NULL", "nan"]:
                        child_element = ET.SubElement(new_element, field_name)
                    else:
                        child_element = ET.SubElement(new_element, field_name)
                        child_element.text = str(field_value)
                parent.append(new_element)

            # Prettify XML output
            rough_string = ET.tostring(root, 'utf-8')
            reparsed = minidom.parseString(rough_string)
            with open(xml_output_path, "w", encoding="utf-8") as f:
                f.write(reparsed.toprettyxml(indent="  "))

            QgsMessageLog.logMessage(f"Populated XML template for '{layer.name()}' and saved to {xml_output_path}.", level=Qgis.Info)
        except Exception as e:
            QgsMessageLog.logMessage(f"Error populating XML template for layer '{layer.name()}': {str(e)}", level=Qgis.Critical)

    def export_to_default_xml(self, xml_output_path, layer, root_name):
        """
        Exports data to a default XML format if no template is available.
        
        :param xml_output_path: Path to save the XML file.
        :param layer: The QGIS vector layer containing the data.
        :param root_name: The name of the root XML element.
        """
        try:
            root = ET.Element(f"IGEA_{root_name.upper()}")
            
            for feature in layer.getFeatures():
                feature_elem = ET.SubElement(root, f"{root_name.upper()}_JT")
                for field in layer.fields():
                    field_name = field.name()
                    field_value = feature[field_name]
                    if field_value in [None, "NULL", "nan"]:
                        field_elem = ET.SubElement(feature_elem, field_name)
                    else:
                        field_elem = ET.SubElement(feature_elem, field_name)
                        field_elem.text = str(field_value)
            
            # Prettify XML output
            rough_string = ET.tostring(root, 'utf-8')
            reparsed = minidom.parseString(rough_string)
            with open(xml_output_path, "w", encoding="utf-8") as f:
                f.write(reparsed.toprettyxml(indent="  "))

            QgsMessageLog.logMessage(f"Exported default XML for '{layer.name()}' to {xml_output_path}.", level=Qgis.Info)
        except Exception as e:
            QgsMessageLog.logMessage(f"Error exporting default XML for layer '{layer.name()}': {str(e)}", level=Qgis.Critical)
