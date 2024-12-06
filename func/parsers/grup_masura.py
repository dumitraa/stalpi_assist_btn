from typing import List

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
        self.grup: List[GrupMasuraJT] = []
        
        # map names - Nr.crt	Denumire	Descrierea BDI	Nr.crt_Locatia	Locatia	ID_Descrierea instalatiei uperioare	Descrierea instalatiei uperioare	Judet	Primarie	Localitate	Tip strada	Strada	nr./ scara	Etaj	Apartament

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
                class_id_inst_sup=feature["CLASS_ID_INST_SUP"],
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
            self.grup.append(grup_data)
            
    def get_linii(self):
        return self.grup
