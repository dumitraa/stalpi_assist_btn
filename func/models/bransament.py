"""
Model exported as python.
Name : 002 BRANS_FIRI_GR
Group : LEA JT
With QGIS : 33802
"""

from qgis.core import QgsProcessing # type: ignore
from qgis.core import QgsProcessingAlgorithm # type: ignore
from qgis.core import QgsProcessingMultiStepFeedback # type: ignore
from qgis.core import QgsProcessingParameterVectorLayer # type: ignore
from qgis.core import QgsProcessingParameterFeatureSink # type: ignore
from qgis.core import QgsCoordinateReferenceSystem # type: ignore
import os
import processing # type: ignore


class BransamentModel(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('brans_firi_desenate', 'BRANS_FIRI_desenate', defaultValue="BRANS_FIRI_GRPM_JT"))
        self.addParameter(QgsProcessingParameterVectorLayer('fb_pe_c_les', 'FB pe C LES', optional=True, types=[QgsProcessing.TypeVectorPoint], defaultValue="FB pe C LES"))
        self.addParameter(QgsProcessingParameterVectorLayer('linie_jt_introduse', 'LINIE_JT introduse', types=[QgsProcessing.TypeVector], defaultValue="LINIE_JT"))
        self.addParameter(QgsProcessingParameterFeatureSink('BRANSAMENT_XML_', 'BRANSAMENT_XML_', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=os.path.join(self.base_dir, f"BRANSAMENT_XML_.shp")))
        self.addParameter(QgsProcessingParameterFeatureSink('GRUP_MASURA_XML_', 'GRUP_MASURA_XML_', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=os.path.join(self.base_dir, f"GRUP_MASURA_XML_.shp")))
        self.addParameter(QgsProcessingParameterFeatureSink('FIRIDA_XML_', 'FIRIDA_XML_', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=os.path.join(self.base_dir, f"FIRIDA_XML_.shp")))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(42, model_feedback)
        results = {}
        outputs = {}

        # Refactor fields
        alg_params = {
            'FIELDS_MAPPING': [{'alias': None,'comment': None,'expression': '"fid"','length': 0,'name': 'fid','precision': 0,'sub_type': 0,'type': 4,'type_name': 'int8'},{'alias': None,'comment': None,'expression': '2002','length': 0,'name': 'CLASS_ID','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_BDI"','length': 0,'name': 'ID_BDI','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT"','length': 0,'name': 'NR_CRT','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"DENUM"','length': 0,'name': 'DENUM','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '2000','length': 0,'name': 'CLASS_ID_LOC','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_LOC"','length': 0,'name': 'ID_LOC','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"NR_CRT_LOC"','length': 0,'name': 'NR_CRT_LOC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '2018','length': 0,'name': 'CLASS_ID_PLC_BR','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_PLC_BR"','length': 0,'name': 'ID_PLC_BR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'aggregate(\r\n    layer:=\'STALP_JT\',\r\n    aggregate:=\'array_agg\',\r\n    expression:="NR_CRT",\r\n    filter:=intersects($geometry, geometry(@parent))\r\n)[0]','length': 0,'name': 'NR_CRT_PLC_BR','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"TIP_BR"','length': 0,'name': 'TIP_BR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_COND"','length': 0,'name': 'TIP_COND','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'round(length($geometry) , 3)','length': 0,'name': 'LUNG','precision': 3,'sub_type': 0,'type': 6,'type_name': 'double precision'},{'alias': None,'comment': None,'expression': 'aggregate(\r\n    layer:=\'STALP_JT\',\r\n    aggregate:=\'array_agg\',\r\n    expression:="JUD",\r\n    filter:=intersects($geometry, geometry(@parent))\r\n)[0]','length': 0,'name': 'JUD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'aggregate(\r\n    layer:=\'STALP_JT\',\r\n    aggregate:=\'array_agg\',\r\n    expression:="PRIM",\r\n    filter:=intersects($geometry, geometry(@parent))\r\n)[0]','length': 0,'name': 'PRIM','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'aggregate(\r\n    layer:=\'STALP_JT\',\r\n    aggregate:=\'array_agg\',\r\n    expression:="LOC",\r\n    filter:=intersects($geometry, geometry(@parent))\r\n)[0]','length': 0,'name': 'LOC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_STR"','length': 0,'name': 'TIP_STR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'upper("STR")','length': 0,'name': 'STR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'upper ("NR_IMOB")','length': 0,'name': 'NR_IMOB','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': "'Masuratori topo'",'length': 0,'name': 'SURSA_COORD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': "format_date(now(), 'dd.MM.yyyy')",'length': 0,'name': 'DATA_COORD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"OBS"','length': 0,'name': 'OBS','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ETAJ"','length': 10,'name': 'ETAJ','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"AP"','length': 10,'name': 'AP','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"SCARA"','length': 20,'name': 'SCARA','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"LIM_PROP"','length': 25,'name': 'LIM_PROP','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_FIRI_BR"','length': 25,'name': 'TIP_FIRI_BR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"LINIA_JT"','length': 200,'name': 'LINIA_JT','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'}],
            'INPUT': parameters['brans_firi_desenate'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RefactorFields'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Refactor fields FB pe LES
        alg_params = {
            'FIELDS_MAPPING': [{'alias': None,'comment': None,'expression': '"CLASS_ID"','length': 0,'name': 'CLASS_ID','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_BDI"','length': 0,'name': 'ID_BDI','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT"','length': 0,'name': 'NR_CRT','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': ' "STR"  ||\' \'  ||  "NR_IMOB" ','length': 0,'name': 'IDEN','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"CLASS_ID_LOC"','length': 0,'name': 'CLASS_ID_LOC','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_LOC"','length': 0,'name': 'ID_LOC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_LOC"','length': 0,'name': 'NR_CRT_LOC','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"CLASS_ID_LOC"','length': 0,'name': 'CLASS_ID_INST_SUP','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_LOC"','length': 0,'name': 'ID_INST_SUP','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"NR_CRT_INST_SUP"','length': 0,'name': 'NR_CRT_INST_SUP','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"JUD"','length': 0,'name': 'JUD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"PRIM"','length': 0,'name': 'PRIM','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"LOC"','length': 0,'name': 'LOC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_STR"','length': 0,'name': 'TIP_STR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"STR"','length': 0,'name': 'STR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_IMOB" ','length': 0,'name': 'NR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'case when etaj is null then 0\r\nelse "ETAJ"\r\nend','length': 0,'name': 'ETAJ','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': "'de bransament' ",'length': 0,'name': 'ROL_FIRI','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_FIRI_RET"','length': 0,'name': 'TIP_FIRI_RET','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'TIP_FIRI_BR','length': 0,'name': 'TIP_FIRI_BR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"AMPL"','length': 0,'name': 'AMPL','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"MAT"','length': 0,'name': 'MAT','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"LIM_PROP"','length': 0,'name': 'LIM_PROP','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DEF_FIRI"','length': 0,'name': 'DEF_FIRI','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CIR"','length': 0,'name': 'NR_CIR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"AN_FUNC"','length': 0,'name': 'AN_FUNC','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ALT"','length': 0,'name': 'ALT','precision': 4,'sub_type': 0,'type': 6,'type_name': 'double precision'},{'alias': None,'comment': None,'expression': 'round_wkt_coordinates($geometry)','length': 0,'name': 'GEO','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"SURSA_COORD"','length': 0,'name': 'SURSA_COORD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DATA_COORD"','length': 0,'name': 'DATA_COORD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': "round(x(transform($geometry, layer_property(@layer, 'crs'), 'EPSG:4326')), 8)",'length': 0,'name': 'LONG','precision': 8,'sub_type': 0,'type': 6,'type_name': 'double precision'},{'alias': None,'comment': None,'expression': "round(y(transform($geometry, layer_property(@layer, 'crs'), 'EPSG:4326')), 8)",'length': 0,'name': 'LAT','precision': 8,'sub_type': 0,'type': 6,'type_name': 'double precision'},{'alias': None,'comment': None,'expression': 'round(x($geometry), 4)','length': 0,'name': 'X_STEREO_70','precision': 4,'sub_type': 0,'type': 6,'type_name': 'double precision'},{'alias': None,'comment': None,'expression': 'round(y($geometry), 4)','length': 0,'name': 'Y_STEREO_70','precision': 4,'sub_type': 0,'type': 6,'type_name': 'double precision'},{'alias': None,'comment': None,'expression': '"Z_STEREO_70"','length': 0,'name': 'Z_STEREO_70','precision': 4,'sub_type': 0,'type': 6,'type_name': 'double precision'}],
            'INPUT': parameters['fb_pe_c_les'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RefactorFieldsFbPeLes'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'LINIA_JT',
            'FIELDS_TO_COPY': ['ID_BDI'],
            'FIELD_2': 'DENUM',
            'INPUT': outputs['RefactorFields']['OUTPUT'],
            'INPUT_2': parameters['linie_jt_introduse'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # NOD SEPARARE
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'ID_LOC',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer (32 bit)
            'FORMULA': '"ID_BDI_2"',
            'INPUT': outputs['JoinAttributesByFieldValue']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['NodSeparare'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # BRANSAMENTE
        alg_params = {
            'FIELDS_MAPPING': [{'alias': None,'comment': None,'expression': '"CLASS_ID"','length': 0,'name': 'CLASS_ID','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': 'NULL','length': 0,'name': 'ID_BDI','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT"','length': 0,'name': 'NR_CRT','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': ' "STR"  || \' \' ||  "NR_IMOB" ','length': 0,'name': 'DENUM','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"CLASS_ID_LOC"','length': 0,'name': 'CLASS_ID_LOC','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_LOC"','length': 0,'name': 'ID_LOC','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"NR_CRT_LOC"','length': 0,'name': 'NR_CRT_LOC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"CLASS_ID_PLC_BR"','length': 0,'name': 'CLASS_ID_PLC_BR','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_PLC_BR"','length': 0,'name': 'ID_PLC_BR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_PLC_BR"','length': 0,'name': 'NR_CRT_PLC_BR','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"TIP_BR"','length': 0,'name': 'TIP_BR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_COND"','length': 0,'name': 'TIP_COND','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'to_string(format_number("LUNG", 3))\r\n','length': 0,'name': 'LUNG','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"JUD"','length': 0,'name': 'JUD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"PRIM"','length': 0,'name': 'PRIM','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"LOC"','length': 0,'name': 'LOC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_STR"','length': 0,'name': 'TIP_STR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"STR"','length': 0,'name': 'STR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_IMOB"','length': 0,'name': 'NR_IMOB','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'round_wkt_coordinates($geometry)','length': 0,'name': 'GEO','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"SURSA_COORD"','length': 0,'name': 'SURSA_COORD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DATA_COORD"','length': 0,'name': 'DATA_COORD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'null','length': 0,'name': 'OBS','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'}],
            'INPUT': outputs['NodSeparare']['OUTPUT'],
            'OUTPUT': parameters['Bransament_xml_']
        }
        outputs['Bransamente'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['BRANSAMENT_XML_'] = outputs['Bransamente']['OUTPUT']

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Extract specific vertices
        alg_params = {
            'INPUT': outputs['NodSeparare']['OUTPUT'],
            'VERTICES': '-1',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractSpecificVertices'] = processing.run('native:extractspecificvertices', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Refactor FIRIDA_BRANS222
        alg_params = {
            'FIELDS_MAPPING': [{'alias': None,'comment': None,'expression': '2003','length': 0,'name': 'CLASS_ID','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': 'NULL','length': 0,'name': 'ID_BDI','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT"','length': 0,'name': 'NR_CRT','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': ' "STR"  ||\' \'  ||  "NR_IMOB" ','length': 0,'name': 'IDEN','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '2002','length': 0,'name': 'CLASS_ID_LOC','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': 'NULL','length': 0,'name': 'ID_LOC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT"','length': 0,'name': 'NR_CRT_LOC','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '2000','length': 0,'name': 'CLASS_ID_INST_SUP','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': ' "ID_LOC"\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n','length': 0,'name': 'ID_INST_SUP','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"NR_CRT_INST_SUP"','length': 0,'name': 'NR_CRT_INST_SUP','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"JUD"','length': 0,'name': 'JUD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"PRIM"','length': 0,'name': 'PRIM','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"LOC"','length': 0,'name': 'LOC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_STR"','length': 0,'name': 'TIP_STR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"STR"','length': 0,'name': 'STR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_IMOB"','length': 0,'name': 'NR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'case \r\n     when  "ETAJ" is null then 0\r\n\t else "ETAJ"\r\n\t end','length': 0,'name': 'ETAJ','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': "'de bransament'",'length': 0,'name': 'ROL_FIRI','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_FIRI_RET"','length': 0,'name': 'TIP_FIRI_RET','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_FIRI_BR"','length': 0,'name': 'TIP_FIRI_BR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"AMPL"','length': 0,'name': 'AMPL','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"MAT"','length': 0,'name': 'MAT','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"LIM_PROP"','length': 0,'name': 'LIM_PROP','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DEF_FIRI"','length': 0,'name': 'DEF_FIRI','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CIR"','length': 0,'name': 'NR_CIR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '0','length': 0,'name': 'AN_FUNC','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '0','length': 0,'name': 'ALT','precision': 8,'sub_type': 0,'type': 6,'type_name': 'double precision'},{'alias': None,'comment': None,'expression': 'round_wkt_coordinates($geometry)','length': 0,'name': 'GEO','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"SURSA_COORD"','length': 0,'name': 'SURSA_COORD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DATA_COORD"','length': 0,'name': 'DATA_COORD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': "round(x(transform($geometry, layer_property(@layer, 'crs'), 'EPSG:4326')), 8)",'length': 0,'name': 'LONG','precision': 8,'sub_type': 0,'type': 6,'type_name': 'double precision'},{'alias': None,'comment': None,'expression': "round(y(transform($geometry, layer_property(@layer, 'crs'), 'EPSG:4326')), 8)",'length': 0,'name': 'LAT','precision': 8,'sub_type': 0,'type': 6,'type_name': 'double precision'},{'alias': None,'comment': None,'expression': 'to_string(format_number((round(x($geometry), 4)), 4))','length': 0,'name': 'X_STEREO_70','precision': 4,'sub_type': 0,'type': 6,'type_name': 'double precision'},{'alias': None,'comment': None,'expression': 'to_string(format_number((round(y($geometry), 4)), 4))','length': 0,'name': 'Y_STEREO_70','precision': 4,'sub_type': 0,'type': 6,'type_name': 'double precision'},{'alias': None,'comment': None,'expression': '0.0000','length': 0,'name': 'Z_STEREO_70','precision': 4,'sub_type': 0,'type': 6,'type_name': 'double precision'},{'alias': None,'comment': None,'expression': 'OBS','length': 0,'name': 'OBS','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'}],
            'INPUT': outputs['ExtractSpecificVertices']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RefactorFirida_brans222'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Field calculator INST SUP pt 
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'ID_INST_SUP',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': 'case when "ID_INST_SUP" is null then \r\n (aggregate(\r\n    layer:=\'TRONSON_XML_\',\r\n    aggregate:=\'array_agg\',\r\n    expression:="ID_LOC",\r\n    filter:=intersects($geometry, geometry(@parent))\r\n)[0])\r\nELSE "ID_INST_SUP"\r\nEND',
            'INPUT': outputs['RefactorFirida_brans222']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorInstSupPt'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # 6 GR_2
        alg_params = {
            'FIELD': 'OBS',
            'INPUT': outputs['FieldCalculatorInstSupPt']['OUTPUT'],
            'OPERATOR': 0,  # =
            'VALUE': '6',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gr_2'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # 7 GR_2
        alg_params = {
            'FIELD': 'OBS',
            'INPUT': outputs['FieldCalculatorInstSupPt']['OUTPUT'],
            'OPERATOR': 0,  # =
            'VALUE': '7',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gr_2'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # 3 GR_1
        alg_params = {
            'FIELD': 'OBS',
            'INPUT': outputs['FieldCalculatorInstSupPt']['OUTPUT'],
            'OPERATOR': 0,  # =
            'VALUE': '3',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gr_1'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # 7 GR_6
        alg_params = {
            'FIELD': 'OBS',
            'INPUT': outputs['FieldCalculatorInstSupPt']['OUTPUT'],
            'OPERATOR': 0,  # =
            'VALUE': '7',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gr_6'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # 7 GR_4
        alg_params = {
            'FIELD': 'OBS',
            'INPUT': outputs['FieldCalculatorInstSupPt']['OUTPUT'],
            'OPERATOR': 0,  # =
            'VALUE': '7',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gr_4'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # 7 GR_3
        alg_params = {
            'FIELD': 'OBS',
            'INPUT': outputs['FieldCalculatorInstSupPt']['OUTPUT'],
            'OPERATOR': 0,  # =
            'VALUE': '7',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gr_3'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # 7 GR_5
        alg_params = {
            'FIELD': 'OBS',
            'INPUT': outputs['FieldCalculatorInstSupPt']['OUTPUT'],
            'OPERATOR': 0,  # =
            'VALUE': '7',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gr_5'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # 5 GR_3
        alg_params = {
            'FIELD': 'OBS',
            'INPUT': outputs['FieldCalculatorInstSupPt']['OUTPUT'],
            'OPERATOR': 0,  # =
            'VALUE': '5',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gr_3'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # 4 GR_1
        alg_params = {
            'FIELD': 'OBS',
            'INPUT': outputs['FieldCalculatorInstSupPt']['OUTPUT'],
            'OPERATOR': 0,  # =
            'VALUE': '4',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gr_1'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # 4 GR_3
        alg_params = {
            'FIELD': 'OBS',
            'INPUT': outputs['FieldCalculatorInstSupPt']['OUTPUT'],
            'OPERATOR': 0,  # =
            'VALUE': '4',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gr_3'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # 6 GR_1
        alg_params = {
            'FIELD': 'OBS',
            'INPUT': outputs['FieldCalculatorInstSupPt']['OUTPUT'],
            'OPERATOR': 0,  # =
            'VALUE': '6',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gr_1'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # 2 GR
        alg_params = {
            'FIELD': 'OBS',
            'INPUT': outputs['FieldCalculatorInstSupPt']['OUTPUT'],
            'OPERATOR': 0,  # =
            'VALUE': '2',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gr'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # 6 GR_4
        alg_params = {
            'FIELD': 'OBS',
            'INPUT': outputs['FieldCalculatorInstSupPt']['OUTPUT'],
            'OPERATOR': 0,  # =
            'VALUE': '6',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gr_4'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}

        # 5 GR_4
        alg_params = {
            'FIELD': 'OBS',
            'INPUT': outputs['FieldCalculatorInstSupPt']['OUTPUT'],
            'OPERATOR': 0,  # =
            'VALUE': '5',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gr_4'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(22)
        if feedback.isCanceled():
            return {}

        # 7 GR_1
        alg_params = {
            'FIELD': 'OBS',
            'INPUT': outputs['FieldCalculatorInstSupPt']['OUTPUT'],
            'OPERATOR': 0,  # =
            'VALUE': '7',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gr_1'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(23)
        if feedback.isCanceled():
            return {}

        # 4 GR_2
        alg_params = {
            'FIELD': 'OBS',
            'INPUT': outputs['FieldCalculatorInstSupPt']['OUTPUT'],
            'OPERATOR': 0,  # =
            'VALUE': '4',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gr_2'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(24)
        if feedback.isCanceled():
            return {}

        # 5 GR_1
        alg_params = {
            'FIELD': 'OBS',
            'INPUT': outputs['FieldCalculatorInstSupPt']['OUTPUT'],
            'OPERATOR': 0,  # =
            'VALUE': '5',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gr_1'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(25)
        if feedback.isCanceled():
            return {}

        # Merge vector layers FB pe LES cu FB
        alg_params = {
            'CRS': QgsCoordinateReferenceSystem('EPSG:3844'),
            'LAYERS': [outputs['RefactorFieldsFbPeLes']['OUTPUT'],outputs['FieldCalculatorInstSupPt']['OUTPUT']],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MergeVectorLayersFbPeLesCuFb'] = processing.run('native:mergevectorlayers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(26)
        if feedback.isCanceled():
            return {}

        # 3 GR_2
        alg_params = {
            'FIELD': 'OBS',
            'INPUT': outputs['FieldCalculatorInstSupPt']['OUTPUT'],
            'OPERATOR': 0,  # =
            'VALUE': '3',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gr_2'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(27)
        if feedback.isCanceled():
            return {}

        # 5 GR_2
        alg_params = {
            'FIELD': 'OBS',
            'INPUT': outputs['FieldCalculatorInstSupPt']['OUTPUT'],
            'OPERATOR': 0,  # =
            'VALUE': '5',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gr_2'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(28)
        if feedback.isCanceled():
            return {}

        # 6 GR_5
        alg_params = {
            'FIELD': 'OBS',
            'INPUT': outputs['FieldCalculatorInstSupPt']['OUTPUT'],
            'OPERATOR': 0,  # =
            'VALUE': '6',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gr_5'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(29)
        if feedback.isCanceled():
            return {}

        # 6 GR_3
        alg_params = {
            'FIELD': 'OBS',
            'INPUT': outputs['FieldCalculatorInstSupPt']['OUTPUT'],
            'OPERATOR': 0,  # =
            'VALUE': '6',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Gr_3'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(30)
        if feedback.isCanceled():
            return {}

        # Merge vector layers FB cu FR
        alg_params = {
            'CRS': QgsCoordinateReferenceSystem('EPSG:3844'),
            'LAYERS': [outputs['MergeVectorLayersFbPeLesCuFb']['OUTPUT'],'FIRIDA_RETEA_d2b48fca_b5ea_46f8_9bfb_dc3f1df4a858'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MergeVectorLayersFbCuFr'] = processing.run('native:mergevectorlayers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(31)
        if feedback.isCanceled():
            return {}

        # GEO 4 ZECIMALE
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GEO',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': '\'POINT (\'|| (replace(format_number("X_STEREO_70", 4), \',\', \'\')) ||\' \'|| (replace(format_number("Y_STEREO_70", 4), \',\', \'\'))||\')\'',
            'INPUT': outputs['MergeVectorLayersFbCuFr']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Geo4Zecimale'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(32)
        if feedback.isCanceled():
            return {}

        # Drop field(s)
        alg_params = {
            'COLUMN': ['layer','fid','path'],
            'INPUT': outputs['Geo4Zecimale']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DropFields'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(33)
        if feedback.isCanceled():
            return {}

        # Merge vector GR MULTIPLE
        alg_params = {
            'CRS': QgsCoordinateReferenceSystem('EPSG:3844'),
            'LAYERS': [outputs['Gr']['OUTPUT'],outputs['Gr_1']['OUTPUT'],outputs['Gr_2']['OUTPUT'],outputs['Gr_1']['OUTPUT'],outputs['Gr_2']['OUTPUT'],outputs['Gr_3']['OUTPUT'],outputs['Gr_1']['OUTPUT'],outputs['Gr_4']['OUTPUT'],outputs['Gr_5']['OUTPUT'],outputs['Gr_4']['OUTPUT'],outputs['Gr_3']['OUTPUT'],outputs['Gr_2']['OUTPUT'],outputs['Gr_1']['OUTPUT'],outputs['Gr_2']['OUTPUT'],outputs['Gr_3']['OUTPUT'],outputs['Gr_4']['OUTPUT'],outputs['Gr_5']['OUTPUT'],outputs['Gr_6']['OUTPUT'],outputs['Gr_1']['OUTPUT'],outputs['Gr_3']['OUTPUT'],outputs['Gr_2']['OUTPUT'],outputs['FieldCalculatorInstSupPt']['OUTPUT'],outputs['RefactorFieldsFbPeLes']['OUTPUT']],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MergeVectorGrMultiple'] = processing.run('native:mergevectorlayers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(34)
        if feedback.isCanceled():
            return {}

        # FR FB an punere in functiune
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'AN_FUNC',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer (32 bit)
            'FORMULA': '2020',
            'INPUT': outputs['DropFields']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FrFbAnPunereInFunctiune'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(35)
        if feedback.isCanceled():
            return {}

        # Field calculator GR pt FB LES
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'NR_CRT_LOC',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': 'CASE WHEN "NR_CRT_LOC" IS NULL THEN "NR_CRT" ELSE "NR_CRT_LOC" END',
            'INPUT': outputs['MergeVectorGrMultiple']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorGrPtFbLes'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(36)
        if feedback.isCanceled():
            return {}

        # CALCUL COTA WGS
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'ALT',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': 'to_string(format_number((overlay_nearest(\r\n      \'poze\' ,\r\n    "altitude",    \r\n    limit := 1  \r\n)[0]  - 2.5), 4))',
            'INPUT': outputs['FrFbAnPunereInFunctiune']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculCotaWgs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(37)
        if feedback.isCanceled():
            return {}

        # Refactor fields
        alg_params = {
            'FIELDS_MAPPING': [{'alias': None,'comment': None,'expression': '2027','length': 0,'name': 'CLASS_ID','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': 'NULL','length': 0,'name': 'ID_BDI','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': ' $id ','length': 0,'name': 'NR_CRT','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"STR" || \' \' || "NR"','length': 0,'name': 'DENUM','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '2003','length': 0,'name': 'CLASS_ID_LOC','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': 'null','length': 0,'name': 'ID_LOC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_LOC"','length': 0,'name': 'NR_CRT_LOC','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '2000','length': 0,'name': 'CLASS_ID_INST_SUP','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_INST_SUP"','length': 0,'name': 'ID_INST_SUP','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"NR_CRT_INST_SUP"','length': 0,'name': 'NR_CRT_INST_SUP','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"JUD"','length': 0,'name': 'JUD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"PRIM"','length': 0,'name': 'PRIM','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"LOC"','length': 0,'name': 'LOC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_STR"','length': 0,'name': 'TIP_STR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"STR"','length': 0,'name': 'STR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR"','length': 0,'name': 'NR_SCARA','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'case \r\n     when  "ETAJ" is null then 0\r\n\t else "ETAJ"\r\n\t end','length': 0,'name': 'ETAJ','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'case \r\n     when  "AP" is null then 0\r\n\t else "AP"\r\n\t end','length': 0,'name': 'AP','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'}],
            'INPUT': outputs['FieldCalculatorGrPtFbLes']['OUTPUT'],
            'OUTPUT': parameters['Grup_masura_xml_']
        }
        outputs['RefactorFields'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['GRUP_MASURA_XML_'] = outputs['RefactorFields']['OUTPUT']

        feedback.setCurrentStep(38)
        if feedback.isCanceled():
            return {}

        # CALCUL COTA MAREA NEAGRA
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Z_STEREO_70',
            'FIELD_PRECISION': 4,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': 'to_string(format_number((overlay_nearest(\r\n      \'poze\' ,\r\n    "altitude",    \r\n    limit := 1  \r\n)[0]  - 2.5) - \r\n(overlay_nearest(\r\n      \'GRID_GEOID\' ,\r\n    "VALUE",    \r\n    limit := 1  \r\n)[0]), 4))',
            'INPUT': outputs['CalculCotaWgs']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculCotaMareaNeagra'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(39)
        if feedback.isCanceled():
            return {}

        # obs
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'OBS',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': 'NULL',
            'INPUT': outputs['CalculCotaMareaNeagra']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Obs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(40)
        if feedback.isCanceled():
            return {}

        # Drop field(s)
        alg_params = {
            'COLUMN': ['OBS'],
            'INPUT': outputs['Obs']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DropFields'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(41)
        if feedback.isCanceled():
            return {}

        # Refactor fields
        alg_params = {
            'FIELDS_MAPPING': [{'alias': None,'comment': None,'expression': '"CLASS_ID"','length': 0,'name': 'CLASS_ID','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_BDI"','length': 0,'name': 'ID_BDI','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT"','length': 0,'name': 'NR_CRT','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"IDEN"','length': 0,'name': 'IDEN','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"CLASS_ID_LOC"','length': 0,'name': 'CLASS_ID_LOC','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_LOC"','length': 0,'name': 'ID_LOC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_LOC"','length': 0,'name': 'NR_CRT_LOC','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"CLASS_ID_INST_SUP"','length': 0,'name': 'CLASS_ID_INST_SUP','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_INST_SUP"','length': 0,'name': 'ID_INST_SUP','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"NR_CRT_INST_SUP"','length': 0,'name': 'NR_CRT_INST_SUP','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"JUD"','length': 0,'name': 'JUD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"PRIM"','length': 0,'name': 'PRIM','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"LOC"','length': 0,'name': 'LOC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_STR"','length': 0,'name': 'TIP_STR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"STR"','length': 0,'name': 'STR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR"','length': 0,'name': 'NR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '\r\ncase \r\n     when  "ETAJ" is null then 0\r\n\t else "ETAJ"\r\n\t end','length': 0,'name': 'ETAJ','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ROL_FIRI"','length': 0,'name': 'ROL_FIRI','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_FIRI_RET"','length': 0,'name': 'TIP_FIRI_RET','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_FIRI_BR"','length': 0,'name': 'TIP_FIRI_BR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"AMPL"','length': 0,'name': 'AMPL','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"MAT"','length': 0,'name': 'MAT','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"LIM_PROP"','length': 0,'name': 'LIM_PROP','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DEF_FIRI"','length': 0,'name': 'DEF_FIRI','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CIR"','length': 0,'name': 'NR_CIR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"AN_FUNC"','length': 0,'name': 'AN_FUNC','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': 'to_string(format_number("ALT", 4))','length': 0,'name': 'ALT','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"GEO"','length': 0,'name': 'GEO','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"SURSA_COORD"','length': 0,'name': 'SURSA_COORD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DATA_COORD"','length': 0,'name': 'DATA_COORD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'to_string(format_number("LONG", 8))','length': 0,'name': 'LONG','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'to_string(format_number("LAT", 8))','length': 0,'name': 'LAT','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': "replace(format_number($x, 4), ',', '')\r\n\r\n\r\n\r\n",'length': 0,'name': 'X_STEREO_70','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': "replace(format_number($y, 4), ',', '')\r\n",'length': 0,'name': 'Y_STEREO_70','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'to_string(format_number("Z_STEREO_70", 4))','length': 0,'name': 'Z_STEREO_70','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'}]
            'INPUT': outputs['DropFields']['OUTPUT'],
            'OUTPUT': parameters['Firida_xml_']
        }
        outputs['RefactorFields'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['FIRIDA_XML_'] = outputs['RefactorFields']['OUTPUT']
        return results

    def name(self):
        return '002_BRANS_FIRI_GR'

    def displayName(self):
        return '002_BRANS_FIRI_GR'

    def group(self):
        return 'LEA JT'

    def groupId(self):
        return 'LEA JT'

    def createInstance(self):
        return BransamentModel()
