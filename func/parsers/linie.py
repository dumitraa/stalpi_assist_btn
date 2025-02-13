from typing import List
from openpyxl import load_workbook
from ... import config

class LinieJT:
    def __init__(self, id, class_id, id_bdi, nr_crt, denum, prop, class_id_loc, id_loc, class_id_inst_sup, id_inst_sup, cod_ad_energ, niv_ten, tip_lin, an_pif_init, nr_iv):
        self.id = id
        self.class_id = class_id
        self.id_bdi = id_bdi
        self.nr_crt = nr_crt
        self.denum = denum
        self.prop = prop
        self.class_id_loc = class_id_loc
        self.id_loc = id_loc
        self.class_id_inst_sup = class_id_inst_sup
        self.id_inst_sup = id_inst_sup
        self.cod_ad_energ = cod_ad_energ
        self.niv_ten = niv_ten
        self.tip_lin = tip_lin
        self.an_pif_init = an_pif_init
        self.nr_iv = nr_iv

    def __repr__(self):
        return f"LinieJT(denum={self.denum}, niv_ten={self.niv_ten}, tip_lin={self.tip_lin})"


class IgeaLinieParser:
    def __init__(self, vector_layer):
        self.vector_layer = vector_layer
        self.linii: List[LinieJT] = []
        
        self.mapping = {
            "ID": "id_bdi",
            "Denumire": lambda ln: "",
            "Descrierea BDI": "denum",
            "Proprietar": lambda ln: ln.prop if ln.prop not in config.NULL_VALUES else "DEER",
            "Locatia": "id_loc",
            "Descrierea instalatiei superioare": lambda ln: "",
            "Nivel tensiune (kV)": "niv_ten",
            "Tipul liniei": "tip_lin",
        }
        
        # self.qgis_mapping = ["CLASS_ID", "ID_BDI", "NR_CRT", "DENUM", "PROP", "CLASS_ID_LOC", "ID_LOC", "CLASS_ID_INST_SUP", "ID_INST_SUP", "COD_AD_ENERG", "NIV_TEN", "TIP_LIN", "AN_PIF_INIT", "NR_IV"]

    def parse(self):
        if not self.vector_layer.isValid():
            raise ValueError("The provided layer is not valid.")

        features = list(self.vector_layer.getFeatures())
        for feature in features:
            attributes = {key: feature[key] for key in feature.fields().names()}
            linie_data = LinieJT(
                id=feature.id(),
                class_id=attributes.get("CLASS_ID"),
                id_bdi=attributes.get("ID_BDI"),
                nr_crt=attributes.get("NR_CRT"),
                denum=attributes.get("DENUM"),
                prop=attributes.get("PROP"),
                class_id_loc=attributes.get("CLASS_ID_LOC"),
                id_loc=attributes.get("ID_LOC"),
                class_id_inst_sup=attributes.get("CLASS_ID_INST_SUP"),
                id_inst_sup=attributes.get("ID_INST_SUP"),
                cod_ad_energ=attributes.get("COD_AD_ENERG"),
                niv_ten=attributes.get("NIV_TEN"),
                tip_lin=attributes.get("TIP_LIN"),
                an_pif_init=attributes.get("AN_PIF_INIT"),
                nr_iv=attributes.get("NR_IV")
            )
            self.linii.append(linie_data)
                    
    def get_name(self):
        return "LINIE_JT"
            
    def get_data(self):
        return self.linii
    
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
        for linie in self.linii:
            row = []
            for header in headers:
                mapping = self.mapping.get(header)
                value = self.resolve_mapping(linie, mapping)
                value = "" if value in config.NULL_VALUES else value
                row.append(value)
            data.append(row)
        
        workbook = load_workbook(excel_file)
        sheet = workbook["LINIE_JOASA_TENSIUNE"]
        
        start_row = sheet.max_row + 1
        header_row = sheet.max_row - 1
        existing_headers = {sheet.cell(row=header_row, column=col_idx).value: col_idx for col_idx in range(1, sheet.max_column + 1) if sheet.cell(row=header_row, column=col_idx).value}
        
        # Write data to the sheet
        for row_idx, row_data in enumerate(data, start=start_row):
            for col_idx, (header, cell_value) in enumerate(zip(headers, row_data), start=1):
                if header.strip() in existing_headers:
                    sheet.cell(row=row_idx, column=existing_headers[header.strip()], value=cell_value if cell_value is not None else "")
        
        workbook.save(excel_file)
