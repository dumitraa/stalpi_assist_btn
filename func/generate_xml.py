import os
import xml.etree.ElementTree as ET
import gc
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QProgressBar, QPushButton, QMessageBox
from xml.dom import minidom
from qgis.core import QgsProject, QgsMessageLog, Qgis  # type: ignore
from .helper_functions import HelperBase, SHPProcessor
from PyQt5.QtCore import QThread, pyqtSignal
from pathlib import Path

class GenerateXMLDialog(QDialog):
    
    def __init__(self, base_dir):
        super().__init__()
        self.helper = HelperBase()
        self.base_dir = base_dir
        self.template_path = 'templates'
        self.processor = None
        
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
            qgis_layers = [
                QgsProject.instance().mapLayersByName('LINIE_JT'),
                QgsProject.instance().mapLayersByName('STALP_XML_'),
                QgsProject.instance().mapLayersByName('BRANSAMENT_XML_'),
                QgsProject.instance().mapLayersByName('GRUP_MASURA_XML_'),
                QgsProject.instance().mapLayersByName('FIRIDA_XML_'),
                QgsProject.instance().mapLayersByName('DESCHIDERI_XML_'),
                QgsProject.instance().mapLayersByName('TRONSON_predare_xml')
            ]

            self.progress_bar.setMaximum(len(qgis_layers))
            self.progress_bar.setValue(0)

            # Use a separate thread for generation to prevent UI freezing
            self.worker_thread = GenerateXMLWorker(self.base_dir, self.template_path)
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

    def __init__(self, base_dir, template_path):
        super().__init__()
        self.helper = HelperBase()
        self.layers = self.helper.get_layers()
        self.base_dir = base_dir
        self.template_path = template_path
        self.processor = None

    def run(self):
        self.generate_xml()
        self.finished.emit()
        
    @staticmethod
    def plugin_path(*args) -> Path:
        """ Return the path to the plugin root folder or file. """
        path = Path(__file__).resolve().parent
        for item in args:
            path = path.joinpath(item)
        return path

    def generate_xml(self):
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
        self.process_layers()
        try: 
            for parser in self.processor.parsers:
                try:
                    layer_name = parser.get_name()
                    safe_layer_name = file_name_mapping.get(layer_name, layer_name)

                    # Define paths
                    xml_template_path = self.plugin_path(f"templates/{safe_layer_name}.xml")
                    xml_path = os.path.join(self.base_dir, f"{safe_layer_name}.xml")

                    # Use XML template if available
                    if os.path.exists(xml_template_path):
                        QgsMessageLog.logMessage(f"Found template for '{layer_name} - {safe_layer_name} with path {xml_template_path}'. Populating XML.", level=Qgis.Info)
                        self.populate_xml_template(xml_template_path, xml_path, parser)
                    else:
                        QgsMessageLog.logMessage(f"No template found for '{layer_name} - {safe_layer_name} with path {xml_template_path}'. Exporting default XML.", level=Qgis.Warning)
                        self.export_to_default_xml(xml_path, parser, safe_layer_name)
                    
                    progress += 1
                    self.progress_updated.emit(progress)

                    # Explicit garbage collection to prevent memory overflow
                    gc.collect()
                except Exception as e:
                    QgsMessageLog.logMessage(f"Error processing layer '{layer_name}': {str(e)}", level=Qgis.Critical)
        except AttributeError as e:
            QgsMessageLog.logMessage(f"Error processing layers: {str(e)}", level=Qgis.Critical)
            QMessageBox.critical(None, "Layer Processing Error", f"An error occurred while processing layers: {e}")

    def populate_xml_template(self, xml_template_path, xml_output_path, parser):
        """
        Populates an XML template with data from the given parser.
        
        :param xml_template_path: Path to the XML template file.
        :param xml_output_path: Path to save the populated XML file.
        :param parser: Parser object containing qgis_mapping with data.
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

            # Populate with new data from the parser
            for feature_data in parser.get_data():
                new_element = ET.Element(repeating_element_tag)
                for qgis_field, xml_field in parser.qgis_mapping.items():
                    # Use getattr to access the attribute of the LinieJT object
                    field_value = getattr(feature_data, xml_field.lower(), None)  # Convert to lowercase to match attribute names if needed
                    if field_value in [None, "NULL", "nan"]:
                        child_element = ET.SubElement(new_element, xml_field)
                    else:
                        child_element = ET.SubElement(new_element, xml_field)
                        child_element.text = str(field_value)
                parent.append(new_element)


            # Prettify XML output
            rough_string = ET.tostring(root, 'utf-8-sig')
            reparsed = minidom.parseString(rough_string)
            with open(xml_output_path, "w", encoding="utf-8") as f:
                f.write(reparsed.toprettyxml(indent="  "))

            QgsMessageLog.logMessage(f"Populated XML template for '{parser.get_name()}' and saved to {xml_output_path}.", level=Qgis.Info)
        except Exception as e:
            QgsMessageLog.logMessage(f"Error populating XML template for parser '{parser.get_name()}': {str(e)}", level=Qgis.Critical)

    def export_to_default_xml(self, xml_output_path, parser, root_name):
        """
        Exports data to a default XML format if no template is available.
        
        :param xml_output_path: Path to save the XML file.
        :param parser: Parser object containing qgis_mapping with data.
        :param root_name: The name of the root XML element.
        """
        try:
            root = ET.Element(f"IGEA_{root_name.upper()}")
            
            for feature_data in parser.get_data():
                feature_elem = ET.SubElement(root, f"{root_name.upper()}_JT")
                for qgis_field, xml_field in parser.qgis_mapping.items():
                    field_value = feature_data[xml_field]
                    if field_value in [None, "NULL", "nan"]:
                        field_elem = ET.SubElement(feature_elem, xml_field)
                    else:
                        field_elem = ET.SubElement(feature_elem, xml_field)
                        field_elem.text = str(field_value)
            
            # Prettify XML output
            rough_string = ET.tostring(root, 'utf-8-sig')
            reparsed = minidom.parseString(rough_string)
            with open(xml_output_path, "w", encoding="utf-8") as f:
                f.write(reparsed.toprettyxml(indent="  "))

            QgsMessageLog.logMessage(f"Exported default XML for '{parser.get_name()}' to {xml_output_path}.", level=Qgis.Info)
        except Exception as e:
            QgsMessageLog.logMessage(f"Error exporting default XML for parser '{parser.get_name()}': {str(e)}", level=Qgis.Critical)
            
    def process_layers(self):
        old_layers = self.layers
        
        if not self.processor:
            try:
                QgsMessageLog.logMessage("No processor found. Creating new processor.", "StalpiAssist", level=Qgis.Info)
                self.processor = SHPProcessor(self.layers)
            except Exception as e:
                QgsMessageLog.logMessage(f"Error creating processor: {str(e)}", "StalpiAssist", level=Qgis.Critical)
                return
        
        try:
            QgsMessageLog.logMessage("Getting current layers.", "StalpiAssist", level=Qgis.Info)
            current_layers = self.helper.get_layers()
        except Exception as e:
            QgsMessageLog.logMessage(f"Error getting current layers: {str(e)}", "StalpiAssist", level=Qgis.Critical)
            return
        
        if current_layers != old_layers:
            QgsMessageLog.logMessage("Layers have changed. Creating new processor.", "StalpiAssist", level=Qgis.Info)
            self.processor = None
            
            try:
                QgsMessageLog.logMessage("Creating new processor.", "StalpiAssist", level=Qgis.Info)
                self.processor = SHPProcessor(current_layers)
            except Exception as e:
                QgsMessageLog.logMessage(f"Error creating new processor: {str(e)}", "StalpiAssist", level=Qgis.Critical)
                return
        else:
            QgsMessageLog.logMessage("No changes in layers. Processor remains unchanged.", "StalpiAssist", level=Qgis.Info)
