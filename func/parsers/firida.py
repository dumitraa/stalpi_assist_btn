from typing import List
from openpyxl import load_workbook
from openpyxl.styles import Border, Side
import pandas as pd
from qgis.core import QgsMessageLog, Qgis # type: ignore

class FiridaJT:
    def __init__(self, id, class_id, id_bdi, nr_crt, iden, class_id_loc, id_loc, nr_crt_loc, 
                 class_id_inst_sup, id_inst_sup, nr_crt_inst_sup, jud, prim, loc, tip_str, 
                 street, nr, etaj, rol_firi, tip_firi_ret, tip_firi_br, ampl, mat, lim_prop, 
                 def_firi, nr_cir, an_func, alt, geo, sursa_coord, data_coord, long, lat, 
                 x_stereo_70, y_stereo_70, z_stereo_70):
        self.id = id
        self.class_id = class_id
        self.id_bdi = id_bdi
        self.nr_crt = nr_crt
        self.iden = iden
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
        self.street = street
        self.nr = nr
        self.etaj = etaj
        self.rol_firi = rol_firi
        self.tip_firi_ret = tip_firi_ret
        self.tip_firi_br = tip_firi_br
        self.ampl = ampl
        self.mat = mat
        self.lim_prop = lim_prop
        self.def_firi = def_firi
        self.nr_cir = nr_cir
        self.an_func = an_func
        self.alt = alt
        self.geo = geo
        self.sursa_coord = sursa_coord
        self.data_coord = data_coord
        self.long = long
        self.lat = lat
        self.x_stereo_70 = x_stereo_70
        self.y_stereo_70 = y_stereo_70
        self.z_stereo_70 = z_stereo_70

    def __repr__(self):
        return f"FiridaJT(nr_crt={self.nr_crt}, iden={self.iden}, geo={self.geo})"


class IgeaFiridaParser:
    def __init__(self, vector_layer):
        self.vector_layer = vector_layer
        self.firide: List[FiridaJT] = []
        
        self.mapping = {
            "Nr.crt": "nr_crt",
            "Identificator": "iden",
            "Descrierea BDI": ("FR ", "iden"),          # might not be correct
            "ID_Locatia": "id_loc",
            "Locatia": "",                              # ?
            "ID_Descrierea instalatiei superioare": "id_inst_sup",
            "Descrierea instalatiei superioare": "desc_inst_sup",
            "Judet": "jud",
            "Primarie": "prim",
            "Localitate": "loc",
            "Tip strada": "tip_str",
            "Strada": "street",
            "Numarul": "nr",
            "Etaj": "etaj",
            "Rolul firidei": "rol_firi",
            "Tip firida retea": "tip_firi_ret",
            "Amplasare": "ampl",
            "Material": "mat",
            "Defecte firida": "def_firi",
            "Nr circuite": "nr_cir",
            "Tip firida bransament": "tip_firi_br",
            "Limita de proprietate": "lim_prop",
            "Anul punerii în functiune": "an_func",
            "Latitudine (grade zecimale)": "lat",
            "Longitudine (grade zecimale)": "long",
            "Altitudine (m)": "alt",
            "x - STEREO 70 (m)": "x_stereo_70",
            "y - STEREO 70 (m)": "y_stereo_70",
            "z - STEREO 70 (m)": "z_stereo_70",
            "Geometrie": "geo",
            "Sursa coordonate": "sursa_coord",
            "Data actualizarii coordonatelor": "data_coord"
        }
        
        self.qgis_mapping = {
            "CLASS_ID": "CLASS_ID",
            "ID_BDI": "ID_BDI",
            "NR_CRT": "NR_CRT",
            "IDEN": "IDEN",
            "CLASS_ID_LOC": "CLASS_ID_LOC",
            "ID_LOC": "ID_LOC",
            "NR_CRT_LOC": "NR_CRT_LOC",
            "CLASS_ID_LOC": "CLASS_ID_INST_SUP",
            "ID_INST_SUP": "ID_INST_SUP",
            "NR CRT INS": "NR_CRT_INST_SUP",
            "JUD": "JUD",
            "PRIM": "PRIM",
            "LOC": "LOC",
            "TIP_STR": "TIP_STR",
            "STR": "STR",
            "NR": "NR",
            "ETAJ": "ETAJ",
            "ROL_FIRI": "ROL_FIRI",
            "TIP_FIRI_RET": "TIP_FIRI_RET",
            "TIP_FIRI_BR": "TIP_FIRI_BR",
            "AMPL": "AMPL",
            "MAT": "MAT",
            "LIM_PROP": "LIM_PROP",
            "DEF_FIRI": "DEF_FIRI",
            "NR_CIR": "NR_CIR",
            "AN_FUNC": "AN_FUNC",
            "ALT": "ALT",
            "GEO": "GEO",
            "SURSA_COORD": "SURSA_COORD",
            "DATA_COOR": "DATA_COORD",
            "LONG": "LONG",
            "LAT": "LAT",
            "X_STEREO_70": "X_STEREO_70",
            "Y_STEREO_70": "Y_STEREO_70",
            "Z_STEREO_70": "Z_STEREO_70"
        }

    def parse(self):
        if not self.vector_layer.isValid():
            raise ValueError("The provided layer is not valid.")

        for feature in self.vector_layer.getFeatures():
            firida_data = FiridaJT(
                id = feature.id(),
                class_id = feature['CLASS_ID'],
                id_bdi = feature['ID_BDI'],
                nr_crt = feature['NR_CRT'],
                iden = feature['IDEN'],
                class_id_loc = feature['CLASS_ID_LOC'],
                id_loc = feature['ID_LOC'],
                nr_crt_loc = feature['NR_CRT_LOC'],
                class_id_inst_sup = feature['CLASS_ID_LOC'],
                id_inst_sup = feature['ID_INST_SUP'],
                nr_crt_inst_sup = feature['NR_CRT_INST_SUP'],
                jud = feature['JUD'],
                prim = feature['PRIM'],
                loc = feature['LOC'],
                tip_str = feature['TIP_STR'],
                street = feature['STR'],
                nr = feature['NR'],
                etaj = feature['ETAJ'],
                rol_firi = feature['ROL_FIRI'],
                tip_firi_ret = feature['TIP_FIRI_RET'],
                tip_firi_br = feature['TIP_FIRI_BR'],
                ampl = feature['AMPL'],
                mat = feature['MAT'],
                lim_prop = feature['LIM_PROP'],
                def_firi = feature['DEF_FIRI'],
                nr_cir = feature['NR_CIR'],
                an_func = feature['AN_FUNC'],
                alt = feature['ALT'],
                geo = feature['GEO'],
                sursa_coord = feature['SURSA_COORD'],
                data_coord = feature['DATA_COORD'],
                long = feature['LONG'],
                lat = feature['LAT'],
                x_stereo_70 = feature['X_STEREO_70'],
                y_stereo_70 = feature['Y_STEREO_70'],
                z_stereo_70 = feature['Z_STEREO_70']
            )
            self.firide.append(firida_data)

    def get_name(self):
        return "FIRIDA_XML_"

    def get_data(self):
        return self.firide
    
    def write_to_excel_sheet(self, excel_file, split=False, done_split=False):
        data = []
        headers = list(self.mapping.keys())

        # Collect data rows
        for firida in self.firide:
            row = []
            for header in headers:
                mapping = self.mapping[header]
                if isinstance(mapping, tuple):
                    prefix, attr = mapping
                    value = f"{prefix} {getattr(firida, attr, '')}"
                else:
                    value = getattr(firida, mapping, "")
                value = "" if value in ["NULL", None, "nan"] else value
                row.append(value)
            data.append(row)

        df = pd.DataFrame(data, columns=headers)

        # Open Excel file
        try:
            workbook = load_workbook(excel_file)
        except Exception as e:
            QgsMessageLog.logMessage(f"Error opening workbook: {e}", "FirideAssistant", level=Qgis.Critical)
            return

        if split:
            df_retea = df[df['Rolul firidei'].str.contains('retea', na=False)]
            df_bransament = df[df['Rolul firidei'].str.contains('bransament', na=False)]
            sheets = {'FIRIDA RETEA': df_retea, 'FIRIDA BRANSAMENT': df_bransament}
        else:
            sheets = {'FIRIDA': df}

        for sheet_name, df_sheet in sheets.items():
            if sheet_name in workbook.sheetnames:
                sheet = workbook[sheet_name]
            else:
                sheet = workbook.create_sheet(sheet_name)

            # Determine header and start rows
            start_row = sheet.max_row + 1
            header_row = sheet.max_row - 1
            existing_headers = {sheet.cell(row=header_row, column=col_idx).value: col_idx for col_idx in range(1, sheet.max_column + 1) if sheet.cell(row=header_row, column=col_idx).value}

            # Ensure headers exist
            for idx, header in enumerate(headers, start=1):
                if header not in existing_headers:
                    sheet.cell(row=header_row, column=idx, value=header)
                    existing_headers[header] = idx

            # Write data rows
            for row_idx, row_data in enumerate(df_sheet.itertuples(index=False, name=None), start=start_row):
                for col_idx, (header, cell_value) in enumerate(zip(headers, row_data), start=1):
                    col_idx = existing_headers.get(header, col_idx)  # Fallback to index
                    sheet.cell(row=row_idx, column=col_idx, value=cell_value)

            # Add borders
            thin_border = Border(left=Side(style='thin'),
                                right=Side(style='thin'),
                                top=Side(style='thin'),
                                bottom=Side(style='thin'))

            for row_idx, row_data in enumerate(df_sheet.itertuples(index=False, name=None), start=start_row):
                for col_idx, header in enumerate(headers, start=1):
                    if header in existing_headers:
                        cell = sheet.cell(row=row_idx, column=existing_headers[header])
                        cell.border = thin_border

        try:
            workbook.save(excel_file)
        except Exception as e:
            QgsMessageLog.logMessage(f"Error saving workbook: {e}", "FirideAssistant", level=Qgis.Critical)

        if not done_split:
            self.write_to_excel_sheet(excel_file, split=True, done_split=True)
