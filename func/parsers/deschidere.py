from typing import List

class DeschidereJT:
    def __init__(self, id, class_id, id_bdi, nr_crt, denum, ip_stp_inc, nr_crt_stp_inc, id_stp_term, nr_crt_stp_term, id_tr_jt1, nr_crt_tr_jt1, id_tr_jt2, nr_crt_tr_jt2, id_tr_jt3, nr_crt_tr_jt3, id_tr_jt4, nr_crt_tr_jt4, id_tr_jt5, nr_crt_tr_jt5, id_tr_jt6, nr_crt_tr_jt6, geo, lung, sursa_coor, data_coord):
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
        self.sursa_coor = sursa_coor
        self.data_coord = data_coord
        

    def __repr__(self):
        return f"DeschidereJT(denum={self.denum}, niv_ten={self.niv_ten}, tip_lin={self.tip_lin})"


class IgeaDeschidereParser:
    def __init__(self, vector_layer):
        self.vector_layer = vector_layer
        self.stalpi: List[DeschidereJT] = []
        
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
                ip_stp_inc=feature["IP_STP_INC"],
                nr_crt_stp_inc=feature["NR_CRT_STP_INC"],
                id_stp_term=feature["ID_STP_TERM"],
                nr_crt_stp_term=feature["NR_CRT_STP_TERM"],
                id_tr_jt1=feature["ID_TR_JT1"],
                nr_crt_tr_jt1=feature["NR_CRT_TR_JT1"],
                id_tr_jt2=feature["ID_TR_JT2"],
                nr_crt_tr_jt2=feature["NR_CRT_TR_JT2"],
                id_tr_jt3=feature["ID_TR_JT3"],
                nr_crt_tr_jt3=feature["NR_CRT_TR_JT3"],
                id_tr_jt4=feature["ID_TR_JT4"],
                nr_crt_tr_jt4=feature["NR_CRT_TR_JT4"],
                id_tr_jt5=feature["ID_TR_JT5"],
                nr_crt_tr_jt5=feature["NR_CRT_TR_JT5"],
                id_tr_jt6=feature["ID_TR_JT6"],
                nr_crt_tr_jt6=feature["NR_CRT_TR_JT6"],
                geo=feature["GEO"],
                lung=feature["LUNG"],
                sursa_coor=feature["SURSA_COOR"], # ?????????????
                data_coord=feature["DATA_COORD"]
            )
            self.deschideri.append(deschidere_data)
            
    def get_linii(self):
        return self.deschideri
