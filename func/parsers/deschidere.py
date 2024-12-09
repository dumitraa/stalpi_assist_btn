from typing import List
from openpyxl import load_workbook
from openpyxl.styles import Border, Side

class DeschidereJT:
    def __init__(self, id, class_id, id_bdi, nr_crt, denum, ip_stp_inc, nr_crt_stp_inc, id_stp_term, nr_crt_stp_term, id_tr_jt1, nr_crt_tr_jt1, id_tr_jt2, nr_crt_tr_jt2, id_tr_jt3, nr_crt_tr_jt3, id_tr_jt4, nr_crt_tr_jt4, id_tr_jt5, nr_crt_tr_jt5, id_tr_jt6, nr_crt_tr_jt6, geo, lung, sursa_coord, data_coord):
        self.id = id
        self.class_id = class_id
        self.id_bdi = id_bdi
        self.nr_crt = nr_crt
        self.denum = denum
        self.ip_stp_inc = ip_stp_inc
        self.nr_crt_stp_inc = nr_crt_stp_inc
        self.id_stp_term = id_stp_term
        self.nr_crt_stp_term = nr_crt_stp_term
        self.id_tr_jt1 = id_tr_jt1
        self.nr_crt_tr_jt1 = nr_crt_tr_jt1
        self.id_tr_jt2 = id_tr_jt2
        self.nr_crt_tr_jt2 = nr_crt_tr_jt2
        self.id_tr_jt3 = id_tr_jt3
        self.nr_crt_tr_jt3 = nr_crt_tr_jt3
        self.id_tr_jt4 = id_tr_jt4
        self.nr_crt_tr_jt4 = nr_crt_tr_jt4
        self.id_tr_jt5 = id_tr_jt5
        self.nr_crt_tr_jt5 = nr_crt_tr_jt5
        self.id_tr_jt6 = id_tr_jt6
        self.nr_crt_tr_jt6 = nr_crt_tr_jt6
        self.geo = geo
        self.lung = lung
        self.sursa_coord = sursa_coord
        self.data_coord = data_coord
        

    def __repr__(self):
        return f"DeschidereJT(denum={self.denum}, niv_ten={self.niv_ten}, tip_lin={self.tip_lin})"


class IgeaDeschidereParser:
    def __init__(self, vector_layer):
        self.vector_layer = vector_layer
        self.deschideri: List[DeschidereJT] = []
        
        # map values: Nr.crt	Denumire	Descrierea BDI	ID_Locatia	Locatia	Nr.crt_Inceput	Stâlpul de inceput	Nr.crt_sfarsit	Stâlpul terminal	ID_Tronson JT1	Tronson JT1	ID_Tronson JT2	Tronson JT2	ID_Tronson JT3	Tronson JT3	ID_Tronson JT4	Tronson JT4	ID_Tronson JT5	Tronson JT5	ID_Tronson JT6	Tronson JT6	Lungime (m)	Geometrie	Observatii

        self.mapping = {
            "Nr.crt": "nr_crt",
            "Denumire": "denum",
            "Descrierea BDI": "",
            "ID_Locatia": "id_loc",
            "Locatia": "loc",
            "Nr.crt_Inceput": "nr_crt_stp_inc",
            "Stâlpul de inceput": "ip_stp_inc",
            "Nr.crt_sfarsit": "nr_crt_stp_term",
            "Stâlpul terminal": "id_stp_term",
            "ID_Tronson JT1": "id_tr_jt1",
            "Tronson JT1": "nr_crt_tr_jt1",
            "ID_Tronson JT2": "id_tr_jt2",
            "Tronson JT2": "nr_crt_tr_jt2",
            "ID_Tronson JT3": "id_tr_jt3",
            "Tronson JT3": "nr_crt_tr_jt3",
            "ID_Tronson JT4": "id_tr_jt4",
            "Tronson JT4": "nr_crt_tr_jt4",
            "ID_Tronson JT5": "id_tr_jt5",
            "Tronson JT5": "nr_crt_tr_jt5",
            "ID_Tronson JT6": "id_tr_jt6",
            "Tronson JT6": "nr_crt_tr_jt6",
            "Lungime (m)": "lung",
            "Geometrie": "geo",
            "Observatii": ""
        }
        
        self.qgis_mapping = {
            "CLASS_ID": "CLASS_ID",
            "ID_BDI": "ID_BDI",
            "NR_CRT": "NR_CRT",
            "DENUM": "DENUM",
            "IP_STP_INC": "ID_STP_INC",
            "NR_CRT_STP": "NR_CRT_STP_INC",
            "ID_STP_TER": "ID_STP_TERM",
            "NR_CRT_S_1": "NR_CRT_STP_TERM",
            "ID_TR_JT1": "ID_TR_JT1",
            "NR_CRT_TR_": "NR_CRT_TR_JT1",
            "ID_TR_JT2": "ID_TR_JT2",
            "NR_CRT_T_1": "NR_CRT_TR_JT2",
            "ID_TR_JT3": "ID_TR_JT3",
            "NR_CRT_T_2": "NR_CRT_TR_JT3",
            "ID_TR_JT4": "ID_TR_JT4",
            "NR_CRT_T_3": "NR_CRT_TR_JT4",
            "ID_TR_JT5": "ID_TR_JT5",
            "NR_CRT_T_4": "NR_CRT_TR_JT5",
            "ID_TR_JT6": "ID_TR_JT6",
            "NR_CRT_T_5": "NR_CRT_TR_JT6",
            "GEO": "GEO",
            "LUNG": "LUNG",
            "SURSA_COOR": "SURSA_COORD",
            "DATA_COORD": "DATA_COORD"
        }
            
    def parse(self):
        if not self.vector_layer.isValid():
            raise ValueError("The provided layer is not valid.")

        for feature in self.vector_layer.getFeatures():
            deschidere_data = DeschidereJT(
                id=feature.id(),
                class_id=feature["CLASS_ID"],
                id_bdi=feature["ID_BDI"],
                nr_crt=feature["NR_CRT"],
                denum=feature["DENUM"],
                ip_stp_inc=feature["ID_STP_INC"],
                nr_crt_stp_inc=feature["NR_CRT_STP"],
                id_stp_term=feature["ID_STP_TER"],
                nr_crt_stp_term=feature["NR_CRT_S_1"],
                id_tr_jt1=feature["ID_TR_JT1"],
                nr_crt_tr_jt1=feature["NR_CRT_TR_"],
                id_tr_jt2=feature["ID_TR_JT2"],
                nr_crt_tr_jt2=feature["NR_CRT_T_1"],
                id_tr_jt3=feature["ID_TR_JT3"],
                nr_crt_tr_jt3=feature["NR_CRT_T_2"],
                id_tr_jt4=feature["ID_TR_JT4"],
                nr_crt_tr_jt4=feature["NR_CRT_T_3"],
                id_tr_jt5=feature["ID_TR_JT5"],
                nr_crt_tr_jt5=feature["NR_CRT_T_4"],
                id_tr_jt6=feature["ID_TR_JT6"],
                nr_crt_tr_jt6=feature["NR_CRT_T_5"],
                geo=feature["GEO"],
                lung=feature["LUNG"],
                sursa_coord=feature["SURSA_COOR"],
                data_coord=feature["DATA_COORD"]
            )
            self.deschideri.append(deschidere_data)
    
    def get_name(self):
        return "STALP_XML_"
            
    def get_data(self):
        return self.deschideri
    
    def write_to_excel_sheet(self, excel_file):
        data = []
        headers = list(self.mapping.keys())
        
        # Prepare data for writing
        for deschidere in self.deschideri:
            row = []
            for header in headers:
                mapping = self.mapping.get(header)
                if not mapping:
                    value = ""
                elif isinstance(mapping, tuple):
                    prefix, attr = mapping
                    value = f"{prefix} {getattr(deschidere, attr, '')}"
                else:
                    value = getattr(deschidere, mapping, "")
                # Replace None with an empty string
                value = "" if value in ["NULL", None, "nan"] else value
                row.append(value)
            data.append(row)
        
        workbook = load_workbook(excel_file)
        sheet = workbook["LINIE_JOASA_TENSIUNE"]
        
        start_row = 2
        existing_headers = {
            sheet.cell(row=1, column=col_idx).value: col_idx
            for col_idx in range(1, sheet.max_column + 1)
        }
        
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
