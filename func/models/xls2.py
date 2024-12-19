"""
Model exported as python.
Name : 006 GENERARE MACHETE XLS_2
Group : LEA JT
With QGIS : 33802
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class GenerareMacheteXls_2(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('bransament_xml_', 'BRANSAMENT_XML_', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('deschideri_xml', 'DESCHIDERI XML', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('firida_xml_', 'FIRIDA_XML_', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('grup_masura_xml_', 'GRUP_MASURA_XML_', types=[QgsProcessing.TypeVectorAnyGeometry], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('linia_jt', 'LINIA_JT', types=[QgsProcessing.TypeVector], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('FiridaMacheta', 'FIRIDA MACHETA', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue='TEMPORARY_OUTPUT'))
        self.addParameter(QgsProcessingParameterFeatureSink('GrupMasuraMacheta', 'GRUP MASURA MACHETA', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue='TEMPORARY_OUTPUT'))
        self.addParameter(QgsProcessingParameterFeatureSink('DeschideriMacheta', 'DESCHIDERI MACHETA', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('BransamenteMacheta', 'BRANSAMENTE MACHETA', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue='TEMPORARY_OUTPUT'))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(12, model_feedback)
        results = {}
        outputs = {}

        # Refactor fields LINIE JT
        alg_params = {
            'FIELDS_MAPPING': [{'alias': None,'comment': None,'expression': '"fid"','length': 0,'name': 'fid','precision': 0,'sub_type': 0,'type': 4,'type_name': 'int8'},{'alias': None,'comment': None,'expression': '"CLASS_ID"','length': 0,'name': 'CLASS_ID','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_BDI"','length': 0,'name': 'ID_BDI','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT"','length': 0,'name': 'NR_CRT','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DENUM"','length': 0,'name': 'DENUM','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"PROP"','length': 0,'name': 'PROP','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"CLASS_ID_LOC"','length': 0,'name': 'CLASS_ID_LOC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_LOC"','length': 0,'name': 'ID_LOC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"CLASS_ID_INST_SUP"','length': 0,'name': 'CLASS_ID_INST_SUP','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_INST_SUP"','length': 0,'name': 'ID_INST_SUP','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"COD_AD_ENERG"','length': 0,'name': 'COD_AD_ENERG','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NIV_TEN"','length': 0,'name': 'NIV_TEN','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_LIN"','length': 0,'name': 'TIP_LIN','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"AN_PIF_INIT"','length': 0,'name': 'AN_PIF_INIT','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_IV"','length': 0,'name': 'NR_IV','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'}],
            'INPUT': parameters['linia_jt'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RefactorFieldsLinieJt'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Refactor fields GR
        alg_params = {
            'FIELDS_MAPPING': [{'alias': None,'comment': None,'expression': 'NR_CRT','length': 0,'name': 'Nr.crt','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'DENUM','length': 0,'name': 'Denumire','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': "'GRUP MASURA' ||' '  || DENUM",'length': 0,'name': 'Descrierea BDI','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'NR_CRT_LOC','length': 0,'name': 'Nr.crt_Locatia','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': "'FB' ||' '  || DENUM",'length': 0,'name': 'Locatia','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'CLASS_ID_INST_SUP','length': 0,'name': 'ID_Descrierea instalatiei uperioare','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Descrierea instalatiei uperioare"','length': 0,'name': 'Descrierea instalatiei uperioare','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'JUD','length': 0,'name': 'Judet','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'PRIM','length': 0,'name': 'Primarie','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'LOC','length': 0,'name': 'Localitate','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'TIP_STR','length': 0,'name': 'Tip strada','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'STR','length': 0,'name': 'Strada','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'NR_SCARA','length': 0,'name': 'nr./ scara','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'ETAJ','length': 0,'name': 'Etaj','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'AP','length': 0,'name': 'Apartament','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'}],
            'INPUT': parameters['grup_masura_xml_'],
            'OUTPUT': parameters['GrupMasuraMacheta']
        }
        outputs['RefactorFieldsGr'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['GrupMasuraMacheta'] = outputs['RefactorFieldsGr']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Refactor fields FR
        alg_params = {
            'FIELDS_MAPPING': [{'alias': None,'comment': None,'expression': 'NR_CRT','length': 0,'name': 'Nr.crt','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': ' "STR"  || \' \' ||  "NR" ','length': 0,'name': 'Identificator','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'CASE WHEN "ROL_FIRI" =\'de bransament\' THEN (\'FB\' || \' \' || "STR"|| \' \' ||"NR")\r\nELSE (\'FR\' || \' \' || "STR"|| \' \' ||"NR")\r\nEND','length': 0,'name': 'Descrierea BDI','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'CASE WHEN "ID_LOC" IS NULL THEN "NR_CRT_LOC"\r\nELSE "ID_LOC"\r\nEND','length': 0,'name': 'ID_Locatia','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Locatia"','length': 0,'name': 'Locatia','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'ID_INST_SUP','length': 0,'name': 'ID_Descrierea instalatiei superioare','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Descrierea instalatiei superioare"','length': 0,'name': 'Descrierea instalatiei superioare','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Judet"','length': 0,'name': 'Judet','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Primarie"','length': 0,'name': 'Primarie','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Localitate"','length': 0,'name': 'Localitate','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'TIP_STR','length': 0,'name': 'Tip strada','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'STR','length': 0,'name': 'Strada','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'NR','length': 0,'name': 'Numarul','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'ETAJ','length': 0,'name': 'Etaj','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'ROL_FIRI','length': 0,'name': 'Rolul firidei','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'TIP_FIRI_RET','length': 0,'name': 'Tip firida retea','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'AMPL','length': 0,'name': 'Amplasare','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'MAT','length': 0,'name': 'Material','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'DEF_FIRI','length': 0,'name': 'Defecte firida','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'NR_CIR','length': 0,'name': 'Nr circuite','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'TIP_FIRI_BR','length': 0,'name': 'Tip firida bransament','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'LIM_PROP','length': 0,'name': 'Limita de proprietate','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'AN_FUNC','length': 0,'name': 'Anul punerii în functiune','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'LAT','length': 0,'name': 'Latitudine (grade zecimale)','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'LONG','length': 0,'name': 'Longitudine (grade zecimale)','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'ALT','length': 0,'name': 'Altitudine (m)','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'X_STEREO_70','length': 0,'name': 'x - STEREO 70 (m)','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'Y_STEREO_70','length': 0,'name': 'y - STEREO 70 (m)','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'Z_STEREO_70','length': 0,'name': 'z - STEREO 70 (m)','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'GEO','length': 0,'name': 'Geometrie','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'SURSA_COORD','length': 0,'name': 'Sursa coordonate','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'DATA_COORD','length': 0,'name': 'Data actualizarii coordonatelor','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'}],
            'INPUT': parameters['firida_xml_'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RefactorFieldsFr'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Refactor deschideri DESCHIDERI
        alg_params = {
            'FIELDS_MAPPING': [{'alias': None,'comment': None,'expression': '"NR_CRT"','length': 0,'name': 'Nr.crt','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DENUM"','length': 0,'name': 'Denumire','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '\'DESC\'  || \' \' || "DENUM"','length': 0,'name': 'Descrierea BDI','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'array_to_string(\r\n    array_distinct(\r\n        aggregate(\r\n            layer:=\'AUX_tr\',\r\n            aggregate:=\'array_agg\',\r\n            expression:="ID_Locatia",\r\n            filter:=geom_to_wkt($geometry) = geom_to_wkt(geometry(@parent))\r\n        )\r\n    ), \', \'\r\n)\r\n','length': 0,'name': 'ID_Locatia','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'array_to_string(\r\n    array_distinct(\r\n        aggregate(\r\n            layer:=\'AUX_tr\',\r\n            aggregate:=\'array_agg\',\r\n            expression:="Locatia",\r\n            filter:=geom_to_wkt($geometry) = geom_to_wkt(geometry(@parent))\r\n        )\r\n    ), \', \'\r\n)','length': 0,'name': 'Locatia','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_STP_INC"','length': 0,'name': 'Nr.crt_Inceput','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'substr("DENUM", 1, strpos("DENUM", \' - \') - 1)','length': 0,'name': 'Stâlpul de inceput','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_STP_TERM"','length': 0,'name': 'Nr.crt_sfarsit','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'substr("DENUM", strpos("DENUM", \' - \') + 3)','length': 0,'name': 'Stâlpul terminal','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_Tronson JT1"','length': 0,'name': 'ID_Tronson JT1','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_TR_JT1"','length': 0,'name': 'Tronson JT1','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_Tronson JT2"','length': 0,'name': 'ID_Tronson JT2','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_TR_JT2"','length': 0,'name': 'Tronson JT2','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_Tronson JT3"','length': 0,'name': 'ID_Tronson JT3','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_TR_JT3"','length': 0,'name': 'Tronson JT3','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_Tronson JT4"','length': 0,'name': 'ID_Tronson JT4','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_TR_JT4"','length': 0,'name': 'Tronson JT4','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_Tronson JT5"','length': 0,'name': 'ID_Tronson JT5','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_TR_JT5"','length': 0,'name': 'Tronson JT5','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_Tronson JT6"','length': 0,'name': 'ID_Tronson JT6','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_TR_JT6"','length': 0,'name': 'Tronson JT6','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"LUNG"','length': 0,'name': 'Lungime (m)','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"GEO"','length': 0,'name': 'Geometrie','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Observatii"','length': 0,'name': 'Observatii','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'}],
            'INPUT': parameters['deschideri_xml'],
            'OUTPUT': parameters['DeschideriMacheta']
        }
        outputs['RefactorDeschideriDeschideri'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['DeschideriMacheta'] = outputs['RefactorDeschideriDeschideri']['OUTPUT']

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Refactor fields BR
        alg_params = {
            'FIELDS_MAPPING': [{'alias': None,'comment': None,'expression': '"NR_CRT"','length': 0,'name': 'Nr.crt','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DENUM"','length': 0,'name': 'Denumire','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '\'BR\' ||  \' \'|| "DENUM"','length': 0,'name': 'Descrierea BDI','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'ID_LOC','length': 0,'name': 'ID_Locatia','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Locatia"','length': 0,'name': 'Locatia','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'NR_CRT_PLC_BR','length': 0,'name': 'ID_PAPT/Nr.crt_Plecare bransament','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'aggregate(\r\n    layer:=\'STALPI MACHETA\',\r\n    aggregate:=\'array_agg\',\r\n    expression:="Descrierea BDI",\r\n    filter:=intersects($geometry, geometry(@parent))\r\n)[0]','length': 0,'name': 'Plecare bransament','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'TIP_BR','length': 0,'name': 'Tip bransament','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Tipul dispunerii"','length': 0,'name': 'Tipul dispunerii','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'TIP_COND','length': 0,'name': 'Tip conductor','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'LUNG','length': 0,'name': 'Lungime (m)','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'JUD','length': 0,'name': 'Judet','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'PRIM','length': 0,'name': 'Primarie','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'LOC','length': 0,'name': 'Localitate','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'TIP_STR','length': 0,'name': 'Tip strada','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'STR','length': 0,'name': 'Strada','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'NR_IMOB','length': 0,'name': 'Numar imobil','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'GEO','length': 0,'name': 'Geometrie','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'SURSA_COORD','length': 0,'name': 'Sursa coordonate','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'DATA_COORD','length': 0,'name': 'Data actualizarii coordonatelor','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'OBS','length': 0,'name': 'Observatii','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'}],
            'INPUT': parameters['bransament_xml_'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RefactorFieldsBr'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Retain fields
        alg_params = {
            'FIELDS': ['ID_BDI','DENUM'],
            'INPUT': outputs['RefactorFieldsLinieJt']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RetainFields'] = processing.run('native:retainfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'ID_Locatia',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'ID_BDI',
            'INPUT': outputs['RefactorFieldsBr']['OUTPUT'],
            'INPUT_2': outputs['RetainFields']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value FR cu LINIE
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'ID_Descrierea instalatiei superioare',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'ID_BDI',
            'INPUT': outputs['RefactorFieldsFr']['OUTPUT'],
            'INPUT_2': outputs['RetainFields']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueFrCuLinie'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Refactor fields
        alg_params = {
            'FIELDS_MAPPING': [{'alias': None,'comment': None,'expression': '"Nr.crt"','length': 0,'name': 'Nr.crt','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Denumire"','length': 0,'name': 'Denumire','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Descrierea BDI"','length': 0,'name': 'Descrierea BDI','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_Locatia"','length': 0,'name': 'ID_Locatia','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'DENUM','length': 0,'name': 'Locatia','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_PAPT/Nr.crt_Plecare bransament"','length': 0,'name': 'ID_PAPT/Nr.crt_Plecare bransament','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Plecare bransament"','length': 0,'name': 'Plecare bransament','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Tip bransament"','length': 0,'name': 'Tip bransament','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'case when\r\n( "Tip conductor" like \'%XABY%\' or \r\n  "Tip conductor" like \'%ACYABY%\') then \'LES\'\r\n  else \'LEA\'\r\n  end','length': 0,'name': 'Tipul dispunerii','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Tip conductor"','length': 0,'name': 'Tip conductor','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Lungime (m)"','length': 0,'name': 'Lungime (m)','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Judet"','length': 0,'name': 'Judet','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Primarie"','length': 0,'name': 'Primarie','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Localitate"','length': 0,'name': 'Localitate','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Tip strada"','length': 0,'name': 'Tip strada','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Strada"','length': 0,'name': 'Strada','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Numar imobil"','length': 0,'name': 'Numar imobil','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Geometrie"','length': 0,'name': 'Geometrie','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Sursa coordonate"','length': 0,'name': 'Sursa coordonate','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Data actualizarii coordonatelor"','length': 0,'name': 'Data actualizarii coordonatelor','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Observatii"','length': 0,'name': 'Observatii','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'}],
            'INPUT': outputs['JoinAttributesByFieldValue']['OUTPUT'],
            'OUTPUT': parameters['BransamenteMacheta']
        }
        outputs['RefactorFields'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['BransamenteMacheta'] = outputs['RefactorFields']['OUTPUT']

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Field calculator DESC INSTALATIE
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'Descrierea instalatiei superioare',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': '"DENUM"',
            'INPUT': outputs['JoinAttributesByFieldValueFrCuLinie']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorDescInstalatie'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Field calculator ID LOC
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'Locatia',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': 'case when "ID_Locatia" = "ID_Descrierea instalatiei superioare" then "Descrierea instalatiei superioare"\r\nelse \r\n(\'BR\'  || \' \' || \r\n (aggregate(\r\n    layer:=\'BRANSAMENT_XML_\',\r\n    aggregate:=\'array_agg\',\r\n    expression:="DENUM",\r\n    filter:=intersects($geometry, geometry(@parent))\r\n)[0]))\r\nEND',
            'INPUT': outputs['FieldCalculatorDescInstalatie']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorIdLoc'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Drop field(s)
        alg_params = {
            'COLUMN': ['ID_BDI','DENUM'],
            'INPUT': outputs['FieldCalculatorIdLoc']['OUTPUT'],
            'OUTPUT': parameters['FiridaMacheta']
        }
        outputs['DropFields'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['FiridaMacheta'] = outputs['DropFields']['OUTPUT']
        return results

    def name(self):
        return '006 GENERARE MACHETE XLS_2'

    def displayName(self):
        return '006 GENERARE MACHETE XLS_2'

    def group(self):
        return 'LEA JT'

    def groupId(self):
        return 'LEA JT'

    def createInstance(self):
        return GenerareMacheteXls_2()
