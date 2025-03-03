from typing import List
from openpyxl import load_workbook
from ... import config
from qgis.core import QgsMessageLog, Qgis, QgsProject # type: ignore


class GrupMasuraJT:
    def __init__(self, id, class_id, id_bdi, nr_crt, denum, class_id_loc, id_loc, nr_crt_loc, class_id_inst_sup, id_inst_sup, nr_crt_inst_sup, jud, prim, loc, tip_str, str, nr_scara, etaj, ap):
        self.id = id
        self.class_id = class_id
        self.id_bdi = id_bdi
        self.nr_crt = nr_crt
        self.denum = denum
        self.class_id_loc = class_id_loc
        self.id_loc = id_loc
        self.nr_crt_loc = nr_crt_loc
        self.class_id_inst_sup = class_id_inst_sup
        self.id_inst_sup = id_inst_sup
        self.nr_crt_inst_sup = nr_crt_inst_sup
        self.jud = jud
        self.prim = prim
        self.loc = loc
        self.tip_str = tip_str
        self.str = str
        self.nr_scara = nr_scara
        self.etaj = etaj
        self.ap = ap

    def __repr__(self):
        return f"GrupMasuraJT(denum={self.denum})"


class IgeaGrupMasuraParser:
    def __init__(self, vector_layer):
        self.vector_layer = vector_layer
        self.grupuri: List[GrupMasuraJT] = []
        

        self.mapping = {
            "Nr.crt": "nr_crt",
            "Denumire": "denum",
            "Descrierea BDI": lambda gr: f"GRUP MASURA {gr.denum['correct']}",
            "Nr.crt_Locatia": "nr_crt_loc",
            "Locatia": lambda gr: f"FB {gr.denum['initial']}",
            "ID_Descrierea instalatiei uperioare": "class_id_inst_sup",
            "Descrierea instalatiei uperioare": "nr_crt_inst_sup",
            "Judet": "jud",
            "Primarie": "prim",
            "Localitate": "loc",
            "Tip strada": "tip_str",
            "Strada": "str",
            "nr./ scara": lambda gr: gr.denum['nr'],
            "Etaj": "etaj",
            "Apartament": "ap"
        }
        
        # self.qgis_mapping = ["CLASS_ID", "ID_BDI", "NR_CRT", "DENUM", "CLASS_ID_LOC", "ID_LOC", "NR_CRT_LOC", "CLASS_ID_INST_SUP", "ID_INST_SUP", "NR_CRT_INST_SUP", "JUD", "PRIM", "LOC", "TIP_STR", "STR", "NR_SCARA", "ETAJ", "AP"]
            
    def parse(self):
        if not self.vector_layer.isValid():
            raise ValueError("The provided layer is not valid.")

        features = list(self.vector_layer.getFeatures())
        for feature in features:
            correct_denum = self.get_correct_denum(feature)
            attributes = {key: feature[key] for key in feature.fields().names()}
            grup_data = GrupMasuraJT(
                id=feature.id(),
                class_id=attributes.get("CLASS_ID"),
                id_bdi=attributes.get("ID_BDI"),
                nr_crt=attributes.get("NR_CRT"),
                denum={'initial': attributes.get("DENUM"), # if this turns out to not be needed just default to attributes.get("DENUM")
                       'correct': correct_denum['denum'],
                       'nr': correct_denum['nr_scara']
                       }, 
                class_id_loc=attributes.get("CLASS_ID_LOC"),
                id_loc=attributes.get("ID_LOC"),
                nr_crt_loc=attributes.get("NR_CRT_LOC"),
                class_id_inst_sup=attributes.get("CLASS_ID_LOC"),
                id_inst_sup=attributes.get("ID_INST_SUP"),
                nr_crt_inst_sup=attributes.get("NR_CRT_INST_SUP"),
                jud=attributes.get("JUD"),
                prim=attributes.get("PRIM"),
                loc=attributes.get("LOC"),
                tip_str=attributes.get("TIP_STR"),
                str=attributes.get("STR"),
                nr_scara=attributes.get("NR_SCARA"),
                etaj=attributes.get("ETAJ"),
                ap=attributes.get("AP")
            )
            self.grupuri.append(grup_data)
    
    def get_name(self):
        return "GRUP_MASURA_XML_"
    
    def get_data(self):
        return self.grupuri
    
    def get_correct_denum(self, feature):
        denum_to_match = feature["DENUM"]
        nr_crt_to_match = feature["NR_CRT"]
        str_value = feature["STR"]
        nr_scara = feature["NR_SCARA"]

        # If NR_SCARA is a string without commas, return DENUM immediately
        if isinstance(nr_scara, str) and "," not in nr_scara:
            return {
                'denum': denum_to_match,
                'nr_scara': nr_scara
            }

        # Get the layer
        layer_list = QgsProject.instance().mapLayersByName("GRUP_MASURA_XML_")
        if not layer_list:
            QgsMessageLog.logMessage("Layer GRUP_MASURA_XML_ not found!", "StalpiAssist", level=Qgis.Critical)
            return {
                'denum': denum_to_match,
                'nr_scara': nr_scara
            }

        gr_layer = layer_list[0]  # Extract first matched layer

        # Extract all relevant features from layer
        matching_features = [f for f in gr_layer.getFeatures() if f["DENUM"] == denum_to_match]

        if not matching_features:
            return {
                'denum': denum_to_match,
                'nr_scara': nr_scara
            }

        QgsMessageLog.logMessage(f"Found {len(matching_features)} matching features for DENUM={denum_to_match}", "StalpiAssist", level=Qgis.Info)

        # Sort matching features by NR_CRT (handling NULLs safely)
        matching_features.sort(key=lambda f: (f["NR_CRT"] if f["NR_CRT"] not in config.NULL_VALUES else float("inf")))

        # Find the index of our feature in the sorted list
        try:
            index = next(i for i, f in enumerate(matching_features) if f["NR_CRT"] == nr_crt_to_match)
        except StopIteration:
            QgsMessageLog.logMessage(f"NR_CRT={nr_crt_to_match} not found in sorted features.", "StalpiAssist", level=Qgis.Warning)
            return {
                'denum': denum_to_match,
                'nr_scara': nr_scara
            }
        except Exception as e:
            QgsMessageLog.logMessage(f"Error finding index: {e}", "StalpiAssist", level=Qgis.Critical)
            return {
                'denum': denum_to_match,
                'nr_scara': nr_scara
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
            correct_nr_scara = scara_values[index] if index < len(scara_values) else scara_values[0]  # Get nth index or fallback to first

        return {
            'denum': f"{str_value} {correct_nr_scara}".strip(),
            'nr_scara': correct_nr_scara
        } 


    
    def resolve_mapping(self, parser, mapping):
        if isinstance(mapping, tuple):
            parts = [
                str(getattr(parser, element, "")).strip() if hasattr(parser, element) else str(element).strip()
                for element in mapping
            ]
            return " ".join(filter(None, parts)).strip()
        elif callable(mapping):
            return mapping(parser)
        return str(getattr(parser, mapping, "")).strip() if mapping else ""

    def write_to_excel_sheet(self, excel_file):
        data = []
        headers = list(self.mapping.keys())
        
        # Prepare data for writing
        sorted_gr = sorted(
            self.grupuri,
            key=lambda gr: gr.nr_crt if gr.nr_crt not in config.NULL_VALUES else float("inf")
        )
        for grupa in sorted_gr:
            row = []
            for header in headers:
                mapping = self.mapping.get(header)
                value = self.resolve_mapping(grupa, mapping)
                # Replace None with an empty string
                value = "" if value in config.NULL_VALUES else value
                row.append(value)
            data.append(row)
        
        workbook = load_workbook(excel_file)
        sheet = workbook["GRUP_MASURA"]
        
        start_row = sheet.max_row + 1
        header_row = sheet.max_row - 1
        existing_headers = {sheet.cell(row=header_row, column=col_idx).value: col_idx for col_idx in range(1, sheet.max_column + 1) if sheet.cell(row=header_row, column=col_idx).value}
        
        # Write data to the sheet
        for row_idx, row_data in enumerate(data, start=start_row):
            for col_idx, (header, cell_value) in enumerate(zip(headers, row_data), start=1):
                if header.strip(" ") in existing_headers:
                    sheet.cell(row=row_idx, column=existing_headers[header], value=cell_value if cell_value is not None else "")

        workbook.save(excel_file)

