from typing import List

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

        self.friendly_names = {
            "class_id": "Clasa ID",
            "id_bdi": "ID BDI",
            "nr_crt": "Nr.crt",
            "denum": "Denumire",
            "class_id_loc": "Clasa ID Locatie",
            "id_loc": "ID Locatie",
            "nr_crt_loc": "Nr. Crt Locatie",
            "class_id_plc_br": "Clasa ID Plecare Bransament",
            "id_plc_br": "ID Plecare Bransament",
            "nr_crt_plc_br": "Nr. Crt Plecare Bransament",
            "tip_br": "Tip Bransament",
            "tip_cond": "Tip Conductor",
            "lung": "Lungime",
            "jud": "Judet",
            "prim": "Primarie",
            "loc": "Localitate",
            "tip_str": "Tip Strada",
            "street": "Strada",
            "nr_imob": "Numar Imobil",
            "geo": "Geometrie",
            "sursa_coord": "Sursa Coordonate",
            "data_coord": "Data Coordonate",
            "obs": "Observatii"
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
                class_id_loc=feature['CLASS_ID_LOC'],
                id_loc=feature['ID_LOC'],
                nr_crt_loc=feature['NR_CRT_LOC'],
                class_id_plc_br=feature['CLASS_ID_PLC_BR'],
                id_plc_br=feature['ID_PLC_BR'],
                nr_crt_plc_br=feature['NR_CRT_PLC_BR'],
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
                sursa_coord=feature['SURSA_COORD'],
                data_coord=feature['DATA_COORD'],
                obs=feature['OBS']
            )
            self.bransamente.append(bransament_data)

    def get_bransamente(self):
        return self.bransamente
