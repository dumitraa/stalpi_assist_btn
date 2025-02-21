"""
Model exported as python.
Name : 004 DESCHIDERI JT
Group : LEA JT
With QGIS : 33802
"""

from qgis.core import QgsProcessing # type: ignore
from qgis.core import QgsProcessingAlgorithm # type: ignore
from qgis.core import QgsProcessingMultiStepFeedback # type: ignore
from qgis.core import QgsProcessingParameterVectorLayer # type: ignore
from qgis.core import QgsProcessingParameterFeatureSink # type: ignore
import processing # type: ignore


class DeschideriJTModel(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('stalpi_desenati', 'STALPI DESENATI', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('tronson_jt', 'Tronson JT', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('DESCHIDERI_XML_', 'DESCHIDERI_XML_', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('SCR_DWG', 'SCR_DWG', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue='TEMPORARY_OUTPUT'))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(19, model_feedback)
        results = {}
        outputs = {}

        # Add geometry attributes
        alg_params = {
            'CALC_METHOD': 0,  # Layer CRS
            'INPUT': parameters['stalpi_desenati'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddGeometryAttributes'] = processing.run('qgis:exportaddgeometrycolumns', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Retain fields
        alg_params = {
            'FIELDS': ['xcoord','ycoord'],
            'INPUT': outputs['AddGeometryAttributes']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RetainFields'] = processing.run('native:retainfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Refactor fields
        alg_params = {
            'FIELDS_MAPPING': [{'alias': None,'comment': None,'expression': '\'-INSERT STALPDEER \' ||  "xcoord"  || \',\' ||  "ycoord"  || \' 1 1 0\'','length': 0,'name': 'SCR_STLP','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'}],
            'INPUT': outputs['RetainFields']['OUTPUT'],
            'OUTPUT': parameters['Scr_dwg']
        }
        outputs['RefactorFields'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['SCR_DWG'] = outputs['RefactorFields']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Buffer
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 0.1,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': parameters['stalpi_desenati'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 5,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Buffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Extract by attribute
        alg_params = {
            'FIELD': 'TIP_TR',
            'INPUT': parameters['tronson_jt'],
            'OPERATOR': 7,  # contains
            'VALUE': 'LEA',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractByAttribute'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # LEA IL
        alg_params = {
            'FIELD': 'TIP_TR',
            'INPUT': outputs['ExtractByAttribute']['OUTPUT'],
            'OPERATOR': 10,  # does not contain
            'VALUE': 'LEA IL',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['LeaIl'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Explode lines
        alg_params = {
            'INPUT': outputs['LeaIl']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExplodeLines'] = processing.run('native:explodelines', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Refactor fields
        alg_params = {
            'FIELDS_MAPPING': [{'alias': None,'comment': None,'expression': "'2015'",'length': 0,'name': 'CLASS_ID','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_BDI"','length': 0,'name': 'ID_BDI','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '@id','length': 0,'name': 'NR_CRT','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '(\'STP. \' + aggregate( \r\n\r\nlayer:=\'STALP_JT\',\r\n    aggregate:=\'array_agg\',\r\n    expression:="DENUM",\r\n    filter:=intersects($geometry, geometry(@parent))\r\n)[0])\r\n\r\n || \' - \'  || \r\n \r\n (\'STP. \' + aggregate( \r\n\r\nlayer:=\'STALP_JT\',\r\n    aggregate:=\'array_agg\',\r\n    expression:="DENUM",\r\n    filter:=intersects($geometry, geometry(@parent))\r\n)[-1])','length': 0,'name': 'DENUM','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_STP_INC"','length': 0,'name': 'ID_STP_INC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'aggregate(\r\n    layer:=\'STALP_JT\',\r\n    aggregate:=\'array_agg\',\r\n    expression:="NR_CRT",\r\n    filter:=intersects($geometry, geometry(@parent))\r\n)[0]','length': 0,'name': 'NR_CRT_STP_INC','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_STP_TERM"','length': 0,'name': 'ID_STP_TERM','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'aggregate(\r\n    layer:=\'STALP_JT\',\r\n    aggregate:=\'array_agg\',\r\n    expression:="NR_CRT",\r\n    filter:=intersects($geometry, geometry(@parent))\r\n)[-1]','length': 0,'name': 'NR_CRT_STP_TERM','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_TR_JT1"','length': 0,'name': 'ID_TR_JT1','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT"','length': 0,'name': 'NR_CRT_TR_JT1','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_TR_JT2"','length': 0,'name': 'ID_TR_JT2','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_TR_JT2"','length': 0,'name': 'NR_CRT_TR_JT2','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_TR_JT3"','length': 0,'name': 'ID_TR_JT3','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_TR_JT3"','length': 0,'name': 'NR_CRT_TR_JT3','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_TR_JT4"','length': 0,'name': 'ID_TR_JT4','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_TR_JT4"','length': 0,'name': 'NR_CRT_TR_JT4','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_TR_JT5"','length': 0,'name': 'ID_TR_JT5','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_TR_JT5"','length': 0,'name': 'NR_CRT_TR_JT5','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_TR_JT6"','length': 0,'name': 'ID_TR_JT6','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_TR_JT6"','length': 0,'name': 'NR_CRT_TR_JT6','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'upper (geom_to_wkt($geometry))','length': 0,'name': 'GEO','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'round(length($geometry) , 3)','length': 0,'name': 'LUNG','precision': 0,'sub_type': 0,'type': 6,'type_name': 'double precision'},{'alias': None,'comment': None,'expression': '"SURSA_COORD"','length': 0,'name': 'SURSA_COORD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DATA_COORD"','length': 0,'name': 'DATA_COORD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT"','length': 0,'name': 'TRCOLLECT','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'}],
            'INPUT': outputs['ExplodeLines']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RefactorFields'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Aggregate
        alg_params = {
            'AGGREGATES': [{'aggregate': 'first_value','delimiter': None,'input': '"CLASS_ID"','length': 0,'name': 'CLASS_ID','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'aggregate': 'first_value','delimiter': None,'input': '"ID_BDI"','length': 0,'name': 'ID_BDI','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'aggregate': 'first_value','delimiter': None,'input': '"NR_CRT"','length': 0,'name': 'NR_CRT','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'aggregate': 'first_value','delimiter': None,'input': '"DENUM"','length': 0,'name': 'DENUM','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'aggregate': 'first_value','delimiter': None,'input': '"ID_STP_INC"','length': 0,'name': 'ID_STP_INC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'aggregate': 'first_value','delimiter': None,'input': '"NR_CRT_STP_INC"','length': 0,'name': 'NR_CRT_STP_INC','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'aggregate': 'first_value','delimiter': None,'input': '"ID_STP_TERM"','length': 0,'name': 'ID_STP_TERM','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'aggregate': 'first_value','delimiter': None,'input': '"NR_CRT_STP_TERM"','length': 0,'name': 'NR_CRT_STP_TERM','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'aggregate': 'first_value','delimiter': None,'input': '"ID_TR_JT1"','length': 0,'name': 'ID_TR_JT1','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'aggregate': 'first_value','delimiter': None,'input': '"NR_CRT_TR_JT1"','length': 20,'name': 'NR_CRT_TR_JT1','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'aggregate': 'first_value','delimiter': None,'input': '"ID_TR_JT2"','length': 0,'name': 'ID_TR_JT2','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'aggregate': 'first_value','delimiter': None,'input': '"NR_CRT_TR_JT2"','length': 0,'name': 'NR_CRT_TR_JT2','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'aggregate': 'first_value','delimiter': None,'input': '"ID_TR_JT3"','length': 0,'name': 'ID_TR_JT3','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'aggregate': 'first_value','delimiter': None,'input': '"NR_CRT_TR_JT3"','length': 0,'name': 'NR_CRT_TR_JT3','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'aggregate': 'first_value','delimiter': None,'input': '"ID_TR_JT4"','length': 0,'name': 'ID_TR_JT4','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'aggregate': 'first_value','delimiter': None,'input': '"NR_CRT_TR_JT4"','length': 0,'name': 'NR_CRT_TR_JT4','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'aggregate': 'first_value','delimiter': None,'input': '"ID_TR_JT5"','length': 0,'name': 'ID_TR_JT5','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'aggregate': 'first_value','delimiter': None,'input': '"NR_CRT_TR_JT5"','length': 0,'name': 'NR_CRT_TR_JT5','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'aggregate': 'first_value','delimiter': None,'input': '"ID_TR_JT6"','length': 0,'name': 'ID_TR_JT6','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'aggregate': 'first_value','delimiter': None,'input': '"NR_CRT_TR_JT6"','length': 0,'name': 'NR_CRT_TR_JT6','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'aggregate': 'first_value','delimiter': None,'input': '"GEO"','length': 0,'name': 'GEO','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'aggregate': 'first_value','delimiter': None,'input': '"LUNG"','length': 0,'name': 'LUNG','precision': 0,'sub_type': 0,'type': 6,'type_name': 'double precision'},{'aggregate': 'first_value','delimiter': None,'input': '"SURSA_COORD"','length': 0,'name': 'SURSA_COORD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'aggregate': 'first_value','delimiter': None,'input': '"DATA_COORD"','length': 0,'name': 'DATA_COORD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'aggregate': 'concatenate','delimiter': ',','input': '"TRCOLLECT"','length': 0,'name': 'TRCOLLECT','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'}],
            'GROUP_BY': 'GEO',
            'INPUT': outputs['RefactorFields']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Aggregate'] = processing.run('native:aggregate', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Refactor fields
        alg_params = {
            'FIELDS_MAPPING': [{'alias': None,'comment': None,'expression': '"CLASS_ID"','length': 0,'name': 'CLASS_ID','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_BDI"','length': 0,'name': 'ID_BDI','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT"','length': 0,'name': 'NR_CRT','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"DENUM"','length': 0,'name': 'DENUM','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_STP_INC"','length': 0,'name': 'ID_STP_INC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_STP_INC"','length': 0,'name': 'NR_CRT_STP_INC','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_STP_TERM"','length': 0,'name': 'ID_STP_TERM','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_STP_TERM"','length': 0,'name': 'NR_CRT_STP_TERM','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_TR_JT1"','length': 0,'name': 'ID_TR_JT1','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'array_get(string_to_array("TRCOLLECT", \',\'), 0)\r\n','length': 20,'name': 'NR_CRT_TR_JT1','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_TR_JT2"','length': 0,'name': 'ID_TR_JT2','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'array_get(string_to_array("TRCOLLECT", \',\'), 1)\r\n','length': 0,'name': 'NR_CRT_TR_JT2','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_TR_JT3"','length': 0,'name': 'ID_TR_JT3','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'array_get(string_to_array("TRCOLLECT", \',\'), 2)\r\n','length': 0,'name': 'NR_CRT_TR_JT3','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_TR_JT4"','length': 0,'name': 'ID_TR_JT4','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'array_get(string_to_array("TRCOLLECT", \',\'), 3)\r\n','length': 0,'name': 'NR_CRT_TR_JT4','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_TR_JT5"','length': 0,'name': 'ID_TR_JT5','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'array_get(string_to_array("TRCOLLECT", \',\'), 4)\r\n','length': 0,'name': 'NR_CRT_TR_JT5','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_TR_JT6"','length': 0,'name': 'ID_TR_JT6','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'array_get(string_to_array("TRCOLLECT", \',\'), 5)\r\n','length': 0,'name': 'NR_CRT_TR_JT6','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'round_wkt_coordinates($geometry)','length': 0,'name': 'GEO','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"LUNG"','length': 0,'name': 'LUNG','precision': 3,'sub_type': 0,'type': 6,'type_name': 'double precision'},{'alias': None,'comment': None,'expression': '"SURSA_COORD"','length': 0,'name': 'SURSA_COORD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DATA_COORD"','length': 0,'name': 'DATA_COORD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TRCOLLECT"','length': 0,'name': 'TRCOLLECT','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'}],
            'INPUT': outputs['Aggregate']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RefactorFields'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # STOP
        alg_params = {
            'INPUT': outputs['RefactorFields']['OUTPUT'],
            'VERTICES': '-1',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Stop'] = processing.run('native:extractspecificvertices', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # START
        alg_params = {
            'INPUT': outputs['RefactorFields']['OUTPUT'],
            'VERTICES': '0',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Start'] = processing.run('native:extractspecificvertices', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Join attributes by location STALPI CU STOP
        alg_params = {
            'DISCARD_NONMATCHING': True,
            'INPUT': outputs['Stop']['OUTPUT'],
            'JOIN': outputs['Buffer']['OUTPUT'],
            'JOIN_FIELDS': [''],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREDICATE': [0],  # intersect
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByLocationStalpiCuStop'] = processing.run('native:joinattributesbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Join attributes by location STALPI CU START
        alg_params = {
            'DISCARD_NONMATCHING': True,
            'INPUT': outputs['Start']['OUTPUT'],
            'JOIN': outputs['Buffer']['OUTPUT'],
            'JOIN_FIELDS': [''],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREDICATE': [0],  # intersect
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByLocationStalpiCuStart'] = processing.run('native:joinattributesbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Retain fields STOP JOIN
        alg_params = {
            'FIELDS': ['NR_CRT','NR_CRT_2','DENUM_2'],
            'INPUT': outputs['JoinAttributesByLocationStalpiCuStop']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RetainFieldsStopJoin'] = processing.run('native:retainfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Retain fields
        alg_params = {
            'FIELDS': ['NR_CRT','NR_CRT_2','DENUM_2'],
            'INPUT': outputs['JoinAttributesByLocationStalpiCuStart']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RetainFields'] = processing.run('native:retainfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value CU START
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'NR_CRT',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'NR_CRT',
            'INPUT': outputs['RefactorFields']['OUTPUT'],
            'INPUT_2': outputs['RetainFields']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueCuStart'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'NR_CRT',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'NR_CRT',
            'INPUT': outputs['JoinAttributesByFieldValueCuStart']['OUTPUT'],
            'INPUT_2': outputs['RetainFieldsStopJoin']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Refactor fields SEMIFINAL
        alg_params = {
            'FIELDS_MAPPING': [{'alias': None,'comment': None,'expression': '"CLASS_ID"','length': 0,'name': 'CLASS_ID','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': 'null','length': 0,'name': 'ID_BDI','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT"','length': 0,'name': 'NR_CRT','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '\'STP. \' ||  "DENUM_2" || \' - \' ||\'STP. \'  ||  "DENUM_2_2"','length': 0,'name': 'DENUM','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_STP_INC"','length': 0,'name': 'ID_STP_INC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'NR_CRT_2','length': 0,'name': 'NR_CRT_STP_INC','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_STP_TERM"','length': 0,'name': 'ID_STP_TERM','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'NR_CRT_2_2','length': 0,'name': 'NR_CRT_STP_TERM','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_TR_JT1"','length': 0,'name': 'ID_TR_JT1','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'array_get(string_to_array("TRCOLLECT", \',\'), 0)\r\n','length': 20,'name': 'NR_CRT_TR_JT1','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_TR_JT2"','length': 0,'name': 'ID_TR_JT2','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'array_get(string_to_array("TRCOLLECT", \',\'), 1)\r\n','length': 0,'name': 'NR_CRT_TR_JT2','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_TR_JT3"','length': 0,'name': 'ID_TR_JT3','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'array_get(string_to_array("TRCOLLECT", \',\'), 2)\r\n','length': 0,'name': 'NR_CRT_TR_JT3','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_TR_JT4"','length': 0,'name': 'ID_TR_JT4','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'array_get(string_to_array("TRCOLLECT", \',\'), 3)\r\n','length': 0,'name': 'NR_CRT_TR_JT4','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_TR_JT5"','length': 0,'name': 'ID_TR_JT5','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'array_get(string_to_array("TRCOLLECT", \',\'), 4)\r\n','length': 0,'name': 'NR_CRT_TR_JT5','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_TR_JT6"','length': 0,'name': 'ID_TR_JT6','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'array_get(string_to_array("TRCOLLECT", \',\'), 5)\r\n','length': 0,'name': 'NR_CRT_TR_JT6','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'round_wkt_coordinates($geometry)','length': 0,'name': 'GEO','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'to_string(format_number("LUNG", 3))','length': 0,'name': 'LUNG','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': "'Masuratori topo'",'length': 0,'name': 'SURSA_COORD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': "format_date(now(), 'dd.MM.yyyy')",'length': 0,'name': 'DATA_COORD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'}],
            'INPUT': outputs['JoinAttributesByFieldValue']['OUTPUT'],
            'OUTPUT': parameters['Deschideri_xml_']
        }
        outputs['RefactorFieldsSemifinal'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['DESCHIDERI_XML_'] = outputs['RefactorFieldsSemifinal']['OUTPUT']
        return results

    def name(self):
        return '004_DESCHIDERI_JT'

    def displayName(self):
        return '004_DESCHIDERI_JT'

    def group(self):
        return 'LEA JT'

    def groupId(self):
        return 'LEA JT'

    def createInstance(self):
        return DeschideriJTModel()
