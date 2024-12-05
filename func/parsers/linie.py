from typing import List

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
        
        self.friendly_names = {
            "class_id": "Clasa ID",
            "id_bdi": "ID BDI",
            "nr_crt": "Nr. crt.",
            "denum": "Denumire",
            "prop": "Proprietar",
            "class_id_loc": "Clasa ID Locatie",
            "id_loc": "ID Locatie",
            "class_id_inst_sup": "Clasa ID Instalatie Sup.",
            "id_inst_sup": "ID Instalatie Sup.",
            "cod_ad_energ": "Cod calcul adresa energetica",
            "niv_ten": "Nivel tensiune",
            "tip_lin": "Tip linie",
            "an_pif_init": "Anul PIF Initial",
            "nr_iv": "Nr. Inventar"
        }
            
    def parse(self):
        if not self.vector_layer.isValid():
            raise ValueError("The provided layer is not valid.")

        for feature in self.vector_layer.getFeatures():
            linie_data = LinieJT(
                id=feature["ID"],
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
            
    def get_linii(self):
        return self.linii
