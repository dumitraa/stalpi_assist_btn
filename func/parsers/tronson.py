from typing import List

class TronsonJT:
    def __init__(self, id, class_id, id_bdi, nr_crt, denum, prop, class_id_loc, id_loc, nr_crt_loc, 
                 class_id_inc_tr, id_inc_tr, nr_crt_inc_tr, class_id_fin_tr, id_fin_tr, 
                 nr_crt_fin_tr, tip_tr, tip_cond, lung_tr, geo, sursa_coord, data_coord, 
                 unit_log_int, s_unit_log, post_luc, obs):
        self.id = id
        self.class_id = class_id
        self.id_bdi = id_bdi
        self.nr_crt = nr_crt
        self.denum = denum
        self.prop = prop
        self.class_id_loc = class_id_loc
        self.id_loc = id_loc
        self.nr_crt_loc = nr_crt_loc
        self.class_id_inc_tr = class_id_inc_tr
        self.id_inc_tr = id_inc_tr
        self.nr_crt_inc_tr = nr_crt_inc_tr
        self.class_id_fin_tr = class_id_fin_tr
        self.id_fin_tr = id_fin_tr
        self.nr_crt_fin_tr = nr_crt_fin_tr
        self.tip_tr = tip_tr
        self.tip_cond = tip_cond
        self.lung_tr = lung_tr
        self.geo = geo
        self.sursa_coord = sursa_coord
        self.data_coord = data_coord
        self.unit_log_int = unit_log_int
        self.s_unit_log = s_unit_log
        self.post_luc = post_luc
        self.obs = obs

    def __repr__(self):
        return f"TronsonJT(nr_crt={self.nr_crt}, denum={self.denum}, geo={self.geo})"


class IgeaTronsonParser:
    def __init__(self, vector_layer):
        self.vector_layer = vector_layer
        self.tronsoane: List[TronsonJT] = []
        self.mapping = {
            "Nr. crt": "nr_crt",
            "ID": "id_bdi",
            "Denumire": "denum",
            "Descrierea BDI": ("TR ", "denum"),
            "Proprietar": "prop",
            "ID_Locatia": "id_loc",
            "Locatia": "",                                  # Din csv tronson_JOASA_TENSIUNE - <ID_LOC> TO DESCRIEREA BDI
            "Nr.crt_Inceput de tronson": "nr_crt_inc_tr",
            "Inceput de tronson": "",                       # to determine
            "Nr.crt_Final de tronson": "nr_crt_fin_tr",
            "Final de tronson": "",                         # to determine
            "Tipul tronsonului": "tip_tr",
            "Tip conductor": "tip_cond",
            "Lungimea tronsonului (km)": "lung_tr",
            "Geometrie": "geo",
            "Sursa coordonate": "sursa_coord",
            "Data actualizarii coordonatelor": "data_coord",
            "Unitate logistica de intretinere": "unit_log_int",
            "Sectie unitate logistica": "s_unit_log",
            "Post de lucru": "post_luc",
            "Observatii": "obs"
        }
        
        self.friendly_names = {
            "class_id": "Clasa ID",
            "id_bdi": "ID BDI",
            "nr_crt": "Nr. crt",
            "denum": "Denumire",
            "prop": "Proprietar",
            "class_id_loc": "Clasa ID Loc.",
            "id_loc": "ID Locatie",
            "nr_crt_loc": "Nr. crt Loc.",
            "class_id_inc_tr": "Clasa ID Inceput de tro.",
            "id_inc_tr": "ID Inceput de tronson",
            "nr_crt_inc_tr": "Nr. crt Inceput de tr.",
            "class_id_fin_tr": "Clasa ID Final de tr.",
            "id_fin_tr": "ID Final de tronson",
            "nr_crt_fin_tr": "Nr. crt Final de tr.",
            "tip_tr": "Tipul tr.",
            "tip_cond": "Tip conductor",
            "lung_tr": "Lungimea tr.",
            "geo": "Geometrie",
            "sursa_coord": "Sursa coordonate",
            "data_coord": "Data coordonate",
            "unit_log_int": "Unitate logistica de intretinere",
            "s_unit_log": "Sectie unitate logistica",
            "post_luc": "Post de lucru",
            "obs": "Observatii"
        }


    def parse(self):
        if not self.vector_layer.isValid():
            raise ValueError("The provided layer is not valid.")

        for feature in self.vector_layer.getFeatures():
            tronson_data = TronsonJT(
                id = feature.id(),
                class_ud = feature['CLASS_ID'],
                id_bdi = feature['ID_BDI'],
                nr_crt = feature['NR_CRT'],
                denum = feature['DENUM'],
                prop = feature['PROP'],
                class_id_loc = feature['CLASS_ID_LOC'],
                id_loc = feature['ID_LOC'],
                nr_crt_loc = feature['NR_CRT_LOC'],
                class_id_inc_tr = feature['CLASS_ID_INC_TR'],
                id_inc_tr = feature['ID_INC_TR'],
                nr_crt_inc_tr = feature['NR_CRT_INC_TR'],
                class_id_fin_tr = feature['CLASS_ID_FIN_TR'],
                id_fin_tr = feature['ID_FIN_TR'],
                nr_crt_fin_tr = feature['NR_CRT_FIN_TR'],
                tip_tr = feature['TIP_TR'],
                tip_cond = feature['TIP_COND'],
                lung_tr = feature['LUNG_TR'],
                geo = feature['GEO'],
                sursa_coord = feature['SURSA_COORD'],
                data_coord = feature['DATA_COORD'],
                unit_log_int = feature['UNIT_LOG_INT'],
                s_unit_log = feature['S_UNIT_LOG'],
                post_luc = feature['POST_LUC'],
                obs = feature['OBS']
            )
            self.tronsoane.append(tronson_data)

    def get_tronsoane(self):
        return self.tronsoane