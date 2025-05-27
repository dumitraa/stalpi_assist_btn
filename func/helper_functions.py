import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import xlsxwriter # type: ignore
from PyQt5.QtCore import QVariant # type: ignore
from qgis.core import QgsVectorLayer, QgsProject, QgsMessageLog, Qgis, QgsFeature, QgsFields, QgsField # type: ignore
from PyQt5.QtWidgets import QMessageBox # type: ignore
from .. import config
import pandas as pd
from pathlib import Path


class HelperBase:
    def __init__(self):
        super().__init__()
        self.processor = None
        
        
    @staticmethod
    def plugin_path(*args) -> Path:
        """ Return the path to the plugin root folder or file. """
        path = Path(__file__).resolve().parent
        for item in args:
            path = path.joinpath(item)
        return path
    
    def get_pt_name(self):
        linie_jt = QgsProject.instance().mapLayersByName("LINIE_JT")
        if not linie_jt:
            return ""
        
        linie_jt = linie_jt[0]
        first_feature = next(linie_jt.getFeatures())
        
        return self.get_descriere(first_feature)
        
    def load_lookup_values(self, xlsx_path):
        """
        Loads values from the given Excel file and returns a set of lookup values.
        """
        if not os.path.exists(xlsx_path):
            QgsMessageLog.logMessage(f"File not found: {xlsx_path}", "StalpiAssist", level=Qgis.Critical)
            return set()

        try:
            df = pd.read_excel(xlsx_path, usecols=[0], dtype=str)
            return set(df.iloc[:, 0].dropna().str.strip())
        except Exception as e:
            QgsMessageLog.logMessage(f"Error loading Excel file: {e}", "StalpiAssist", level=Qgis.Critical)
            return set()

    def get_descriere(self, feature):
        """
        Extracts the matching substring from feature["DENUM"] if it exists in the lookup values.
        """
        denum_value = str(feature["DENUM"]).replace("_", " ")
        if not denum_value:
            return None

        # Ensure lookup values are loaded once and cached
        if not hasattr(self, '_lookup_values'):
            xlsx_path = self.plugin_path('templates', 'pt.xlsx')
            self._lookup_values = self.load_lookup_values(xlsx_path)

        # Check for matches in the lookup set
        for lookup in self._lookup_values:
            if lookup.replace("_", " ") in denum_value:
                return lookup  # Return first found match

        QMessageBox.critical(None, "Avertizare", f"Nu a fost gasit niciun match pentru valoarea '{denum_value}' S-a folosit denumirea proiectului")
        project_name = self.get_project_name()
        
        return project_name  # No match found
    
    # MARK: DEFAULT
    def get_project_name(self):
        project = QgsProject.instance()
        if project.fileName():
            return os.path.splitext(os.path.basename(project.fileName()))[0]
        
        QMessageBox.critical(None, "Eroare", "Proiectul nu este salvat!")
        return ""
    
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
    
    def resolve_mapping(self, parser, mapping):
        if isinstance(mapping, tuple):
            parts = [
                self.n(str(getattr(parser, element, ""))) if hasattr(parser, element) else self.n(str(element))
                for element in mapping
            ]
            return self.n(" ".join(filter(None, parts)))
        
        elif callable(mapping):
            return mapping(parser)
        return self.n(str(getattr(parser, mapping, ""))) if mapping else ""

    
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
    
    def n(self, value):
        '''
        normalize the value by removing extra spaces and newlines
        '''
        return value.replace("\n", " ").replace("\r", " ")
    
    def create_scratch_layer(self, name, geom_type):
        crs = "EPSG:3844"
        if geom_type == "Point":
            uri = f"Point?crs={crs}"
        elif geom_type == "LineString":
            uri = f"LineString?crs={crs}"
        else:
            uri = f"None?crs={crs}"

        layer = QgsVectorLayer(uri, name, "memory")
        provider = layer.dataProvider()

        fields = QgsFields()
        fields.append(QgsField("nume_layer", QVariant.String))  
        fields.append(QgsField("coloane", QVariant.String))     
        fields.append(QgsField("feature_id", QVariant.Int))
        provider.addAttributes(fields)
        layer.updateFields()
        return layer

    def check_obligatory_fields(self):
        layers_to_check = {
            "STALP_JT": [
                "DENUM", "NR_INS_STP", "PROP", "JUD", "PRIM", "LOC", "TIP_STR", "STR",
                "TIP_CIR", "DESC_CTG_MT_JT", "NR_CIR", "TIP_FUND", 
                "ADAOS", "TIP_LEG_JT", "fid"],
            "BRANS_FIRI_GRPM_JT": [
                "fid", "TIP_BR", "TIP_COND", "JUD", "PRIM", "LOC", "TIP_STR", "STR", 
                "NR_IMOB", "TIP_FIRI_BR", "LINIA_JT"],
            "TRONSON_JT": [
                "TIP_TR", "TIP_COND", "fid", "LINIA_JT"],
            "FB pe C LES": [
                "fid", "TIP_BR", "TIP_COND", "JUD", "PRIM", "LOC", "TIP_STR", 
                "STR", "NR_IMOB", "TIP_FIRI_BR", "LINIA_JT"],
            "LINIE_JT": [
                "ID_BDI", "DENUM"]
        }

        layer_types = {
            "STALP_JT": "Point",
            "FB pe C LES": "Point",
            "TRONSON_JT": "LineString",
            "BRANS_FIRI_GRPM_JT": "LineString",
            "LINIE_JT": "None"
        }
        
        is_valid = True

        created_layers = {}

        for layer_name, columns in layers_to_check.items():
            layers = QgsProject.instance().mapLayersByName(layer_name)
            if not layers:
                continue

            layer = layers[0]
            geom_type = layer_types[layer_name]

            scratch_layer = None
            for feature in layer.getFeatures():
                incomplete_columns = set()          
                for column in columns:
                    if column not in [field.name() for field in layer.fields()]:
                        continue
                    value = feature[column]
                    if value in config.NULL_VALUES:
                        incomplete_columns.add(column)
                        
                if layer_name == "STALP_JT":
                    nr_cir_fo_val = feature['NR_CIR_FO']
                    prop_fo_val = feature['PROP_FO']
                    
                    if nr_cir_fo_val not in config.NULL_VALUES and prop_fo_val in config.NULL_VALUES:
                        incomplete_columns.add('PROP_FO (NR_CIR_FO e completat)')
                        
                if incomplete_columns:
                    is_valid = False
                    if not scratch_layer:
                        scratch_layer = self.create_scratch_layer(f"{layer_name}_coloane_necompletate", geom_type)
                        created_layers[layer_name] = scratch_layer

                    new_feature = QgsFeature(scratch_layer.fields())
                    new_feature.setAttributes([
                        layer_name,                         
                        ", ".join(incomplete_columns),     
                        feature.id()                            
                    ])
                    if geom_type != "None":
                        geometry = feature.geometry()
                        if geometry and geometry.isGeosValid():
                            new_feature.setGeometry(geometry)
                            
                    scratch_layer.dataProvider().addFeature(new_feature)

        for name, layer in created_layers.items():
            QgsProject.instance().addMapLayer(layer)
     
        return is_valid

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
                QgsMessageLog.logMessage(f"Output not found for key: {output_key}", "StalpiAssist", level=Qgis.Critical)
                return False

            # Step 3: Add the output layer to the project
            self.add_layer_to_project(output_path)
            return True

        except Exception as e:
            QgsMessageLog.logMessage(f"Error processing and adding output: {e}", "StalpiAssist", level=Qgis.Critical)
            return False
        
    def get_fr_iden(self, feature, is_firida):
        
        street = feature['STR']
        number = feature['NR'] if is_firida else feature["NR_IMOB"]
            
        first_num = self.n(number).split(",")[0] if "," in number else number
        first_str = self.n(street).split(",")[0] if "," in street else street
        
        full_str = street + " " + number
        short_str = first_str + " " + first_num
        nr = first_num
        
        return {'initial': full_str, 'correct': short_str, 'nr': nr, 'first_str': first_str}
        
    def get_correct_denum(self, feature):
        denum_to_match = feature["DENUM"]
        nr_crt_to_match = feature["NR_CRT"]
        str_value = self.n(feature["STR"]).split(",")[0] if "," in feature["STR"] else feature["STR"]
        str_full = feature["STR"]
        nr_scara = feature["NR_SCARA"]
        short_denum = f"{str_full.split(',')[0] if ',' in str_full else str_full} {nr_scara.split(',')[0] if ',' in nr_scara else nr_scara}"

        # If NR_SCARA is a string without commas, return DENUM immediately
        if isinstance(nr_scara, str) and "," not in nr_scara:
            return {
                'denum': denum_to_match,
                'short_denum': short_denum,
                'nr_scara': nr_scara,
                'str': str_value
            }

        # Get the layer
        layer_list = QgsProject.instance().mapLayersByName("GRUP_MASURA_XML_")
        if not layer_list:
            QgsMessageLog.logMessage("Layer GRUP_MASURA_XML_ not found!", "StalpiAssist", level=Qgis.Critical)
            return {
                'denum': denum_to_match,
                'short_denum': short_denum,
                'nr_scara': nr_scara,
                'str': str_value
            }

        gr_layer = layer_list[0]  # Extract first matched layer

        # Extract all relevant features from layer
        matching_features = [f for f in gr_layer.getFeatures() if f["DENUM"] == denum_to_match]

        if not matching_features:
            return {
                'denum': denum_to_match,
                'short_denum': short_denum,
                'nr_scara': nr_scara,
                'str': str_value
            }

        # Sort matching features by NR_CRT (handling NULLs safely)
        matching_features.sort(key=lambda f: (f["NR_CRT"] if f["NR_CRT"] not in config.NULL_VALUES else float("inf")))

        # Find the index of our feature in the sorted list
        try:
            index = next(i for i, f in enumerate(matching_features) if f["NR_CRT"] == nr_crt_to_match)
        except StopIteration:
            QgsMessageLog.logMessage(f"NR_CRT={nr_crt_to_match} not found in sorted features.", "StalpiAssist", level=Qgis.Critical)
            return {
                'denum': denum_to_match,
                'short_denum': short_denum,
                'nr_scara': nr_scara,
                'str': str_value
            }
        except Exception as e:
            QgsMessageLog.logMessage(f"Error finding index: {e}", "StalpiAssist", level=Qgis.Critical)
            return {
                'denum': denum_to_match,
                'short_denum': short_denum,
                'nr_scara': nr_scara,
                'str': str_value
            }

        # Extract NR_SCARA values and ensure they are properly indexed
        nr_scara_list = [f["NR_SCARA"] for f in matching_features]
        
        if len(nr_scara_list) > index:
            correct_nr_scara = nr_scara_list[index]
        else:
            correct_nr_scara = nr_scara_list[0]  # Fallback if index is out of range

        # Handle cases where NR_SCARA is a comma-separated string
        if isinstance(correct_nr_scara, str) and "," in correct_nr_scara:
            scara_values = correct_nr_scara.split(",")
            
            if len(self.n(str_full).split(",")) == len(scara_values):
                str_parts = [self.n(part) for part in self.n(str_full).split(",")]
                str_value = str_parts[index] if index < len(str_parts) else str_parts[0]
                correct_nr_scara = scara_values[index] if index < len(scara_values) else scara_values[0]
            else:
                correct_nr_scara = scara_values[index] if index < len(scara_values) else scara_values[0]  # Get nth index or fallback to first

        return {
            'denum': self.n(f"{str_value} {correct_nr_scara}"),
            'short_denum': short_denum,
            'nr_scara': correct_nr_scara,
            'str': str_value
        } 
        
    def replace_empty_values(self):
        '''
        replaces all empty values ('') with "NULL" from all fields
        '''
        layers = ["STALP_JT", "BRANS_FIRI_GRPM_JT", "FB pe C LES", "TRONSON_JT"]
        
        for layer_name in layers:
            layer = QgsProject.instance().mapLayersByName(layer_name)[0]
            if not layer:
                continue

            updates = {}
            for feature in layer.getFeatures():
                attrs = {}
                for field in layer.fields():
                    idx = layer.fields().indexOf(field.name())
                    if idx == -1:
                        continue

                    original_value = feature[field.name()]
                    if original_value == '' or original_value == "NUL":
                        attrs[idx] = None
                if attrs:
                    updates[feature.id()] = attrs

            layer.startEditing()
            layer.dataProvider().changeAttributeValues(updates)
            layer.commitChanges()
            
    def delete_id_bdi(self):
        layers = ["STALP_JT", "BRANS_FIRI_GRPM_JT", "FB pe C LES", "TRONSON_JT"]
        
        for layer_name in layers:
            layer = QgsProject.instance().mapLayersByName(layer_name)[0]
            if not layer:
                continue

            updates = {}
            for feature in layer.getFeatures():
                attrs = {}
                for field in layer.fields():
                    idx = layer.fields().indexOf(field.name())
                    if idx == -1:
                        continue

                    if field.name() == "ID_BDI":
                        attrs[idx] = None
                if attrs:
                    updates[feature.id()] = attrs

            layer.startEditing()
            layer.dataProvider().changeAttributeValues(updates)
            layer.commitChanges()
        
    def remove_diacritics(self):
        layers = ["STALP_JT", "BRANS_FIRI_GRPM_JT", "FB pe C LES"]
        fields = ["JUD", "PRIM", "LOC", "STR"]
            
        diacritics_map = {
            'ă': 'a', 'Ă': 'A',
            'â': 'a', 'Â': 'A',
            'î': 'i', 'Î': 'I',
            'ș': 's', 'Ș': 'S',
            'ț': 't', 'Ț': 'T'
        }

        # Helper function for replacing diacritics
        def replace_diacritics(text):
            for diacritic, replacement in diacritics_map.items():
                text = text.replace(diacritic, replacement).upper()
            return text

        # Iterate through each layer name
        for layer_name in layers:
            layer = QgsProject.instance().mapLayersByName(layer_name)[0]
            if not layer:
                continue

            updates = {}
            for feature in layer.getFeatures():
                attrs = {}
                for field in fields:
                    idx = layer.fields().indexOf(field)
                    if idx == -1:
                        continue

                    original_value = feature[field]
                    if original_value and isinstance(original_value, str):
                        cleaned_value = replace_diacritics(original_value)
                        attrs[idx] = cleaned_value
                if attrs:
                    updates[feature.id()] = attrs

            # Commit updates in batch (efficient method)
            layer.startEditing()
            layer.dataProvider().changeAttributeValues(updates)
            layer.commitChanges()


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
            try:
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
            
            except ValueError as ve:
                QgsMessageLog.logMessage(f"ValueError processing layer '{layer_name}': {str(ve)}", "StalpiAssist", level=Qgis.Critical)
            except AttributeError as ae:
                QgsMessageLog.logMessage(f"AttributeError processing layer '{layer_name}': {str(ae)}", "StalpiAssist", level=Qgis.Critical)
            except Exception as e:
                QgsMessageLog.logMessage(f"Error processing layer '{layer_name}': {str(e)}", "StalpiAssist", level=Qgis.Critical)
        
        
        

