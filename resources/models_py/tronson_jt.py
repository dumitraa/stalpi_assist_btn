"""
Model exported as python
Name : 001 TRONSON_JT
Group : LEA JT
With QGIS : 33802
"""

from qgis.core import QgsProcessing # type: ignore
from qgis.core import QgsProcessingAlgorithm # type: ignore
from qgis.core import QgsProcessingMultiStepFeedback # type: ignore
from qgis.core import QgsProcessingParameterVectorLayer # type: ignore
from qgis.core import QgsProcessingParameterFeatureSink # type: ignore
from qgis.core import QgsExpressionFunction, QgsExpression # type: ignore
from qgis.core import QgsGeometry, QgsWkbTypes # type: ignore
from qgis.core import QgsGeometry, QgsWkbTypes # type: ignore

import processing # type: ignore


class TronsonJTModel(QgsProcessingAlgorithm):
    def register_functions(self):
        @QgsExpressionFunction(
            "round_wkt_coordinates",  # Name in QGIS expressions
            "Custom",  # Group name
            "Rounds WKT geometry coordinates to a given precision"  # Description
        )
        def round_wkt_coordinates(values):
            def format_point(point):
                return f"{round(point.x(), 4):.4f} {round(point.y(), 4):.4f}"

            geometry = values[0]  # Get the geometry from the input
            if isinstance(geometry, QgsGeometry):
                if geometry.isMultipart():
                    if geometry.type() == QgsWkbTypes.LineGeometry:
                        parts = [
                            "(" + ", ".join(format_point(point) for point in line) + ")"
                            for line in geometry.asMultiPolyline()
                        ]
                        wkt = f"MULTILINESTRING ({', '.join(parts)})"
                    else:
                        wkt = geometry.asWkt()  # For other geometry types
                else:
                    if geometry.type() == QgsWkbTypes.LineGeometry:
                        points = ", ".join(format_point(point) for point in geometry.asPolyline())
                        wkt = f"LINESTRING ({points})"
                    else:
                        wkt = geometry.asWkt()  # For other geometry types
                return wkt
            return None  # Return None if input is invalid

        QgsExpression.registerFunction(round_wkt_coordinates)

    def initAlgorithm(self, config=None):
        self.register_functions()
        self.addParameter(QgsProcessingParameterVectorLayer('linie_jt_introduse', 'LINIE_JT introduse', types=[QgsProcessing.TypeVector], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('stalpi_desenati', 'STALPI DESENATI', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('tronson_desenat', 'TRONSON DESENAT', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('TRONSON_XML_', 'TRONSON_XML_', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(22, model_feedback)
        results = {}
        outputs = {}

        # Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'LINIA_JT',
            'FIELDS_TO_COPY': ['ID_BDI'],
            'FIELD_2': 'DENUM',
            'INPUT': parameters['tronson_desenat'],
            'INPUT_2': parameters['linie_jt_introduse'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
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

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Field calculator
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'ID_LOC',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': '"ID_BDI_2"',
            'INPUT': outputs['JoinAttributesByFieldValue']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Refactor fields generaL
        alg_params = {
            'FIELDS_MAPPING': [{'alias': None,'comment': None,'expression': "'2001'",'length': 0,'name': 'CLASS_ID','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_BDI"','length': 0,'name': 'ID_BDI','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT"','length': 0,'name': 'NR_CRT','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': None,'length': 0,'name': 'DENUM','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': "'DEER'",'length': 0,'name': 'PROP','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': "'2000'",'length': 0,'name': 'CLASS_ID_LOC','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_LOC"','length': 0,'name': 'ID_LOC','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"NR_CRT_LOC"','length': 0,'name': 'NR_CRT_LOC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': "'2018'",'length': 0,'name': 'CLASS_ID_INC_TR','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_INC_TR"','length': 0,'name': 'ID_INC_TR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': None,'length': 0,'name': 'NR_CRT_INC_TR','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': "'2018'",'length': 0,'name': 'CLASS_ID_FIN_TR','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_FIN_TR"','length': 0,'name': 'ID_FIN_TR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': None,'length': 0,'name': 'NR_CRT_FIN_TR','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"TIP_TR"','length': 0,'name': 'TIP_TR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_COND"','length': 0,'name': 'TIP_COND','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'round(length($geometry) / 1000, 3)','length': 0,'name': 'LUNG_TR','precision': 3,'sub_type': 0,'type': 6,'type_name': 'double precision'},{'alias': None,'comment': None,'expression': None,'length': 0,'name': 'GEO','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': "'Masuratori topo'",'length': 0,'name': 'SURSA_COORD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': "format_date(now(), 'dd.MM.yyyy')\r\n",'length': 0,'name': 'DATA_COORD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"UNIT_LOG_INT"','length': 0,'name': 'UNIT_LOG_INT','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"S_UNIT_LOG"','length': 0,'name': 'S_UNIT_LOG','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"POST_LUC"','length': 0,'name': 'POST_LUC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'}],
            'INPUT': outputs['FieldCalculator']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RefactorFieldsGeneral'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # STOP
        alg_params = {
            'INPUT': outputs['RefactorFieldsGeneral']['OUTPUT'],
            'VERTICES': '-1',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Stop'] = processing.run('native:extractspecificvertices', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # START
        alg_params = {
            'INPUT': outputs['RefactorFieldsGeneral']['OUTPUT'],
            'VERTICES': '0',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Start'] = processing.run('native:extractspecificvertices', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
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

        feedback.setCurrentStep(7)
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

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Retain fields STOP JOIN
        alg_params = {
            'FIELDS': ['NR_CRT','NR_CRT_2','DENUM_2'],
            'INPUT': outputs['JoinAttributesByLocationStalpiCuStop']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RetainFieldsStopJoin'] = processing.run('native:retainfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Retain fields
        alg_params = {
            'FIELDS': ['NR_CRT','NR_CRT_2','DENUM_2'],
            'INPUT': outputs['JoinAttributesByLocationStalpiCuStart']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RetainFields'] = processing.run('native:retainfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value CU START
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'NR_CRT',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'NR_CRT',
            'INPUT': outputs['RefactorFieldsGeneral']['OUTPUT'],
            'INPUT_2': outputs['RetainFields']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueCuStart'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
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

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Refactor fields
        alg_params = {
            'FIELDS_MAPPING': [{'alias': None,'comment': None,'expression': '"fid"','length': 0,'name': 'fid','precision': 0,'sub_type': 0,'type': 4,'type_name': 'int8'},{'alias': None,'comment': None,'expression': '"CLASS_ID"','length': 0,'name': 'CLASS_ID','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': 'NULL','length': 0,'name': 'ID_BDI','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT"','length': 0,'name': 'NR_CRT','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '\'STP. \' ||  "DENUM_2" || \' - \' ||\'STP. \'  ||  "DENUM_2_2"','length': 0,'name': 'DENUM','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"PROP"','length': 0,'name': 'PROP','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"CLASS_ID_LOC"','length': 0,'name': 'CLASS_ID_LOC','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_LOC"','length': 0,'name': 'ID_LOC','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"NR_CRT_LOC"','length': 0,'name': 'NR_CRT_LOC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"CLASS_ID_INC_TR"','length': 0,'name': 'CLASS_ID_INC_TR','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_INC_TR"','length': 0,'name': 'ID_INC_TR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'NR_CRT_2','length': 0,'name': 'NR_CRT_INC_TR','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"CLASS_ID_FIN_TR"','length': 0,'name': 'CLASS_ID_FIN_TR','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_FIN_TR"','length': 0,'name': 'ID_FIN_TR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'NR_CRT_2_2','length': 0,'name': 'NR_CRT_FIN_TR','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"TIP_TR"','length': 0,'name': 'TIP_TR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_COND"','length': 0,'name': 'TIP_COND','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'to_string(format_number((length($geometry)/1000), 3))','length': 0,'name': 'LUNG_TR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'round_wkt_coordinates($geometry)','length': 0,'name': 'GEO','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"SURSA_COORD"','length': 0,'name': 'SURSA_COORD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DATA_COORD"','length': 0,'name': 'DATA_COORD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"UNIT_LOG_INT"','length': 0,'name': 'UNIT_LOG_INT','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"S_UNIT_LOG"','length': 0,'name': 'S_UNIT_LOG','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"POST_LUC"','length': 0,'name': 'POST_LUC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"OBS"','length': 0,'name': 'OBS','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'}],
            'INPUT': outputs['JoinAttributesByFieldValue']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RefactorFields'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Field calculator DENUM FB
        alg_params = {
            'FIELD_LENGTH': 100,
            'FIELD_NAME': 'DENUM',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': '\r\ncase when "NR_CRT_FIN_TR" is null then \r\n\'STP. 0\' || \' - \' ||\r\n (aggregate(\r\n    layer:=\'FB pe C LES\',\r\n    aggregate:=\'array_agg\',\r\n    expression:="DENUM",\r\n    filter:=intersects($geometry, geometry(@parent))\r\n)[0])\r\nELSE "DENUM"\r\nEND',
            'INPUT': outputs['RefactorFields']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorDenumFb'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Field calculator CLASS id FB
        alg_params = {
            'FIELD_LENGTH': 100,
            'FIELD_NAME': 'CLASS_ID_FIN_TR',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': '\r\n(case when "NR_CRT_FIN_TR" is null then \r\n (aggregate(\r\n    layer:=\'FB pe C LES\',\r\n    aggregate:=\'array_agg\',\r\n    expression:="CLASS_ID",\r\n    filter:=intersects($geometry, geometry(@parent))\r\n)[0])\r\nELSE "CLASS_ID_FIN_TR"\r\nEND)',
            'INPUT': outputs['FieldCalculatorDenumFb']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorClassIdFb'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Field calculator NR CRT FB
        alg_params = {
            'FIELD_LENGTH': 50,
            'FIELD_NAME': 'NR_CRT_FIN_TR',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer (32 bit)
            'FORMULA': 'case when "NR_CRT_FIN_TR" is null then \r\n (aggregate(\r\n    layer:=\'FB pe C LES\',\r\n    aggregate:=\'array_agg\',\r\n    expression:="NR_CRT",\r\n    filter:=intersects($geometry, geometry(@parent))\r\n)[0])\r\nELSE "NR_CRT_FIN_TR"\r\nEND',
            'INPUT': outputs['FieldCalculatorClassIdFb']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorNrCrtFb'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Field calculator DENUM FR
        alg_params = {
            'FIELD_LENGTH': 100,
            'FIELD_NAME': 'DENUM',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': '\r\ncase when "NR_CRT_FIN_TR" is null then \r\n\'STP. 0\' || \' - FR \' || \r\n (aggregate(\r\n    layer:=\'FIRIDA RETEA\',\r\n    aggregate:=\'array_agg\',\r\n    expression:="IDEN",\r\n    filter:=intersects($geometry, geometry(@parent))\r\n)[0])\r\nELSE "DENUM"\r\nEND',
            'INPUT': outputs['FieldCalculatorNrCrtFb']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorDenumFr'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # Field calculator CLASS id FR
        alg_params = {
            'FIELD_LENGTH': 100,
            'FIELD_NAME': 'CLASS_ID_FIN_TR',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': '\r\n(case when "NR_CRT_FIN_TR" is null then \r\n (aggregate(\r\n    layer:=\'FIRIDA RETEA\',\r\n    aggregate:=\'array_agg\',\r\n    expression:="CLASS_ID",\r\n    filter:=intersects($geometry, geometry(@parent))\r\n)[0])\r\nELSE "CLASS_ID_FIN_TR"\r\nEND)',
            'INPUT': outputs['FieldCalculatorDenumFr']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorClassIdFr'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Field calculator NR CRT FR
        alg_params = {
            'FIELD_LENGTH': 50,
            'FIELD_NAME': 'NR_CRT_FIN_TR',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer (32 bit)
            'FORMULA': 'case when "NR_CRT_FIN_TR" is null then \r\n (aggregate(\r\n    layer:=\'FIRIDA RETEA\',\r\n    aggregate:=\'array_agg\',\r\n    expression:="NR_CRT",\r\n    filter:=intersects($geometry, geometry(@parent))\r\n)[0])\r\nELSE "NR_CRT_FIN_TR"\r\nEND',
            'INPUT': outputs['FieldCalculatorClassIdFr']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorNrCrtFr'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # CLASS_ID_INC_TR
        alg_params = {
            'FIELD_LENGTH': 100,
            'FIELD_NAME': 'CLASS_ID_INC_TR',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': 'case when  "NR_CRT_INC_TR" is null then 1004\r\nelse  "CLASS_ID_INC_TR" \r\nend',
            'INPUT': outputs['FieldCalculatorNrCrtFr']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Class_id_inc_tr'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # ID_INC_TR
        alg_params = {
            'FIELD_LENGTH': 100,
            'FIELD_NAME': 'ID_INC_TR',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': 'case when  "NR_CRT_INC_TR" is null then\r\n(\r\naggregate(\r\n    layer:=\'PTCZ_PTAB\',\r\n    aggregate:=\'array_agg\',\r\n    expression:="ID_BDI",\r\n    filter:=intersects($geometry, buffer(geometry(@parent), 0.5))\r\n)[0])\r\nelse  "ID_INC_TR" \r\nend',
            'INPUT': outputs['Class_id_inc_tr']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Id_inc_tr'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}

        # DENUM
        alg_params = {
            'FIELD_LENGTH': 300,
            'FIELD_NAME': 'DENUM',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': 'case when  "NR_CRT_INC_TR" is null then\r\n((\r\naggregate(\r\n    layer:=\'PTCZ_PTAB\',\r\n    aggregate:=\'array_agg\',\r\n    expression:="DENUM",\r\n    filter:=intersects($geometry, buffer(geometry(@parent), 0.5))\r\n)[0])  || \' - STP. \'  || \r\n(aggregate(\r\n    layer:=\'STALP_JT\',\r\n    aggregate:=\'array_agg\',\r\n    expression:="DENUM",\r\n    filter:=intersects($geometry, buffer(geometry(@parent), 0.3))\r\n)[-1]))\r\nelse  "DENUM" \r\nend',
            'INPUT': outputs['Id_inc_tr']['OUTPUT'],
            'OUTPUT': parameters['TRONSON_XML_']
        }
        outputs['Denum'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['TRONSON_XML_'] = outputs['Denum']['OUTPUT']
        return results

    def name(self):
        return '001_TRONSON_JT'

    def displayName(self):
        return '001_TRONSON_JT'

    def group(self):
        return 'LEA JT'

    def groupId(self):
        return 'LEA JT'

    def createInstance(self):
        return TronsonJTModel()
