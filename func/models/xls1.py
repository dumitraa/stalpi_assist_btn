"""
Model exported as python.
Name : 005 GENERARE MACHETE XLS_1
Group : LEA JT
With QGIS : 33802
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class GenerareMacheteXls_1(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('linie', 'LINIE', types=[QgsProcessing.TypeVector], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('stalp_xml_', 'STALP_XML_', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('tronson_aranjat_', 'TRONSON_ARANJAT_', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('tronson_xml_', 'TRONSON_XML_', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Aux_tr', 'AUX_tr', type=QgsProcessing.TypeVectorLine, createByDefault=True, supportsAppend=True, defaultValue='TEMPORARY_OUTPUT'))
        self.addParameter(QgsProcessingParameterFeatureSink('Linie_macheta', 'LINIE_MACHETA', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue='TEMPORARY_OUTPUT'))
        self.addParameter(QgsProcessingParameterFeatureSink('StalpiMacheta', 'STALPI MACHETA', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue='TEMPORARY_OUTPUT'))
        self.addParameter(QgsProcessingParameterFeatureSink('TronsonMacheta', 'TRONSON MACHETA', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(12, model_feedback)
        results = {}
        outputs = {}

        # Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'ID_LOC',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'ID_BDI',
            'INPUT': parameters['tronson_aranjat_'],
            'INPUT_2': parameters['linie'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Refactor TRONSON JT
        alg_params = {
            'FIELDS_MAPPING': [{'alias': None,'comment': None,'expression': '"NR_CRT"','length': 0,'name': 'Nr. crt','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID"','length': 0,'name': 'ID','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DENUM"','length': 0,'name': 'Denumire','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '\'TR \' || "DENUM"','length': 0,'name': 'Descrierea BDI','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"PROP"','length': 0,'name': 'Proprietar','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_LOC"','length': 0,'name': 'ID_Locatia','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DENUM_2"','length': 0,'name': 'Locatia','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_INC_TR"','length': 0,'name': 'Nr.crt_Inceput de tronson','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Inceput de tronson"','length': 0,'name': 'Inceput de tronson','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_FIN_TR"','length': 0,'name': 'Nr.crt_Final de tronson','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Final de tronson"','length': 0,'name': 'Final de tronson','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_TR"','length': 0,'name': 'Tipul tronsonului','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_COND"','length': 0,'name': 'Tip conductor','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"LUNG_TR"','length': 0,'name': 'Lungimea tronsonului (km)','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"GEO"','length': 0,'name': 'Geometrie','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"SURSA_COORD"','length': 0,'name': 'Sursa coordonate','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DATA_COORD"','length': 0,'name': 'Data actualizarii coordonatelor','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"UNIT_LOG_INT"','length': 0,'name': 'Unitate logistica de intretinere','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"S_UNIT_LOG"','length': 0,'name': 'Sectie unitate logistica','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"POST_LUC"','length': 0,'name': 'Post de lucru','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Observatii"','length': 0,'name': 'Observatii','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'}],
            'INPUT': outputs['JoinAttributesByFieldValue']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RefactorTronsonJt'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Refactor STALPI
        alg_params = {
            'FIELDS_MAPPING': [{'alias': None,'comment': None,'expression': '"NR_CRT"','length': 0,'name': 'Nr crt','precision': 0,'sub_type': 0,'type': 4,'type_name': 'int8'},{'alias': None,'comment': None,'expression': 'concat(coalesce("ID_LINIE_JT_1", \'\'), \r\n       if("ID_LINIE_JT_2" is not null, \',\' || "ID_LINIE_JT_2", \'\'), \r\n       if("ID_LINIE_JT_3" is not null, \',\' || "ID_LINIE_JT_3", \'\'), \r\n       if("ID_LINIE_JT_4" is not null, \',\' || "ID_LINIE_JT_4", \'\'), \r\n       if("ID_LINIE_JT_5" is not null, \',\' || "ID_LINIE_JT_5", \'\'), \r\n       if("ID_LINIE_JT_6" is not null, \',\' || "ID_LINIE_JT_6", \'\'), \r\n       if("ID_LINIE_JT_7" is not null, \',\' || "ID_LINIE_JT_7", \'\'))\r\n','length': 0,'name': 'ID_linie JT','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DENUM"','length': 0,'name': 'Denumire','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '\'STP.\' ||\' \'  || "DENUM" || \' \' || "STR"','length': 0,'name': 'Descrierea BDI','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_INS_STP"','length': 0,'name': 'Numar inscriptionat pe stalp','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DESC_DET"','length': 0,'name': 'Descriere detaliata','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"PROP"','length': 0,'name': 'Proprietar','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DET_PROP"','length': 0,'name': 'Detaliere Proprietar','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_ZONA_AMP"','length': 0,'name': 'Tip zona de amplasare','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"JUD"','length': 0,'name': 'Judet','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"PRIM"','length': 0,'name': 'Primarie','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"LOC"','length': 0,'name': 'Localitate','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_STR"','length': 0,'name': 'Tip strada','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"STR"','length': 0,'name': 'Strada','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_CIR"','length': 0,'name': 'Tip circuit','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_MAT"','length': 0,'name': 'Tip material','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DESC_CTG_MT_JT"','length': 0,'name': 'Descriere catalog MT, JT','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CIR"','length': 0,'name': 'Numar circuite','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Defecte stalp"','length': 0,'name': 'Defecte stalp','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_FUND"','length': 0,'name': 'Tipul fundatiei','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"OBS_FUND"','length': 0,'name': 'Observatii fundatie','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ANC"','length': 0,'name': 'Ancora','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"OBS_ANC"','length': 0,'name': 'Observatii ancora','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Adaos"','length': 0,'name': 'Adaos','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"OBS_ADAOS"','length': 0,'name': 'Observatii adaos','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"FIB_OPT"','length': 0,'name': 'Fibra optica','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CIR_FO"','length': 0,'name': 'Numar circuite FO','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"PROP_FO"','length': 0,'name': 'Proprietar FO','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"LTC"','length': 0,'name': 'LTC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CIR_LTC"','length': 0,'name': 'Numar circuite LTC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"PROP_LTC"','length': 0,'name': 'Proprietar LTC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"CATV"','length': 0,'name': 'CATV','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CIR_CATV"','length': 0,'name': 'Numar circuite CATV','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"PROP_CATV"','length': 0,'name': 'Proprietar CATV','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ECHIP_COM"','length': 0,'name': 'Echipamente comunicatii ','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DISP_CUIB_PAS"','length': 0,'name': 'Dispozitiv cuib pasari','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CONS_C2S"','length': 0,'name': 'Tipul de consola','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_LEG_JT"','length': 0,'name': 'Tip legaturi JT','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"PRIZA_LEG_PAM"','length': 0,'name': 'Priza de legare la pamant','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"CORP_IL"','length': 0,'name': 'Corp iluminat','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"CUTIE_SEL"','length': 0,'name': 'Cutie selectivitate/cutie sectionare','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"LAT"','length': 0,'name': 'Latitudine (grade zecimale)','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"LONG"','length': 0,'name': 'Longitudine (grade zecimale)','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ALT"','length': 0,'name': 'Altitudine (m)','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"X_STEREO_70"','length': 0,'name': 'x - STEREO 70 (m)','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Y_STEREO_70"','length': 0,'name': 'y - STEREO 70 (m)','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Z_STEREO_70"','length': 0,'name': 'z - STEREO 70 (m)','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"GEO"','length': 0,'name': 'Geometrie','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"SURSA_COORD"','length': 0,'name': 'Sursa coordonate','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DATA_COORD"','length': 0,'name': 'Data actualizarii coordonatelor','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"OBS"','length': 0,'name': 'Observatii','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'}],
            'INPUT': parameters['stalp_xml_'],
            'OUTPUT': parameters['StalpiMacheta']
        }
        outputs['RefactorStalpi'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['StalpiMacheta'] = outputs['RefactorStalpi']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Refactor fields tr cu nr crt text
        alg_params = {
            'FIELDS_MAPPING': [{'alias': None,'comment': None,'expression': '"NR_CRT"','length': 0,'name': 'NR_CRT','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'}],
            'INPUT': parameters['tronson_xml_'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RefactorFieldsTrCuNrCrtText'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Refactor LINIE JT
        alg_params = {
            'FIELDS_MAPPING': [{'alias': None,'comment': None,'expression': '"ID_BDI"','length': 0,'name': 'ID','precision': 0,'sub_type': 0,'type': 6,'type_name': 'double precision'},{'alias': None,'comment': None,'expression': None,'length': 0,'name': 'Denumire','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DENUM"','length': 0,'name': 'Descrierea BDI','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': "'DEER'",'length': 0,'name': 'Proprietar','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Locatia"','length': 0,'name': 'Locatia','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Descrierea instalatiei superioare"','length': 0,'name': 'Descrierea instalatiei superioare','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Nivel tensiune (kV)"','length': 0,'name': 'Nivel tensiune (kV)','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Tipul liniei"','length': 0,'name': 'Tipul liniei','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'}],
            'INPUT': parameters['linie'],
            'OUTPUT': parameters['Linie_macheta']
        }
        outputs['RefactorLinieJt'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Linie_macheta'] = outputs['RefactorLinieJt']['OUTPUT']

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Join attributes STALP INCEPUT
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'Nr.crt_Inceput de tronson',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'Nr crt',
            'INPUT': outputs['RefactorTronsonJt']['OUTPUT'],
            'INPUT_2': outputs['RefactorStalpi']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesStalpInceput'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Field calculator stalp inceput
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'Inceput de tronson',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': '"Descrierea BDI_2"',
            'INPUT': outputs['JoinAttributesStalpInceput']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorStalpInceput'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Join attributes STALP SFARSIT
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'Nr.crt_Final de tronson',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'Nr crt',
            'INPUT': outputs['FieldCalculatorStalpInceput']['OUTPUT'],
            'INPUT_2': outputs['RefactorStalpi']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesStalpSfarsit'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Field calculator stalp sfarsit
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'Final de tronson',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': '"Descrierea BDI_3"',
            'INPUT': outputs['JoinAttributesStalpSfarsit']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorStalpSfarsit'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Refactor fields tronson
        alg_params = {
            'FIELDS_MAPPING': [{'alias': None,'comment': None,'expression': '"Nr. crt"','length': 0,'name': 'Nr. crt','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID"','length': 0,'name': 'ID','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Denumire"','length': 0,'name': 'Denumire','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Descrierea BDI"','length': 0,'name': 'Descrierea BDI','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Proprietar"','length': 0,'name': 'Proprietar','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_Locatia"','length': 0,'name': 'ID_Locatia','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Locatia"','length': 0,'name': 'Locatia','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Nr.crt_Inceput de tronson"','length': 0,'name': 'Nr.crt_Inceput de tronson','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'substr("Denumire", 1, strpos("Denumire", \' - \') - 1)\r\n','length': 0,'name': 'Inceput de tronson','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Nr.crt_Final de tronson"','length': 0,'name': 'Nr.crt_Final de tronson','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'substr("Denumire", strpos("Denumire", \' - \') + 3)\r\n','length': 0,'name': 'Final de tronson','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Tipul tronsonului"','length': 0,'name': 'Tipul tronsonului','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Tip conductor"','length': 0,'name': 'Tip conductor','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Lungimea tronsonului (km)"','length': 0,'name': 'Lungimea tronsonului (km)','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Geometrie"','length': 0,'name': 'Geometrie','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Sursa coordonate"','length': 0,'name': 'Sursa coordonate','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Data actualizarii coordonatelor"','length': 0,'name': 'Data actualizarii coordonatelor','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Unitate logistica de intretinere"','length': 0,'name': 'Unitate logistica de intretinere','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Sectie unitate logistica"','length': 0,'name': 'Sectie unitate logistica','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Post de lucru"','length': 0,'name': 'Post de lucru','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"Observatii"','length': 0,'name': 'Observatii','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'}],
            'INPUT': outputs['FieldCalculatorStalpSfarsit']['OUTPUT'],
            'OUTPUT': parameters['TronsonMacheta']
        }
        outputs['RefactorFieldsTronson'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['TronsonMacheta'] = outputs['RefactorFieldsTronson']['OUTPUT']

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'NR_CRT',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'Nr. crt',
            'INPUT': outputs['RefactorFieldsTrCuNrCrtText']['OUTPUT'],
            'INPUT_2': outputs['RefactorFieldsTronson']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Explode lines TRONSON prin AX
        alg_params = {
            'INPUT': outputs['JoinAttributesByFieldValue']['OUTPUT'],
            'OUTPUT': parameters['Aux_tr']
        }
        outputs['ExplodeLinesTronsonPrinAx'] = processing.run('native:explodelines', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Aux_tr'] = outputs['ExplodeLinesTronsonPrinAx']['OUTPUT']
        return results

    def name(self):
        return '005 GENERARE MACHETE XLS_1'

    def displayName(self):
        return '005 GENERARE MACHETE XLS_1'

    def group(self):
        return 'LEA JT'

    def groupId(self):
        return 'LEA JT'

    def createInstance(self):
        return GenerareMacheteXls_1()
