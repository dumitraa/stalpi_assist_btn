from typing import List

class FiridaJT:
    def __init__(self, id, class_id, id_bdi, nr_crt, iden, class_id_loc, id_loc, nr_crt_loc, 
                 class_id_inst_sup, id_inst_sup, desc_inst_sup, nr_crt_inst_sup, jud, prim, loc, tip_str, 
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
        self.desc_inst_sup = desc_inst_sup
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
                class_id_inst_sup = feature['CLASS_ID_INST_SUP'],
                id_inst_sup = feature['ID_INST_SUP'],
                desc_inst_sup = feature['DESC_INST_SUP'],
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

    def get_firide(self):
        return self.firide