from typing import List
from openpyxl import load_workbook
from openpyxl.styles import Border, Side


class BransamentJT():
    def __init__(self, id, class_id, id_bdi, nr_crt, denum, class_id_loc, id_loc, nr_crt_loc, 
                 class_id_plc_br, id_plc_br, nr_crt_plc_br, tip_br, tip_cond, lung, jud, 
                 prim, loc, tip_str, street, nr_imob, geo, sursa_coord, data_coord, obs):
        self.id = id
        self.class_id = class_id
        self.id_bdi = id_bdi
        self.nr_crt = nr_crt
        self.denum = denum
        self.class_id_loc = class_id_loc
        self.id_loc = id_loc
        self.nr_crt_loc = nr_crt_loc
        self.class_id_plc_br = class_id_plc_br
        self.id_plc_br = id_plc_br
        self.nr_crt_plc_br = nr_crt_plc_br
        self.tip_br = tip_br
        self.tip_cond = tip_cond
        self.lung = lung
        self.jud = jud
        self.prim = prim
        self.loc = loc
        self.tip_str = tip_str
        self.street = street
        self.nr_imob = nr_imob
        self.geo = geo
        self.sursa_coord = sursa_coord
        self.data_coord = data_coord
        self.obs = obs

    def __repr__(self):
        return f"BransamentJT(nr_crt={self.nr_crt}, denum={self.denum}, geo={self.geo})"


class IgeaBransamentParser:
    def __init__(self, vector_layer):
        self.vector_layer = vector_layer
        self.bransamente: List[BransamentJT] = []
        
        self.mapping = {
            "Nr. Crt": "nr_crt",
            "Denumire": "denum",
            "Descrierea BDI": ("BR ", "denum"),
            "ID_Locatia": "id_loc",
            "Locatia": "",                                          # to determine
            "ID_PAPT/Nr. Crt_Plecare bransament": "nr_crt_plc_br",
            "Plecare bransament": "",                               # to determine
            "Tip bransament": "tip_br",
            "Tipul dispunerii": "",                                 # to determine, "LES"?
            "Tip conductor": "tip_cond",
            "Lungime (m)": "lung",
            "Judet": "jud",
            "Primarie": "prim",
            "Localitate": "loc",
            "Tip strada": "tip_str",
            "Strada": "street",
            "Numar imobil": "nr_imob",
            "Geometrie": "geo",
            "Sursa coordonate": "sursa_coord",
            "Data actualizarii coordonatelor": "data_coord",
            "Observatii": "obs",
        }
        
        self.qgis_mapping = {
            "CLASS_ID": "CLASS_ID",
            "ID_BDI": "ID_BDI",
            "NR_CRT": "NR_CRT",
            "DENUM": "DENUM",
            "CLASS_ID_L": "CLASS_ID_LOC",
            "ID_LOC": "ID_LOC",
            "NR_CRT_LOC": "NR_CRT_LOC",
            "CLASS_ID_P": "CLASS_ID_PLC_BR",
            "ID_PLC_BR": "ID_PLC_BR",
            "NR_CRT_PLC": "NR_CRT_PLC_BR",
            "TIP_BR": "TIP_BR",
            "TIP_COND": "TIP_COND",
            "LUNG": "LUNG",
            "JUD": "JUD",
            "PRIM": "PRIM",
            "LOC": "LOC",
            "TIP_STR": "TIP_STR",
            "STR": "STR",
            "NR_IMOB": "NR_IMOB",
            "GEO": "GEO",
            "SURSA_COOR": "SURSA_COORD",
            "DATA_COORD": "DATA_COORD",
            "OBS": "OBS"
        }
            

    def parse(self):
        if not self.vector_layer.isValid():
            raise ValueError("The provided layer is not valid.")

        for feature in self.vector_layer.getFeatures():
            bransament_data = BransamentJT(
                id=feature.id(),
                class_id=feature['CLASS_ID'],
                id_bdi=feature['ID_BDI'],
                nr_crt=feature['NR_CRT'],
                denum=feature['DENUM'],
                class_id_loc=feature['CLASS_ID_L'],
                id_loc=feature['ID_LOC'],
                nr_crt_loc=feature['NR_CRT_LOC'],
                class_id_plc_br=feature['CLASS_ID_P'],
                id_plc_br=feature['ID_PLC_BR'],
                nr_crt_plc_br=feature['NR_CRT_PLC'],
                tip_br=feature['TIP_BR'],
                tip_cond=feature['TIP_COND'],
                lung=feature['LUNG'],
                jud=feature['JUD'],
                prim=feature['PRIM'],
                loc=feature['LOC'],
                tip_str=feature['TIP_STR'],
                street=feature['STR'],
                nr_imob=feature['NR_IMOB'],
                geo=feature['GEO'],
                sursa_coord=feature['SURSA_COOR'],
                data_coord=feature['DATA_COORD'],
                obs=feature['OBS']
            )
            self.bransamente.append(bransament_data)
            
    def get_name(self):
        return "BRANSAMENT_XML_"

    def get_data(self):
        return self.bransamente

    def write_to_excel_sheet(self, excel_file):
        data = []
        headers = list(self.mapping.keys())
        
        for bransament in self.bransamente:
            row = []
            for header in headers:
                mapping = self.mapping[header]
                if not mapping:
                    value = ""
                elif isinstance(mapping, tuple):
                    prefix, attr = mapping
                    value = f"{prefix} {getattr(bransament, attr, '')}"
                else:
                    value = getattr(bransament, mapping, "")
                value = "" if value in ["NULL", None, "nan"] else value
                row.append(value)
            data.append(row)
        
        workbook = load_workbook(excel_file)
        sheet = workbook["BRANSAMENT"]
        
        start_row = 2
        existing_headers = {sheet.cell(row=1, column=col_idx).value: col_idx for col_idx in range(1, sheet.max_column + 1)}
        
        for row_idx, row_data in enumerate(data, start=start_row):
                for col_idx, (header, cell_value) in enumerate(zip(headers, row_data), start=1):
                    if header.strip(" ") in existing_headers:
                        sheet.cell(row=row_idx, column=existing_headers[header], value=cell_value)
        
        thin_border = Border(left=Side(style='thin'), 
                            right=Side(style='thin'), 
                            top=Side(style='thin'), 
                            bottom=Side(style='thin'))
        
        for row_idx, row_data in enumerate(data, start=start_row):
            for header in enumerate(headers, start=1):
                if header in existing_headers:
                    cell = sheet.cell(row=row_idx, column=existing_headers[header])
                    cell.border = thin_border
        
        workbook.save(excel_file)