import os
import xml.etree.ElementTree as ET
import gc
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QProgressBar, QPushButton, QMessageBox # type: ignore
from xml.dom import minidom
from qgis.core import QgsProject, QgsMessageLog, Qgis  # type: ignore
from PyQt5.QtCore import QThread, pyqtSignal # type: ignore
from pathlib import Path # type: ignore
from .helper_functions import HelperBase
from .. import config

class GenerateXMLDialog(QDialog):
    
    def __init__(self, base_dir):
        super().__init__()
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
            qgis_layers = [
                QgsProject.instance().mapLayersByName('LINIE_JT'),
                QgsProject.instance().mapLayersByName('STALP_XML_'),
                QgsProject.instance().mapLayersByName('BRANSAMENT_XML_'),
                QgsProject.instance().mapLayersByName('GRUP_MASURA_XML_'),
                QgsProject.instance().mapLayersByName('FIRIDA_XML_'),
                QgsProject.instance().mapLayersByName('DESCHIDERI_XML_'),
                QgsProject.instance().mapLayersByName('TRONSON_predare_xml')
            ]

            column_mapping = {
                "LINIE_JT": ["CLASS_ID", "ID_BDI", "NR_CRT", "DENUM", "PROP", "CLASS_ID_LOC", "ID_LOC", "CLASS_ID_INST_SUP", "ID_INST_SUP", "COD_AD_ENERG", "NIV_TEN", "TIP_LIN",
                             "AN_PIF_INIT", "NR_IV"],
                "STALP_XML_": ["CLASS_ID", "ID_BDI", "NR_CRT", "ID_LINIE_JT_1", "NR_CRT_LINIE_JT_1", "ID_LINIE_JT_2", "NR_CRT_LINIE_JT_2", "ID_LINIE_JT_3", "NR_CRT_LINIE_JT_3", 
                               "ID_LINIE_JT_4", "NR_CRT_LINIE_JT_4", "ID_LINIE_JT_5", "NR_CRT_LINIE_JT_5", "ID_LINIE_JT_6", "NR_CRT_LINIE_JT_6", "ID_LINIE_JT_7", "NR_CRT_LINIE_JT_7", "DENUM", "NR_INS_STP", "DESC_DET", "PROP", "DET_PROP", "TIP_ZONA_AMP", "JUD", "PRIM", "LOC", "TIP_STR", "STR", "TIP_CIR", "TIP_MAT", "DESC_CTG_MT_JT", "NR_CIR", "UZURA_STP", "TIP_FUND", "OBS_FUND", "ANC", "OBS_ANC", "ADAOS", "OBS_ADAOS", "FIB_OPT", "NR_CIR_FO", "PROP_FO", "LTC", "NR_CIR_LTC", "PROP_LTC", "CATV", "NR_CIR_CATV", "PROP_CATV", "ECHIP_COM", "DISP_CUIB_PAS", "NR_CONS_C2S", "NR_CONS_C4S", "NR_CONS_C2T", "NR_CONS_C4T", "NR_CONS_C2BR", "NR_CONS_C4BR", "TIP_LEG_JT", "PRIZA_LEG_PAM", "CORP_IL", "CUTIE_SEL", "GEO", "LAT", "LONG", "ALT", "X_STEREO_70", "Y_STEREO_70", "Z_STEREO_70", "SURSA_COORD", "DATA_COORD", "OBS", "IMG_FILE_1", "IMG_FILE_2", "IMG_FILE_3", "IMG_FILE_4"],
                "TRONSON_predare_xml": ["CLASS_ID", "ID_BDI", "NR_CRT", "DENUM", "PROP", "CLASS_ID_LOC", "ID_LOC", "NR_CRT_LOC", "CLASS_ID_INC_TR", "ID_INC_TR", "NR_CRT_INC_TR", 
                                        "CLASS_ID_FIN_TR", "ID_FIN_TR", "NR_CRT_FIN_TR", "TIP_TR", "TIP_COND", "LUNG_TR", "GEO", "SURSA_COORD", "DATA_COORD", "UNIT_LOG_INT", "S_UNIT_LOG", "POST_LUC", "OBS"],
                "GRUP_MASURA_XML_": ["CLASS_ID", "ID_BDI", "NR_CRT", "DENUM", "CLASS_ID_LOC", "ID_LOC", "NR_CRT_LOC", "CLASS_ID_INST_SUP", "ID_INST_SUP", "NR_CRT_INST_SUP", "JUD", "PRIM", 
                                     "LOC", "TIP_STR", "STR", "NR_SCARA", "ETAJ", "AP"],
                "FIRIDA_XML_": ["CLASS_ID", "ID_BDI", "NR_CRT", "IDEN", "CLASS_ID_LOC", "ID_LOC", "NR_CRT_LOC", "CLASS_ID_INST_SUP", "ID_INST_SUP", "NR_CRT_INST_SUP", "JUD", "PRIM", "LOC", 
                                "TIP_STR", "STR", "NR", "ETAJ", "ROL_FIRI", "TIP_FIRI_RET", "TIP_FIRI_BR", "AMPL", "MAT", "LIM_PROP", "DEF_FIRI", "NR_CIR", "AN_FUNC", "ALT", "GEO", "SURSA_COORD", "DATA_COORD", "LONG", "LAT", "X_STEREO_70", "Y_STEREO_70", "Z_STEREO_70"],
                "DESCHIDERI_XML_": ["CLASS_ID", "ID_BDI", "NR_CRT", "DENUM", "ID_STP_INC", "NR_CRT_STP_INC", "ID_STP_TERM", "NR_CRT_STP_TERM", "ID_TR_JT1", "NR_CRT_TR_JT1", "ID_TR_JT2", 
                                    "NR_CRT_TR_JT2", "ID_TR_JT3", "NR_CRT_TR_JT3", "ID_TR_JT4", "NR_CRT_TR_JT4", "ID_TR_JT5", "NR_CRT_TR_JT5", "ID_TR_JT6", "NR_CRT_TR_JT6", "GEO", "LUNG", "SURSA_COORD", "DATA_COORD"],
                "BRANSAMENT_XML_": ["ID_BDI", "NR_CRT", "DENUM", "CLASS_ID_LOC", "ID_LOC", "NR_CRT_LOC", "CLASS_ID_PLC_BR", "ID_PLC_BR", "NR_CRT_PLC_BR", "TIP_BR", "TIP_COND", "LUNG", "JUD", "PRIM", "LOC", "TIP_STR", "STR", "NR_IMOB", "GEO", "SURSA_COORD", "DATA_COORD", "OBS"]
            }

            for i, layer_group in enumerate(qgis_layers):
                if not layer_group:
                    raise ValueError(f"Layer group index {i} is empty or does not exist.")

                for layer in layer_group:
                    layer_name = layer.name()
                    required_columns = column_mapping.get(layer_name, [])

                    if not required_columns:
                        raise ValueError(f"No column mapping found for layer '{layer_name}'")

                    layer_columns = [field.name() for field in layer.fields()]
                    missing_columns = [col for col in required_columns if col not in layer_columns]

                    if missing_columns:
                        raise ValueError(f"Layer '{layer_name}' is missing required columns: {missing_columns}")

            self.progress_bar.setMaximum(len(qgis_layers))
            self.progress_bar.setValue(0)

            self.worker_thread = GenerateXMLWorker(self.base_dir, self.template_path, qgis_layers)
            self.worker_thread.progress_updated.connect(self.progress_bar.setValue)
            self.worker_thread.finished.connect(self.on_generation_complete)
            self.worker_thread.start()

        except IndexError as e:
            QgsMessageLog.logMessage(f"Error accessing layers: {str(e)}", "StalpiAssist", level=Qgis.Critical)
            QMessageBox.critical(self, "Error", f"Could not find one or more layers. Please check layer names.")
        except Exception as e:
            QgsMessageLog.logMessage(f"Unexpected error: {str(e)}", "StalpiAssist", level=Qgis.Critical)
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def on_generation_complete(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Complete")
        msg_box.setText("File generation completed!")
        msg_box.setStandardButtons(QMessageBox.Ok)

        if msg_box.exec_() == QMessageBox.Ok:
            self.close()

class GenerateXMLWorker(QThread):
    progress_updated = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, base_dir, template_path, layers):
        super().__init__()
        self.base_dir = base_dir
        self.helper = HelperBase()
        self.template_path = template_path
        self.layers = layers

    def run(self):
        self.generate_xml()
        self.finished.emit()

    @staticmethod
    def plugin_path(*args) -> Path:
        path = Path(__file__).resolve().parent
        for item in args:
            path = path.joinpath(item)
        return path

    def generate_xml(self):
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

        for layer_group in self.layers:
            if not layer_group:
                continue

            for layer in layer_group:
                try:
                    layer_name = layer.name()
                    safe_layer_name = file_name_mapping.get(layer_name, layer_name)

                    xml_template_path = self.plugin_path(f"templates/{safe_layer_name}.xml")
                    xml_path = self.helper.create_valid_output(self.base_dir, f"{safe_layer_name}.xml", "xml")

                    if xml_template_path.exists():
                        self.populate_xml_template(xml_template_path, xml_path, layer)
                    else:
                        self.export_to_default_xml(xml_path, layer, safe_layer_name)

                    progress += 1
                    self.progress_updated.emit(progress)

                    gc.collect()
                except Exception as e:
                    QgsMessageLog.logMessage(f"Error processing layer '{layer.name()}': {str(e)}", "StalpiAssist", level=Qgis.Critical)

    def populate_xml_template(self, xml_template_path, xml_output_path, layer):
        try:
            tree = ET.parse(xml_template_path)
            root = tree.getroot()

            repeating_element_tag = list(root)[0].tag
            parent = root

            for child in root.findall(repeating_element_tag):
                parent.remove(child)

            sorted_features = sorted(
                layer.getFeatures(),
                key=lambda f: f["NR_CRT"] if f["NR_CRT"] not in config.NULL_VALUES else float("inf")
            )
            
            required_deschidere_length = {
                "CLASS_ID": 4,
                "ID_BDI": 8,
                "NR_CRT": 8,
                "DENUM": 50,
                "ID_STP_INC": 8,
                "NR_CRT_STP_INC": 8,
                "ID_STP_TERM": 8,
                "NR_CRT_STP_TERM": 8,
                "ID_TR_JT1": 8,
                "NR_CRT_TR_JT1": 8,
                "ID_TR_JT2": 8,
                "NR_CRT_TR_JT2": 8,
                "ID_TR_JT3": 8,
                "NR_CRT_TR_JT3": 8,
                "ID_TR_JT4": 8,
                "NR_CRT_TR_JT4": 8,
                "ID_TR_JT5": 8,
                "NR_CRT_TR_JT5": 8,
                "ID_TR_JT6": 8,
                "NR_CRT_TR_JT6": 8,
                "GEO": 4000,
                "SURSA_COORD": 30,
            }
            
            required_tronson_length = {
                "CLASS_ID": 4,
                "ID_BDI": 8,
                "NR_CRT": 8,
                "DENUM": 50,
                "CLASS_ID_LOC": 4,
                "ID_LOC": 8,
                "NR_CRT_LOC": 8,
                "CLASS_ID_INC_TR": 4,
                "ID_INC_TR": 8,
                "NR_CRT_INC_TR": 8,
                "CLASS_ID_FIN_TR": 4,
                "ID_FIN_TR": 8,
                "NR_CRT_FIN_TR": 8,
                "TIP_TR": 30,
                "TIP_COND": 60,
                "GEO": 4000,
                "SURSA_COORD": 30,
                "UNIT_LOG_INT": 30,
                "S_UNIT_LOG": 30,
                "POST_LUC": 50,
                "OBS": 200
            }
            
            required_firida_length = {
                "CLASS_ID": 4,
                "ID_BDI": 8,
                "NR_CRT": 8,
                "IDEN": 50,
                "CLASS_ID_LOC": 4,
                "ID_LOC": 8,
                "NR_CRT_LOC": 8,
                "CLASS_ID_INST_SUP": 4,
                "ID_INST_SUP": 8,
                "NR_CRT_INST_SUP": 8,
                "JUD": 30,
                "PRIM": 30,
                "LOC": 30,
                "TIP_STR": 30,
                "STR": 60,
                "NR": 10,
                "ETAJ": 10,
                "ROL_FIRI": 30,
                "TIP_FIRI_RET": 30,
                "TIP_FIRI_BR": 30,
                "AMPL": 30,
                "MAT": 30,
                "LIM_PROP": 30,
                "DEF_FIRI": 30,
                "NR_CIR": 30,
                "AN_FUNC": 4,
                "GEO": 4000,
                "SURSA_COORD": 30
            }
            
            required_bransament_length = {
                "CLASS_ID": 4,
                "ID_BDI": 8,
                "NR_CRT": 8,
                "DENUM": 100,
                "CLASS_ID_LOC": 4,
                "ID_LOC": 8,
                "NR_CRT_LOC": 8,
                "CLASS_ID_PLC_BR": 8,
                "ID_PLC_BR": 8,
                "NR_CRT_PLC_BR": 4,
                "TIP_BR": 30,
                "TIP_COND": 60,
                "LUNG": 8,
                "JUD": 30,
                "PRIM": 30,
                "LOC": 30,
                "TIP_STR": 30,
                "STR": 60,
                "NR_IMOB": 10,
                "GEO": 4000,
                "SURSA_COORD": 30,
                "OBS": 200
            }

            
            required_grup_masura_length = {
                "CLASS_ID": 4,
                "ID_BDI": 8,
                "NR_CRT": 8,
                "DENUM": 50,
                "CLASS_ID_LOC": 4,
                "ID_LOC": 8,
                "NR_CRT_LOC": 8,
                "CLASS_ID_INST_SUP": 4,
                "ID_INST_SUP": 8,
                "NR_CRT_INST_SUP": 8,
                "JUD": 30,
                "PRIM": 30,
                "LOC": 30,
                "TIP_STR": 30,
                "STR": 60,
                "NR_SCARA": 8,
                "ETAJ": 10,
                "AP": 3
            }
            
            required_stalp_length = {
                "CLASS_ID": 4,
                "ID_BDI": 8,
                "NR_CRT": 8,
                "ID_LINIE_JT_1": 8,
                "NR_CRT_LINIE_JT_1": 8,
                "ID_LINIE_JT_2": 8,
                "NR_CRT_LINIE_JT_2": 8,
                "ID_LINIE_JT_3": 8,
                "NR_CRT_LINIE_JT_3": 8,
                "ID_LINIE_JT_4": 8,
                "NR_CRT_LINIE_JT_4": 8,
                "ID_LINIE_JT_5": 8,
                "NR_CRT_LINIE_JT_5": 8,
                "ID_LINIE_JT_6": 8,
                "NR_CRT_LINIE_JT_6": 8,
                "DENUM": 85,
                "NR_INS_STP": 30,
                "DESC_DET": 250,
                "PROP": 40,
                "DET_PROP": 60,
                "TIP_ZONA_AMP": 30,
                "JUD": 30,
                "PRIM": 30,
                "LOC": 30,
                "TIP_STR": 30,
                "STR": 60,
                "TIP_CIR": 30,
                "TIP_MAT": 30,
                "DESC_CTG_MT_JT": 30,
                "NR_CIR": 30,
                "UZURA_STP": 60,
                "TIP_FUND": 30,
                "OBS_FUND": 60,
                "ANC": 30,
                "OBS_ANC": 60,
                "ADAOS": 30,
                "OBS_ADAOS": 60,
                "FIB_OPT": 30,
                "NR_CIR_FO": 2,
                "PROP_FO": 30,
                "LTC": 30,
                "NR_CIR_LTC": 2,
                "PROP_LTC": 30,
                "CATV": 30,
                "NR_CIR_CATV": 2,
                "PROP_CATV": 30,
                "ECHIP_COM": 30,
                "DISP_CUIB_PAS": 30,
                "NR_CONS_C2S": 2,
                "NR_CONS_C4S": 2,
                "NR_CONS_C2T": 2,
                "NR_CONS_C4T": 2,
                "NR_CONS_C2BR": 2,
                "NR_CONS_C4BR": 2,
                "TIP_LEG_JT": 30,
                "PRIZA_LEG_PAM": 30,
                "CORP_IL": 30,
                "CUTIE_SEL": 30,
                "GEO": 4000,
                "SURSA_COORD": 30,
                "IMG_FILE_1": 400,
                "IMG_FILE_2": 400,
                "IMG_FILE_3": 400,
                "IMG_FILE_4": 400
            }

            
            required_linie_jt_length = {
                "CLASS_ID": 4,
                "ID_BDI": 8,
                "NR_CRT": 8,
                "DENUM": 40,
                "PROP": 40,
                "CLASS_ID_LOC": 4,
                "ID_LOC": 8,
                "CLASS_ID_INST_SUP": 4,
                "ID_INST_SUP": 8,
                "COD_AD_ENERG": 3,
                "NIV_TEN": 3,
                "TIP_LIN": 10,
                "AN_PIF_INIT": 4,
                "NR_IV": 25
            }
            
            for feature in sorted_features:
                new_element = ET.Element(repeating_element_tag)
                for field in layer.fields():
                    field_value = feature[field.name()]
                    if field.name() == "fid" or field.name().startswith("new_name"):
                        continue
                    
                    if str(xml_template_path).endswith("deschidere.xml"):
                        field_value = str(field_value)[:required_deschidere_length[field.name()]] if field.name() in required_deschidere_length else field_value
                    
                    if str(xml_template_path).endswith("tronson_jt.xml"):
                        field_value = str(field_value)[:required_tronson_length[field.name()]] if field.name() in required_tronson_length else field_value
                    
                    if str(xml_template_path).endswith("firida.xml"):
                        # complete the logic for firida.xml
                        fr_iden = self.helper.get_fr_iden(feature, True)
                        if field.name() == "IDEN":
                            field_value = fr_iden['correct']
                        if field.name() == "NR":
                            field_value = fr_iden['nr']
                        if field.name() == "STR":
                            field_value = fr_iden['first_str']
                            
                        # cut field to required length
                        field_value = str(field_value)[:required_firida_length[field.name()]] if field.name() in required_firida_length else field_value
                            
                    if str(xml_template_path).endswith("bransament.xml"):
                        # complete the logic for bransament.xml
                        br_denum = self.helper.get_fr_iden(feature, False)
                        if field.name() == "DENUM":
                            field_value = br_denum['correct']
                        if field.name() == "NR_IMOB":
                            field_value = br_denum['nr']
                        if field.name() == "STR":
                            field_value = br_denum['first_str']
                            
                        # cut field to required length
                        field_value = str(field_value)[:required_bransament_length[field.name()]] if field.name() in required_bransament_length else field_value
                            
                    if str(xml_template_path).endswith("grup_masura.xml"):
                        # complete the logic for grup_masura.xml
                        correct_denum = self.helper.get_correct_denum(feature)
                        if field.name() == "DENUM":
                            field_value = correct_denum['denum']
                        if field.name() == "NR_SCARA":
                            field_value = correct_denum['nr_scara']
                        if field.name() == "STR":
                            field_value = correct_denum['str']
                            
                        # cut field to required length
                        field_value = str(field_value)[:required_grup_masura_length[field.name()]] if field.name() in required_grup_masura_length else field_value
                            
                    if str(xml_template_path).endswith("stalp.xml"):
                        # complete the logic for stalp.xml
                        if field.name() == "NR_CIR":
                            if isinstance(field_value, str) and field_value.isdigit() and int(field_value) > 2:
                                field_value = f"{field_value} circuite"
                        if field.name() == "TIP_MAT":
                            if feature["DESC_CTG_MT_JT"] in ["SV 10001", "SV 10002", "SV 15011"]:
                                field_value = "Beton"
                            elif "St. metalic" in feature["DESC_CTG_MT_JT"]:
                                field_value = "Metal"
                            elif "St. lemn" in feature["DESC_CTG_MT_JT"]:
                                field_value = "Lemn"
                            elif "Portal" in feature["DESC_CTG_MT_JT"]:
                                field_value = "Portal"
                        if field.name() == "UZURA_STP":
                            field_value = "5"
                        if field.name() == "PROP_CATV" or field.name() == "PROP_LTC":
                            field_value = "0"
                        if field.name() == "ADAOS":
                            if field_value.lower() in ["lemn", "metal", "beton"]:
                                field_value = "Da"
                                
                        # cut field to required length
                        field_value = str(field_value)[:required_stalp_length[field.name()]] if field.name() in required_stalp_length else field_value

                    if str(xml_template_path).endswith("linie_jt.xml"):
                        # complete the logic for linie_jt.xml
                        if field.name() == "DENUM":
                            field_value = ''
                            
                        # cut field to required length
                        field_value = str(field_value)[:required_linie_jt_length[field.name()]] if field.name() in required_linie_jt_length else field_value
                        
                    child_element = ET.SubElement(new_element, field.name())
                    if str(field_value) not in config.NULL_VALUES:
                        child_element.text = str(field_value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    else:
                        child_element.text = ""
                parent.append(new_element)

            rough_string = ET.tostring(root, 'utf-8')
            reparsed = minidom.parseString(rough_string.decode("utf-8"))
            with open(xml_output_path, "w", encoding="utf-8") as f:
                f.write(reparsed.toprettyxml(indent="  "))

        except Exception as e:
            QgsMessageLog.logMessage(f"Error populating XML template for layer '{layer.name()}': {str(e)}", "StalpiAssist", level=Qgis.Critical)

    def export_to_default_xml(self, xml_output_path, layer, root_name):
        try:
            root = ET.Element(f"IGEA_{root_name.upper()}")

            for feature in layer.getFeatures():
                feature_elem = ET.SubElement(root, f"{root_name.upper()}_JT")
                for field in layer.fields():
                    field_value = feature[field.name()]
                    field_elem = ET.SubElement(feature_elem, field.name())
                    if field_value not in config.NULL_VALUES:
                        field_elem.text = str(field_value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

            rough_string = ET.tostring(root, 'utf-8')
            reparsed = minidom.parseString(rough_string.decode("utf-8"))
            with open(xml_output_path, "w", encoding="utf-8") as f:
                f.write(reparsed.toprettyxml(indent="  "))

        except Exception as e:
            QgsMessageLog.logMessage(f"Error exporting default XML for layer '{layer.name()}': {str(e)}", "StalpiAssist", level=Qgis.Critical)