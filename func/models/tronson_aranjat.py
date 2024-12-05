"""
Model exported as python.
Name : TRONSOANE DUBLE ACTUALIZARE
Group : 
With QGIS : 33802
"""

from qgis.core import QgsProcessing # type: ignore
from qgis.core import QgsProcessingAlgorithm # type: ignore
from qgis.core import QgsProcessingMultiStepFeedback # type: ignore
from qgis.core import QgsProcessingParameterVectorLayer # type: ignore
from qgis.core import QgsProcessingParameterFeatureSink # type: ignore
import processing # type: ignore


class TronsonAranjatModel(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('tronson_aranjat', 'TRONSON ARANJAT', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('TRONSON_predare_xml', 'TRONSON_predare_xml', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue='TEMPORARY_OUTPUT'))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        # Refactor fields
        alg_params = {
            'FIELDS_MAPPING': [{'alias': None,'comment': None,'expression': '"CLASS_ID"','length': 0,'name': 'CLASS_ID','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_BDI"','length': 0,'name': 'ID_BDI','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT"','length': 0,'name': 'NR_CRT','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"DENUM"','length': 0,'name': 'DENUM','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"PROP"','length': 0,'name': 'PROP','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"CLASS_ID_LOC"','length': 0,'name': 'CLASS_ID_LOC','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_LOC"','length': 0,'name': 'ID_LOC','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"NR_CRT_LOC"','length': 0,'name': 'NR_CRT_LOC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"CLASS_ID_INC_TR"','length': 0,'name': 'CLASS_ID_INC_TR','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_INC_TR"','length': 0,'name': 'ID_INC_TR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_INC_TR"','length': 0,'name': 'NR_CRT_INC_TR','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"CLASS_ID_FIN_TR"','length': 0,'name': 'CLASS_ID_FIN_TR','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_FIN_TR"','length': 0,'name': 'ID_FIN_TR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_FIN_TR"','length': 0,'name': 'NR_CRT_FIN_TR','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"TIP_TR"','length': 0,'name': 'TIP_TR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_COND"','length': 0,'name': 'TIP_COND','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'to_string(format_number((length($geometry)/1000), 3))','length': 0,'name': 'LUNG_TR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'round_wkt_coordinates($geometry)','length': 0,'name': 'GEO','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"SURSA_COORD"','length': 0,'name': 'SURSA_COORD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DATA_COORD"','length': 0,'name': 'DATA_COORD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"UNIT_LOG_INT"','length': 0,'name': 'UNIT_LOG_INT','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"S_UNIT_LOG"','length': 0,'name': 'S_UNIT_LOG','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"POST_LUC"','length': 0,'name': 'POST_LUC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"OBS"','length': 0,'name': 'OBS','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'}],
            'INPUT': parameters['tronson_aranjat'],
            'OUTPUT': parameters['TRONSON_predare_xml']
        }
        outputs['RefactorFields'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['TRONSON_predare_xml'] = outputs['RefactorFields']['OUTPUT']
        return results

    def name(self):
        return 'TRONSOANE_DUBLE_ACTUALIZARE'

    def displayName(self):
        return 'TRONSOANE_DUBLE_ACTUALIZARE'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return TronsonAranjatModel()
