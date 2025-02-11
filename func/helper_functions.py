import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import xlsxwriter
from qgis.core import QgsVectorLayer, QgsProject, QgsMessageLog, Qgis # type: ignore


class HelperBase:
    def __init__(self):
        super().__init__()
        self.processor = None
        
    # MARK: DEFAULT
    # Generate xml/xlsx files, replace blanks with apostrophes
    def generate_files(self, layers, base_dir):
        """
        Generates XML and XLSX files for the columns of given layers, skipping any column named 'fid'.
        Replaces blanks in column names with apostrophes.
        
        :param layers: List of QgsVectorLayer objects to process.
        :param base_dir: Directory where the files will be saved.
        """
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        
        for layer in layers:
            layer_name = layer.name()
            safe_layer_name = layer_name.replace(" ", "_")  # Replace spaces in layer name
            
            # XML file generation
            xml_path = os.path.join(base_dir, f"{safe_layer_name}.xml")
            root = ET.Element("Layer")
            root.set("name", layer_name)
            
            for field in layer.fields():
                if field.name().lower() != "fid":  # Skip 'fid'
                    field_elem = ET.SubElement(root, "Field")
                    field_name = field.name().replace(" ", "'")  # Replace blanks with apostrophes
                    field_elem.set("name", field_name)
                    field_elem.set("type", field.typeName())
            
            tree = ET.ElementTree(root)
            tree.write(xml_path, encoding="utf-8-sig", xml_declaration=True)
            
            # XLSX file generation
            xlsx_path = os.path.join(base_dir, f"{safe_layer_name}.xlsx")
            workbook = xlsxwriter.Workbook(xlsx_path)
            worksheet = workbook.add_worksheet()
            
            # Write header row
            headers = [field.name().replace(" ", "'") for field in layer.fields() if field.name().lower() != "fid"]
            for col_idx, header in enumerate(headers):
                worksheet.write(0, col_idx, header)
            
            # Write rows (data for illustration, can include actual feature data if needed)
            for row_idx, feature in enumerate(layer.getFeatures(), start=1):
                for col_idx, field in enumerate(layer.fields()):
                    if field.name().lower() != "fid":  # Skip 'fid'
                        value = feature[field.name()]
                        worksheet.write(row_idx, col_idx, value)
            
            workbook.close()

    # Create valid path and subdirectories if needed
    def create_valid_output(self, main_dir, filename, subdir=None):
        if subdir:
            full_path = os.path.join(main_dir, subdir)
        else:
            full_path = main_dir

        # Ensure directory exists
        os.makedirs(full_path, exist_ok=True)

        # Normalize path to avoid mix of \ and /
        valid_path = os.path.normpath(os.path.join(full_path, filename)).replace("\\", "/")
        
        return valid_path

    
    # Retrieve layers by name from the QGIS project
    def get_layers(self):
        '''
        Get layers by name from the QGIS project and add them to self.layers
        '''
        layers = {}
        layer_names = ['STALP_JT', 'NO_OFFSET_TRONSON_XML_', 'TRONSON_JT', 'BRANS_FIRI_GRPM_JT', 'FB pe C LES', 'FIRIDA_RETEA_JT', 'GRID_GEIOD', 'PTCZ_PTAB', 'TRONSON_XML_', 'TRONSON_ARANJARE', 'poze', 'FIRIDA_XML_', 'BRANSAMENT_XML_', 'GRUP_MASURA_XML_', 'STALP_XML_', 'DESCHIDERI_XML_', 'TRONSON_predare_xml', 'LINIE_MACHETA', 'STALPI_MACHETA', 'TRONSON_MACHETA', 'FIRIDA MACHETA', 'GRUP MASURA MACHETA', 'DESCHIDERI MACHETA', 'BRANSAMENTE MACHETA', 'LINIE_JT', "SCR_DWG"]
        
        # Get all layers in the current QGIS project (keep the layer objects)
        try:
            qgis_layers = QgsProject.instance().mapLayers().values()
            if not qgis_layers:
                raise ValueError("No layers found in the project.")
        except Exception as e:
            QgsMessageLog.logMessage(f"Error getting layers: {e}", "StalpiAssist", level=Qgis.Critical)
            return layers

        # Iterate through the actual layer objects
        for layer_name in layer_names:
            layer = next((l for l in qgis_layers if l.name() == layer_name), None)
            layers[layer_name] = layer  # Add the layer if found, else None

        return layers


    def add_layer_to_project(self, layer):
        try:
            if isinstance(layer, str):  # If layer is a file path
                layer_name = os.path.splitext(os.path.basename(layer))[0]
                merged_layer = QgsVectorLayer(layer, layer_name, 'ogr')
                
                if not merged_layer.isValid():
                    QgsMessageLog.logMessage(f"Invalid layer: {layer}", "StalpiAssist", level=Qgis.Critical)
                    return
                
                QgsProject.instance().addMapLayer(merged_layer)
            elif isinstance(layer, QgsVectorLayer):  # If layer is already a QgsVectorLayer object
                if not layer.isValid():
                    QgsMessageLog.logMessage("Invalid QgsVectorLayer object.", "StalpiAssist", level=Qgis.Critical)
                    return
                
                QgsProject.instance().addMapLayer(layer)
            else:
                raise TypeError("Invalid input type. Expected str or QgsVectorLayer.")
        except Exception as e:
            QgsMessageLog.logMessage(f"Error adding layer to project: {e}", "StalpiAssist", level=Qgis.Critical)

            
            
    def run_algorithm(self, algorithm, params, context, feedback, output_key):
        try:
            # Step 1: Run the algorithm
            results = algorithm.processAlgorithm(params, context, feedback)
            
            # Step 2: Retrieve the desired output path(s)
            output_path = results.get(output_key)
            
            if not output_path:
                QgsMessageLog.logMessage(f"Output not found for key: {output_key}", "StalpiAssist", level=Qgis.Warning)
                return False

            # Step 3: Add the output layer to the project
            self.add_layer_to_project(output_path)
            return True

        except Exception as e:
            QgsMessageLog.logMessage(f"Error processing and adding output: {e}", "StalpiAssist", level=Qgis.Critical)
            return False

# MARK: PARSERS
    def save_xml(self, xml_name, name, xml_file):
        root = ET.Element(xml_name) 

        for linie in self.linii:
            linie_element = ET.SubElement(root, name)
            for attr, value in linie.__dict__.items():
                child = ET.SubElement(linie_element, attr.upper())
                child.text = str(value) if value is not None else ""

        rough_string = ET.tostring(root, 'utf-8-sig')

        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="    ")

        with open(xml_file, 'w', encoding='utf-8-sig') as f:
            f.write(pretty_xml)
        
        
class SHPProcessor:
    '''
    Class to process the SHP layers, validate them and load them into QGIS
    '''
    def __init__(self, layers):
        '''
        Constructor for the SHPProcessor class
        :param layers: A dictionary with layer names and their respective QgsVectorLayer objects
        :param output_xlsx: The name of the output Excel file
        :return:
        '''
        self.layers = layers
        self.parsers = []
        self.invalid_elements = []
        self.load_layers()
    
    
    def load_layers(self):
        from .parsers.firida import IgeaFiridaParser
        from .parsers.bransament import IgeaBransamentParser
        from .parsers.linie import IgeaLinieParser
        from .parsers.tronson import IgeaTronsonParser
        from .parsers.deschidere import IgeaDeschidereParser
        from .parsers.stalp import IgeaStalpParser
        from .parsers.grup_masura import IgeaGrupMasuraParser
        
        """
        Load the SHP layers, parse them, and store the parsers in a list.
        :return: None
        """        
        for layer_name, layer in self.layers.items():
            # try:
            parser = None  # Initialize parser
            
            match layer_name.lower():
                case "linie_jt": 
                    parser = IgeaLinieParser(layer)
                case "stalp_xml_":
                    parser = IgeaStalpParser(layer)
                case "bransament_xml_":
                    parser = IgeaBransamentParser(layer)
                case "grup_masura_xml_":
                    parser = IgeaGrupMasuraParser(layer)
                case "deschideri_xml_":
                    parser = IgeaDeschidereParser(layer)
                case "firida_xml_":
                    parser = IgeaFiridaParser(layer)
                case "tronson_predare_xml":
                    parser = IgeaTronsonParser(layer)
                case _:
                    continue
            
            if parser is None:
                raise ValueError(f"No parser found for layer: {layer_name}")
            
            # Debugging: Ensure the layer data is loaded before parsing
            if not layer.isValid():
                raise ValueError(f"Layer '{layer_name}' is invalid or could not be loaded.")
            
            parser.parse()  # Parse the layer
            self.parsers.append(parser)  # Add the parser to the list
            
            # except ValueError as ve:
            #     QgsMessageLog.logMessage(f"ValueError processing layer '{layer_name}': {str(ve)}", "StalpiAssist", level=Qgis.Warning)
            # except AttributeError as ae:
            #     QgsMessageLog.logMessage(f"AttributeError processing layer '{layer_name}': {str(ae)}", "StalpiAssist", level=Qgis.Warning)
            # except Exception as e:
            #     QgsMessageLog.logMessage(f"Error processing layer '{layer_name}': {str(e)}", "StalpiAssist", level=Qgis.Critical)
        
        
        

