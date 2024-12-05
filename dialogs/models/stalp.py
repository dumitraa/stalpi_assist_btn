"""
Model exported as python.
Name : 003 STALP JT generare
Group : LEA JT
With QGIS : 33802
"""

from qgis.core import QgsProcessing # type: ignore
from qgis.core import QgsProcessingAlgorithm # type: ignore
from qgis.core import QgsProcessingMultiStepFeedback # type: ignore
from qgis.core import QgsProcessingParameterVectorLayer # type: ignore
from qgis.core import QgsProcessingParameterFeatureSink # type: ignore
import processing # type: ignore


class StalpJTModel(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('poze_geotag', 'poze geotag', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('stalp_in_lucru', 'STALP in lucru', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Stalp_xml_', 'STALP_XML_', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue='TEMPORARY_OUTPUT'))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(20, model_feedback)
        results = {}
        outputs = {}

        # Delete duplicate geometries
        alg_params = {
            'INPUT': parameters['poze_geotag'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DeleteDuplicateGeometries'] = processing.run('native:deleteduplicategeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # id loc tronson
        alg_params = {
            'FIELDS_MAPPING': [{'alias': None,'comment': None,'expression': "'2018'",'length': 0,'name': 'CLASS_ID','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_BDI"','length': 0,'name': 'ID_BDI','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT"','length': 0,'name': 'NR_CRT','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': 'array_get(\r\n    array_sort(\r\n        aggregate(\r\n            layer:=\'TRONSON_XML_\',\r\n            aggregate:=\'array_agg\',\r\n            expression:="ID_LOC",\r\n            filter:=intersects($geometry, geometry(@parent))\r\n        )\r\n    ), 0\r\n)','length': 10,'name': 'ID_LINIE_JT_1','precision': 0,'sub_type': 0,'type': 4,'type_name': 'int8'},{'alias': None,'comment': None,'expression': '"NR_CRT_LINIE_JT_1"','length': 0,'name': 'NR_CRT_LINIE_JT_1','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'array_get(\r\n    array_sort(\r\n        aggregate(\r\n            layer:=\'TRONSON_XML_\',\r\n            aggregate:=\'array_agg\',\r\n            expression:="ID_LOC",\r\n            filter:=intersects($geometry, geometry(@parent))\r\n        )\r\n    ), 1\r\n)','length': 0,'name': 'ID_LINIE_JT_2','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_LINIE_JT_2"','length': 0,'name': 'NR_CRT_LINIE_JT_2','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'array_get(\r\n    array_sort(\r\n        aggregate(\r\n            layer:=\'TRONSON_XML_\',\r\n            aggregate:=\'array_agg\',\r\n            expression:="ID_LOC",\r\n            filter:=intersects($geometry, geometry(@parent))\r\n        )\r\n    ), 2\r\n)','length': 0,'name': 'ID_LINIE_JT_3','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_LINIE_JT_3"','length': 0,'name': 'NR_CRT_LINIE_JT_3','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'array_get(\r\n    array_sort(\r\n        aggregate(\r\n            layer:=\'TRONSON_XML_\',\r\n            aggregate:=\'array_agg\',\r\n            expression:="ID_LOC",\r\n            filter:=intersects($geometry, geometry(@parent))\r\n        )\r\n    ), 3\r\n)','length': 0,'name': 'ID_LINIE_JT_4','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_LINIE_JT_4"','length': 0,'name': 'NR_CRT_LINIE_JT_4','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'array_get(\r\n    array_sort(\r\n        aggregate(\r\n            layer:=\'TRONSON_XML_\',\r\n            aggregate:=\'array_agg\',\r\n            expression:="ID_LOC",\r\n            filter:=intersects($geometry, geometry(@parent))\r\n        )\r\n    ), 4\r\n)','length': 0,'name': 'ID_LINIE_JT_5','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_LINIE_JT_5"','length': 0,'name': 'NR_CRT_LINIE_JT_5','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'array_get(\r\n    array_sort(\r\n        aggregate(\r\n            layer:=\'TRONSON_XML_\',\r\n            aggregate:=\'array_agg\',\r\n            expression:="ID_LOC",\r\n            filter:=intersects($geometry, geometry(@parent))\r\n        )\r\n    ), 5\r\n)','length': 0,'name': 'ID_LINIE_JT_6','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_LINIE_JT_6"','length': 0,'name': 'NR_CRT_LINIE_JT_6','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'array_get(\r\n    array_sort(\r\n        aggregate(\r\n            layer:=\'TRONSON_XML_\',\r\n            aggregate:=\'array_agg\',\r\n            expression:="ID_LOC",\r\n            filter:=intersects($geometry, geometry(@parent))\r\n        )\r\n    ), 6\r\n)','length': 0,'name': 'ID_LINIE_JT_7','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_LINIE_JT_7"','length': 0,'name': 'NR_CRT_LINIE_JT_7','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DENUM"','length': 0,'name': 'DENUM','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'case\r\nwhen "NR_INS_STP" is NULL then \'FN\'\r\nelse "NR_INS_STP"\r\nend','length': 0,'name': 'NR_INS_STP','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'DESC_DET','length': 0,'name': 'DESC_DET','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'case \r\nwhen  "PROP" = \'ELECTRICA\' then \'DEER\'\r\nwhen  "PROP" = \'TERTI + ELECTRICA(comodat)\' then \'TERTI + DEER\'\r\nelse "PROP"\r\nend','length': 0,'name': 'PROP','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'case \r\nwhen  "PROP" = \'ELECTRICA\' then \'DEER\'\r\nwhen  "PROP" = \'TERTI + ELECTRICA(comodat)\' then \'TERTI + DEER\'\r\nelse "PROP"\r\nend','length': 0,'name': 'DET_PROP','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_ZONA_AMP"','length': 0,'name': 'TIP_ZONA_AMP','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'upper ("JUD")','length': 0,'name': 'JUD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'upper ("PRIM")','length': 0,'name': 'PRIM','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'upper ("LOC")','length': 0,'name': 'LOC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_STR"','length': 0,'name': 'TIP_STR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'upper("STR")','length': 0,'name': 'STR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_CIR"','length': 0,'name': 'TIP_CIR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'case \r\nwhen  "DESC_CTG_MT_JT" LIKE  \'%SE%\' then \'Beton\'\r\nwhen  "DESC_CTG_MT_JT" LIKE  \'%SC%\' then \'Beton\'\r\nwhen  "DESC_CTG_MT_JT" =  \'metal\' then \'Metal\'\r\nwhen  "DESC_CTG_MT_JT" =  \'Lemn\' then \'Lemn\'\r\nend','length': 0,'name': 'TIP_MAT','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DESC_CTG_MT_JT"','length': 0,'name': 'DESC_CTG_MT_JT','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CIR"','length': 0,'name': 'NR_CIR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"UZURA_STP"','length': 0,'name': 'UZURA_STP','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"TIP_FUND"','length': 0,'name': 'TIP_FUND','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"OBS_FUND"','length': 0,'name': 'OBS_FUND','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ANC"','length': 0,'name': 'ANC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"OBS_ANC"','length': 0,'name': 'OBS_ANC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ADAOS"','length': 0,'name': 'ADAOS','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"OBS_ADAOS"','length': 0,'name': 'OBS_ADAOS','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"FIB_OPT"','length': 0,'name': 'FIB_OPT','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CIR_FO"','length': 0,'name': 'NR_CIR_FO','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': 'case \r\nwhen "FIB_OPT" = \'Nu\' then 0\r\nelse "PROP_FO"\r\nend','length': 0,'name': 'PROP_FO','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"LTC"','length': 0,'name': 'LTC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CIR_LTC"','length': 0,'name': 'NR_CIR_LTC','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"PROP_LTC"','length': 0,'name': 'PROP_LTC','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"CATV"','length': 0,'name': 'CATV','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CIR_CATV"','length': 0,'name': 'NR_CIR_CATV','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"PROP_CATV"','length': 0,'name': 'PROP_CATV','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ECHIP_COM"','length': 0,'name': 'ECHIP_COM','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DISP_CUIB_PAS"','length': 0,'name': 'DISP_CUIB_PAS','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'coalesce(to_real(NULLIF(trim("NR_CONS_C2S"), \'\')), 0)\r\n\r\n\r\n','length': 0,'name': 'NR_CONS_C2S','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': 'coalesce(to_real(NULLIF(trim("NR_CONS_C4S"), \'\')), 0)\r\n\r\n\r\n','length': 0,'name': 'NR_CONS_C4S','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': 'coalesce(to_real(NULLIF(trim("NR_CONS_C2T"), \'\')), 0)\r\n\r\n\r\n','length': 0,'name': 'NR_CONS_C2T','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': 'coalesce(to_real(NULLIF(trim("NR_CONS_C4T"), \'\')), 0)\r\n\r\n\r\n','length': 0,'name': 'NR_CONS_C4T','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': 'coalesce(to_real(NULLIF(trim("NR_CONS_C2BR"), \'\')), 0)\r\n\r\n','length': 0,'name': 'NR_CONS_C2BR','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': 'coalesce(to_real(NULLIF(trim("NR_CONS_C4BR"), \'\')), 0)\r\n\r\n','length': 0,'name': 'NR_CONS_C4BR','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"TIP_LEG_JT"','length': 0,'name': 'TIP_LEG_JT','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"PRIZA_LEG_PAM"','length': 0,'name': 'PRIZA_LEG_PAM','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"CORP_IL"','length': 0,'name': 'CORP_IL','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"CUTIE_SEL"','length': 0,'name': 'CUTIE_SEL','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"GEO"','length': 0,'name': 'GEO','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': "round(y(transform($geometry, layer_property(@layer, 'crs'), 'EPSG:4326')), 8)\n",'length': 0,'name': 'LAT','precision': 8,'sub_type': 0,'type': 6,'type_name': 'double precision'},{'alias': None,'comment': None,'expression': "round(x(transform($geometry, layer_property(@layer, 'crs'), 'EPSG:4326')), 8)\n",'length': 0,'name': 'LONG','precision': 8,'sub_type': 0,'type': 6,'type_name': 'double precision'},{'alias': None,'comment': None,'expression': 'overlay_nearest(\r\n      \'poze\' ,\r\n    "altitude",    \r\n    limit := 1  \r\n)[0]  - 2.5','length': 0,'name': 'ALT','precision': 8,'sub_type': 0,'type': 6,'type_name': 'double precision'},{'alias': None,'comment': None,'expression': 'round(x($geometry), 4)','length': 0,'name': 'X_STEREO_70','precision': 4,'sub_type': 0,'type': 6,'type_name': 'double precision'},{'alias': None,'comment': None,'expression': 'round(y($geometry), 4)','length': 0,'name': 'Y_STEREO_70','precision': 4,'sub_type': 0,'type': 6,'type_name': 'double precision'},{'alias': None,'comment': None,'expression': '(overlay_nearest(\r\n      \'poze\' ,\r\n    "altitude",    \r\n    limit := 1  \r\n)[0]  - 2.5) - \r\n(overlay_nearest(\r\n      \'GRID_GEOID\' ,\r\n    "VALUE",    \r\n    limit := 1  \r\n)[0])','length': 0,'name': 'Z_STEREO_70','precision': 4,'sub_type': 0,'type': 6,'type_name': 'double precision'},{'alias': None,'comment': None,'expression': "'Masuratori topo'",'length': 0,'name': 'SURSA_COORD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': "format_date(now(), 'dd.MM.yyyy')\r",'length': 0,'name': 'DATA_COORD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"OBS"','length': 0,'name': 'OBS','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"IMG_FILE_1"','length': 0,'name': 'IMG_FILE_1','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"IMG_FILE_2"','length': 0,'name': 'IMG_FILE_2','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"IMG_FILE_3"','length': 0,'name': 'IMG_FILE_3','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"IMG_FILE_4"','length': 0,'name': 'IMG_FILE_4','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '\'STP. \' || "DENUM"  || \'_1\'','length': 0,'name': 'new_name_1','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '\'STP. \' || "DENUM"  || \'_2\'','length': 0,'name': 'new_name_2','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '\'STP. \' || "DENUM"  || \'_3\'','length': 0,'name': 'new_name_3','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '\'STP. \' || "DENUM"  || \'_4\'','length': 0,'name': 'new_name_4','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'}],
            'INPUT': parameters['stalp_in_lucru'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['IdLocTronson'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Join attributes by nearest
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELDS_TO_COPY': ['Photo'],
            'INPUT': parameters['stalp_in_lucru'],
            'INPUT_2': outputs['DeleteDuplicateGeometries']['OUTPUT'],
            'MAX_DISTANCE': 100,
            'NEIGHBORS': 4,
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByNearest'] = processing.run('native:joinbynearest', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # JT2
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'ID_LINIE_JT_2',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': 'if(\r\n    "ID_LINIE_JT_2" IN ( "ID_LINIE_JT_1"),\r\n    NULL,\r\n    "ID_LINIE_JT_2"\r\n)',
            'INPUT': outputs['IdLocTronson']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Jt2'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Aggregate
        alg_params = {
            'AGGREGATES': [{'aggregate': 'first_value','delimiter': None,'input': '"NR_CRT"','length': 0,'name': 'NR_CRT_st','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'aggregate': 'concatenate','delimiter': ',','input': '"Photo"','length': 0,'name': 'numepoze','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'}],
            'GROUP_BY': 'NR_CRT',
            'INPUT': outputs['JoinAttributesByNearest']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Aggregate'] = processing.run('native:aggregate', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # JT3
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'ID_LINIE_JT_3',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': 'if(\r\n    "ID_LINIE_JT_3" IN ( "ID_LINIE_JT_1", "ID_LINIE_JT_2"),\r\n    NULL,\r\n    "ID_LINIE_JT_3"\r\n)',
            'INPUT': outputs['Jt2']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Jt3'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # JT4
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'ID_LINIE_JT_4',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': 'if(\r\n    "ID_LINIE_JT_4" IN ( "ID_LINIE_JT_1", "ID_LINIE_JT_2", "ID_LINIE_JT_3"),\r\n    NULL,\r\n    "ID_LINIE_JT_4"\r\n)',
            'INPUT': outputs['Jt3']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Jt4'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # JT5
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'ID_LINIE_JT_5',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': 'if(\r\n    "ID_LINIE_JT_5" IN ( "ID_LINIE_JT_1", "ID_LINIE_JT_2", "ID_LINIE_JT_3", "ID_LINIE_JT_4"),\r\n    NULL,\r\n    "ID_LINIE_JT_5"\r\n)',
            'INPUT': outputs['Jt4']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Jt5'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # JT6
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'ID_LINIE_JT_6',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': 'if(\r\n    "ID_LINIE_JT_6" IN ( "ID_LINIE_JT_1", "ID_LINIE_JT_2", "ID_LINIE_JT_3", "ID_LINIE_JT_4", "ID_LINIE_JT_5"),\r\n    NULL,\r\n    "ID_LINIE_JT_6"\r\n)',
            'INPUT': outputs['Jt5']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Jt6'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # JT7
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'ID_LINIE_JT_7',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': 'if(\r\n    "ID_LINIE_JT_7" IN ( "ID_LINIE_JT_1", "ID_LINIE_JT_2", "ID_LINIE_JT_3", "ID_LINIE_JT_4", "ID_LINIE_JT_5", "ID_LINIE_JT_6"),\r\n    NULL,\r\n    "ID_LINIE_JT_7"\r\n)',
            'INPUT': outputs['Jt6']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Jt7'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'NR_CRT',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'NR_CRT_st',
            'INPUT': outputs['Jt7']['OUTPUT'],
            'INPUT_2': outputs['Aggregate']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValue'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # POZA1
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'IMG_FILE_1',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': '(array_get(string_to_array("NUMEPOZE", \',\'), 0)) ',
            'INPUT': outputs['JoinAttributesByFieldValue']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Poza1'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # POZA2
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'IMG_FILE_2',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': '(array_get(string_to_array("NUMEPOZE", \',\'), 1))',
            'INPUT': outputs['Poza1']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Poza2'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # POZA3
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'IMG_FILE_3',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': 'array_get(string_to_array("NUMEPOZE", \',\'), 2)',
            'INPUT': outputs['Poza2']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Poza3'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # POZA4
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'IMG_FILE_4',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': 'array_get(string_to_array("NUMEPOZE", \',\'), 3)',
            'INPUT': outputs['Poza3']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Poza4'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Drop field(s)
        alg_params = {
            'COLUMN': ['NR_CRT_ST','numepoze'],
            'INPUT': outputs['Poza4']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DropFields'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # GEO 4 ZECIMALE
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'GEO',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': '\'POINT (\'|| (replace(format_number("X_STEREO_70", 4), \',\', \'\')) ||\' \'|| (replace(format_number("Y_STEREO_70", 4), \',\', \'\'))||\')\'',
            'INPUT': outputs['DropFields']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Geo4Zecimale'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # LINIE STALPI BR
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'ID_LINIE_JT_1',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer (32 bit)
            'FORMULA': 'case when "ID_LINIE_JT_1" is null then \r\n (aggregate(\r\n    layer:=\'BRANSAMENT_XML_\',\r\n    aggregate:=\'array_agg\',\r\n    expression:="ID_LOC",\r\n    filter:=intersects($geometry, geometry(@parent))\r\n)[0])\r\nELSE "ID_LINIE_JT_1"\r\nEND',
            'INPUT': outputs['Geo4Zecimale']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['LinieStalpiBr'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Refactor fields COO pt XML
        alg_params = {
            'FIELDS_MAPPING': [{'alias': None,'comment': None,'expression': '"CLASS_ID"','length': 0,'name': 'CLASS_ID','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_BDI"','length': 0,'name': 'ID_BDI','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT"','length': 0,'name': 'NR_CRT','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ID_LINIE_JT_1"','length': 10,'name': 'ID_LINIE_JT_1','precision': 0,'sub_type': 0,'type': 4,'type_name': 'int8'},{'alias': None,'comment': None,'expression': '"NR_CRT_LINIE_JT_1"','length': 0,'name': 'NR_CRT_LINIE_JT_1','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_LINIE_JT_2"','length': 0,'name': 'ID_LINIE_JT_2','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_LINIE_JT_2"','length': 0,'name': 'NR_CRT_LINIE_JT_2','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_LINIE_JT_3"','length': 0,'name': 'ID_LINIE_JT_3','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_LINIE_JT_3"','length': 0,'name': 'NR_CRT_LINIE_JT_3','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_LINIE_JT_4"','length': 0,'name': 'ID_LINIE_JT_4','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_LINIE_JT_4"','length': 0,'name': 'NR_CRT_LINIE_JT_4','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_LINIE_JT_5"','length': 0,'name': 'ID_LINIE_JT_5','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_LINIE_JT_5"','length': 0,'name': 'NR_CRT_LINIE_JT_5','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_LINIE_JT_6"','length': 0,'name': 'ID_LINIE_JT_6','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_LINIE_JT_6"','length': 0,'name': 'NR_CRT_LINIE_JT_6','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ID_LINIE_JT_7"','length': 0,'name': 'ID_LINIE_JT_7','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_CRT_LINIE_JT_7"','length': 0,'name': 'NR_CRT_LINIE_JT_7','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DENUM"','length': 0,'name': 'DENUM','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"NR_INS_STP"','length': 0,'name': 'NR_INS_STP','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'CASE WHEN ( "DESC_DET" || \'-\' || ((array_to_string(\r\n    array_distinct(\r\n        aggregate(\r\n            layer:=\'TRONSON_JT\',\r\n            aggregate:=\'array_agg\',\r\n            expression:="LINIA_JT",\r\n            filter:=intersects($geometry, geometry(@parent))\r\n        )\r\n    ), \', \'\r\n))|| \' - \'  || "STR")) IS NOT NULL THEN  ( "DESC_DET" || \'-\' || ((array_to_string(\r\n    array_distinct(\r\n        aggregate(\r\n            layer:=\'TRONSON_JT\',\r\n            aggregate:=\'array_agg\',\r\n            expression:="LINIA_JT",\r\n            filter:=intersects($geometry, geometry(@parent))\r\n        )\r\n    ), \', \'\r\n))|| \' - \'  || "STR"))\r\nELSE "DESC_DET" \r\nEND','length': 0,'name': 'DESC_DET','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"PROP"','length': 0,'name': 'PROP','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DET_PROP"','length': 0,'name': 'DET_PROP','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': "'Rural'",'length': 0,'name': 'TIP_ZONA_AMP','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"JUD"','length': 0,'name': 'JUD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"PRIM"','length': 0,'name': 'PRIM','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"LOC"','length': 0,'name': 'LOC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_STR"','length': 0,'name': 'TIP_STR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"STR"','length': 0,'name': 'STR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_CIR"','length': 0,'name': 'TIP_CIR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"TIP_MAT"','length': 0,'name': 'TIP_MAT','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DESC_CTG_MT_JT"','length': 0,'name': 'DESC_CTG_MT_JT','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': ' CASE \r\n WHEN "NR_CIR" =  \'1\' THEN \'Simplu circuit\'\r\n WHEN "NR_CIR" =  \'2\' THEN \'Dublu circuit\'\r\n ELSE "NR_CIR"\r\n END','length': 0,'name': 'NR_CIR','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"UZURA_STP"','length': 0,'name': 'UZURA_STP','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"TIP_FUND"','length': 0,'name': 'TIP_FUND','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"OBS_FUND"','length': 0,'name': 'OBS_FUND','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ANC"','length': 0,'name': 'ANC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"OBS_ANC"','length': 0,'name': 'OBS_ANC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"ADAOS"','length': 0,'name': 'ADAOS','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"OBS_ADAOS"','length': 0,'name': 'OBS_ADAOS','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"FIB_OPT"','length': 0,'name': 'FIB_OPT','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'case when"NR_CIR_FO" is null then 0\r\nelse "NR_CIR_FO"\r\nend','length': 0,'name': 'NR_CIR_FO','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '\r\ncase when"FIB_OPT" = \'Nu\' then 0\r\nelse "PROP_FO"\r\nend','length': 0,'name': 'PROP_FO','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"LTC"','length': 0,'name': 'LTC','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'case when"NR_CIR_LTC" is null then 0\r\nelse "NR_CIR_LTC"\r\nend','length': 0,'name': 'NR_CIR_LTC','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '\r\ncase when"LTC" = \'Nu\'  then 0\r\nelse "PROP_LTC"\r\nend','length': 0,'name': 'PROP_LTC','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': ' "CATV"\r\n','length': 0,'name': 'CATV','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'case when"NR_CIR_CATV" is null then 0\r\nelse "NR_CIR_CATV"\r\nend','length': 0,'name': 'NR_CIR_CATV','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '\r\n\r\n\r\ncase when "CATV" = \'Nu\'  then 0\r\nelse "PROP_CATV"\r\nend','length': 0,'name': 'PROP_CATV','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"ECHIP_COM"','length': 0,'name': 'ECHIP_COM','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DISP_CUIB_PAS"','length': 0,'name': 'DISP_CUIB_PAS','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'case when "NR_CONS_C2S" is null then 0\r\nelse "NR_CONS_C2S"\r\nend','length': 0,'name': 'NR_CONS_C2S','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '\r\ncase when "NR_CONS_C4S" is null then 0\r\nelse "NR_CONS_C4S"\r\nend','length': 0,'name': 'NR_CONS_C4S','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '\r\ncase when "NR_CONS_C2T" is null then 0\r\nelse "NR_CONS_C2T"\r\nend','length': 0,'name': 'NR_CONS_C2T','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '\r\ncase when "NR_CONS_C4T" is null then 0\r\nelse "NR_CONS_C4T"\r\nend','length': 0,'name': 'NR_CONS_C4T','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '\r\ncase when "NR_CONS_C2BR" is null then 0\r\nelse "NR_CONS_C2BR"\r\nend','length': 0,'name': 'NR_CONS_C2BR','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '\r\ncase when "NR_CONS_C4BR" is null then 0\r\nelse "NR_CONS_C4BR"\r\nend','length': 0,'name': 'NR_CONS_C4BR','precision': 0,'sub_type': 0,'type': 2,'type_name': 'integer'},{'alias': None,'comment': None,'expression': '"TIP_LEG_JT"','length': 0,'name': 'TIP_LEG_JT','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"PRIZA_LEG_PAM"','length': 0,'name': 'PRIZA_LEG_PAM','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"CORP_IL"','length': 0,'name': 'CORP_IL','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"CUTIE_SEL"','length': 0,'name': 'CUTIE_SEL','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"GEO"','length': 0,'name': 'GEO','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'to_string(format_number("LAT", 8))','length': 0,'name': 'LAT','precision': 8,'sub_type': 0,'type': 6,'type_name': 'double precision'},{'alias': None,'comment': None,'expression': 'to_string(format_number("LONG", 8))','length': 0,'name': 'LONG','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'to_string(format_number("ALT", 4))','length': 0,'name': 'ALT','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': "replace(format_number($x, 4), ',', '')",'length': 0,'name': 'X_STEREO_70','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': "replace(format_number($y, 4), ',', '')",'length': 0,'name': 'Y_STEREO_70','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': 'to_string(format_number("Z_STEREO_70", 4))','length': 0,'name': 'Z_STEREO_70','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"SURSA_COORD"','length': 0,'name': 'SURSA_COORD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"DATA_COORD"','length': 0,'name': 'DATA_COORD','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"OBS"','length': 0,'name': 'OBS','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"IMG_FILE_1"','length': 0,'name': 'IMG_FILE_1','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"IMG_FILE_2"','length': 0,'name': 'IMG_FILE_2','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"IMG_FILE_3"','length': 0,'name': 'IMG_FILE_3','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"IMG_FILE_4"','length': 0,'name': 'IMG_FILE_4','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"new_name_1"','length': 0,'name': 'new_name_1','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"new_name_2"','length': 0,'name': 'new_name_2','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"new_name_3"','length': 0,'name': 'new_name_3','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': None,'comment': None,'expression': '"new_name_4"','length': 0,'name': 'new_name_4','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'}],
            'INPUT': outputs['LinieStalpiBr']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RefactorFieldsCooPtXml'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # Field calculator DESC_DET
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'DESC_DET',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': 'case when "TIP_CIR" =\'BR\' then (  "DESC_DET" || \'-\'  ||\r\n((array_to_string(\r\n    array_distinct(\r\n        aggregate(\r\n            layer:=\'BRANS_FIRI_GRPM_JT\',\r\n            aggregate:=\'array_agg\',\r\n            expression:="LINIA_JT",\r\n            filter:=intersects($geometry, geometry(@parent))\r\n        )\r\n    ), \', \'\r\n))) || \' - \'  || "STR")\r\nELSE "DESC_DET"\r\nEND',
            'INPUT': outputs['RefactorFieldsCooPtXml']['OUTPUT'],
            'OUTPUT': parameters['Stalp_xml_']
        }
        outputs['FieldCalculatorDesc_det'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Stalp_xml_'] = outputs['FieldCalculatorDesc_det']['OUTPUT']
        return results

    def name(self):
        return '003_STALP_JT'

    def displayName(self):
        return '003_STALP_JT'

    def group(self):
        return 'LEA JT'

    def groupId(self):
        return 'LEA JT'

    def createInstance(self):
        return StalpJTModel()
