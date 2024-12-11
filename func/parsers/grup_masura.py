from typing import List
from openpyxl import load_workbook
from openpyxl.styles import Border, Side

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
        return f"GrupMasuraJT(denum={self.denum}, niv_ten={self.niv_ten}, tip_lin={self.tip_lin})"


class IgeaGrupMasuraParser:
    def __init__(self, vector_layer):
        self.vector_layer = vector_layer
        self.grupuri: List[GrupMasuraJT] = []
        

        self.mapping = {
            "Nr.crt": "nr_crt",
            "Denumire": "denum",
            "Descrierea BDI": "",
            "Nr.crt_Locatia": "nr_crt_loc",
            "Locatia": "id_loc",
            "ID_Descrierea instalatiei uperioare": "id_inst_sup",
            "Descrierea instalatiei uperioare": "nr_crt_inst_sup",
            "Judet": "jud",
            "Primarie": "prim",
            "Localitate": "loc",
            "Tip strada": "tip_str",
            "Strada": "str",
            "nr./ scara": "nr_scara",
            "Etaj": "etaj",
            "Apartament": "ap"
        }
        
        self.qgis_mapping = {
            "CLASS_ID": "CLASS_ID",
            "ID_BDI": "ID_BDI",
            "NR_CRT": "NR_CRT",
            "DENUM": "DENUM",
            "CLASS_ID_LOC": "CLASS_ID_LOC",
            "ID_LOC": "ID_LOC",
            "NR_CRT_LOC": "NR_CRT_LOC",
            "CLASS_ID_LOC": "CLASS_ID_INST_SUP",
            "ID_INST_SUP": "ID_INST_SUP",
            "NR_CRT_INST_SUP": "NR_CRT_INST_SUP",
            "JUD": "JUD",
            "PRIM": "PRIM",
            "LOC": "LOC",
            "TIP_STR": "TIP_STR",
            "STR": "STR",
            "NR_SCARA": "NR_SCARA",
            "ETAJ": "ETAJ",
            "AP": "AP"
        }
            
    def parse(self):
        if not self.vector_layer.isValid():
            raise ValueError("The provided layer is not valid.")

        for feature in self.vector_layer.getFeatures():
            grup_data = GrupMasuraJT(
                id=feature.id(),
                class_id=feature["CLASS_ID"],
                id_bdi=feature["ID_BDI"],
                nr_crt=feature["NR_CRT"],
                denum=feature["DENUM"],
                class_id_loc=feature["CLASS_ID_LOC"],
                id_loc=feature["ID_LOC"],
                nr_crt_loc=feature["NR_CRT_LOC"],
                class_id_inst_sup=feature["CLASS_ID_LOC"],
                id_inst_sup=feature["ID_INST_SUP"],
                nr_crt_inst_sup=feature["NR_CRT_INST_SUP"],
                jud=feature["JUD"],
                prim=feature["PRIM"],
                loc=feature["LOC"],
                tip_str=feature["TIP_STR"],
                str=feature["STR"],
                nr_scara=feature["NR_SCARA"],
                etaj=feature["ETAJ"],
                ap=feature["AP"]
            )
            self.grupuri.append(grup_data)
    
    def get_name(self):
        return "GRUP_MASURA_XML_"
    
    def get_data(self):
        return self.grupuri
    
    def write_to_excel_sheet(self, excel_file):
        data = []
        headers = list(self.mapping.keys())
        
        # Prepare data for writing
        for grup in self.grupuri:
            row = []
            for header in headers:
                mapping = self.mapping.get(header)
                if not mapping:
                    value = ""
                elif isinstance(mapping, tuple):
                    prefix, attr = mapping
                    value = f"{prefix} {getattr(grup, attr, '')}"
                else:
                    value = getattr(grup, mapping, "")
                # Replace None with an empty string
                value = "" if value in ["NULL", None, "nan"] else value
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
