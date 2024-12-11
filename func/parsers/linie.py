from typing import List
from openpyxl import load_workbook
from openpyxl.styles import Border, Side

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
            "Denumire": "denum",
            "Descrierea BDI": "",                       # to determine
            "Proprietar": "prop",
            "Locatia": "",                              # to determine
            "Descrierea instalatiei superioare": "",    # to determine
            "Nivel tensiune (kV)": "niv_ten",
            "Tipul liniei": "tip_lin",
        }
        
        self.qgis_mapping = {
            "CLASS_ID": "CLASS_ID",
            "ID_BDI": "ID_BDI",
            "NR_CRT": "NR_CRT",
            "DENUM": "DENUM",
            "PROP": "PROP",
            "CLASS_ID_LOC": "CLASS_ID_LOC",
            "ID_LOC": "ID_LOC",
            "CLASS_ID_INST_SUP": "CLASS_ID_INST_SUP",
            "ID_INST_SUP": "ID_INST_SUP",
            "COD_AD_ENERG": "COD_AD_ENERG",
            "NIV_TEN": "NIV_TEN",
            "TIP_LIN": "TIP_LIN",
            "AN_PIF_INIT": "AN_PIF_INIT",
            "NR_IV": "NR_IV",
        }
            
            
    def parse(self):
        if not self.vector_layer.isValid():
            raise ValueError("The provided layer is not valid.")

        for feature in self.vector_layer.getFeatures():
            linie_data = LinieJT(
                id=feature.id(),
                class_id=feature["CLASS_ID"],
                id_bdi=feature["ID_BDI"],
                nr_crt=feature["NR_CRT"],
                denum=feature["DENUM"],
                prop=feature["PROP"],
                class_id_loc=feature["CLASS_ID_LOC"],
                id_loc=feature["ID_LOC"],
                class_id_inst_sup=feature["CLASS_ID_INST_SUP"],
                id_inst_sup=feature["ID_INST_SUP"],
                cod_ad_energ=feature["COD_AD_ENERG"],
                niv_ten=feature["NIV_TEN"],
                tip_lin=feature["TIP_LIN"],
                an_pif_init=feature["AN_PIF_INIT"],
                nr_iv=feature["NR_IV"]
            )
            self.linii.append(linie_data)
            
    def get_data(self):
        return self.linii
    
    def get_name(self):
        return "LINIE_JT"
    
    def write_to_excel_sheet(self, excel_file):
        data = []
        headers = list(self.mapping.keys())
        
        # Prepare data for writing
        for linie in self.linii:
            row = []
            for header in headers:
                mapping = self.mapping.get(header)
                if not mapping:
                    value = ""
                elif isinstance(mapping, tuple):
                    prefix, attr = mapping
                    value = f"{prefix} {getattr(linie, attr, '')}"
                else:
                    value = getattr(linie, mapping, "")
                # Replace None with an empty string
                value = "" if value in ["NULL", None, "nan"] else value
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
        
        # Add borders to the cells
        thin_border = Border(
            left=Side(style="thin"),
            right=Side(style="thin"),
            top=Side(style="thin"),
            bottom=Side(style="thin"),
        )
        
        for row_idx, row_data in enumerate(data, start=start_row):
            for header in headers:
                if header.strip() in existing_headers:
                    cell = sheet.cell(row=row_idx, column=existing_headers[header.strip()])
                    cell.border = thin_border
        
        workbook.save(excel_file)

