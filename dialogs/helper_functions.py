'''
#TODO

OVERALL:
- Buffer
- Field Calculator
- Refactor Fields
- Extract Specific Vertices
- Join Attributes by Location
- Retain Fields
- Join Attributes Table
- Extract By Attribute
- Merge Vector Layers
- Delete Column
- Join by Nearest
- Aggregate
- Export Add Geometry Columns
- Explode Lines

---

TRONSON:
- Join Attributes Table
- Buffer
- Field Calculator
- Refactor Fields
- Extract Specific Vertices
- Join Attributes by Location
- Retain Fields
- Join Attributes Table

--

BRANSAMENT:
- Refactor Fields
- Join Attributes Table
- Field Calculator
- Extract Specific Vertices
- Extract By Attribute
- Merge Vector Layers
- Delete Column

--

STALP:
- Refactor Fields
- Join by Nearest
- Field Calculator
- Aggregate
- Join Attributes Table
- Delete Column

--

TRONSON_2:
- Refactor Fields

--

DESCHIDERI:
- Export Add Geometry Columns
- Retain Fields
- Refactor Fields
- Buffer
- Extract By Attribute
- Explode Lines
- Aggregate
- Extract Specific Vertices
- Join Attributes by Location
- Join Attributes Table

--

XLS_1:
- Refactor Fields
- Join Attributes Table
- Explode Lines

--

XLS_2:
- Refactor Fields
- Retain Fields
- Join Attributes Table
- Field Calculator
- Delete Column

'''

from qgis.core import QgsProcessing, QgsProject, QgsVectorLayer, QgsMessageLog, Qgis, QgsWkbTypes, QgsField # type: ignore
import processing # type: ignore
import os
from PyQt5.QtWidgets import QFileDialog
import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QInputDialog
import xml.etree.ElementTree as ET
# import xlsxwriter
import csv
from qgis.PyQt.QtCore import QVariant # type: ignore


class HelperBase:
    def __init__(self):
        super().__init__()
        
    # MARK: MODELS
    # Join Attributes Table
    def join_attr_table(self, field, fields_to_copy, field_2, input, input_2, base_dir, output, layers):
        if not input or not input_2:
            QgsMessageLog.logMessage(f"No valid layers found for joining", "StalpiAssist", level=Qgis.Warning)
            return False
        
        # QgsMessageLog.logMessage(f"Entered merge_layers with layer_list: {layer_list} and folder: {folder}", "StalpiAssist", level=Qgis.Info)
        try:
            output = os.path.join(base_dir, f"{output}.shp") if output else QgsProcessing.TEMPORARY_OUTPUT
            if output and not QgsVectorLayer(output, '', 'ogr').isValid():
                processing.run("native:joinattributestable", {
                    'DISCARD_NONMATCHING': False,
                    'FIELD': field,
                    'FIELDS_TO_COPY': fields_to_copy,
                    'FIELD_2': field_2,
                    'INPUT': input,
                    'INPUT_2': input_2,
                    'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
                    'PREFIX': None,
                    'OUTPUT': output
                })
                self.add_layer_to_project(output)
                layers.update(self.get_layers())
            else:
                QgsMessageLog.logMessage(f"Merge output already exists and is valid: {output}", "StalpiAssist", level=Qgis.Info)
                
            return True
        except Exception as e:
            QgsMessageLog.logMessage(f"Error in join_attr_table: {e}", "StalpiAssist", level=Qgis.Critical)
            return False
        
    
    # Buffer
    def buffer(self, input, output, base_dir, layers):
        if not input:
            QgsMessageLog.logMessage(f"No valid layers found for buffering", "StalpiAssist", level=Qgis.Warning)
            return False
        
        try:
            # Check if the layer already exists
            existing_layer = QgsProject.instance().mapLayersByName(output)
            if existing_layer:
                QgsMessageLog.logMessage(f"Layer '{output}' already exists. Skipping buffer.", "StalpiAssist", level=Qgis.Info)
                return True

            # QgsMessageLog.logMessage(f"Buffering: {input} with {output}", "StalpiAssist", level=Qgis.Info)
            output = os.path.join(base_dir, f"{output}.shp") if output else QgsProcessing.TEMPORARY_OUTPUT
            if output:
                processing.run("native:buffer", {
                    'DISSOLVE': False,
                    'DISTANCE': 0.1,
                    'END_CAP_STYLE': 0,  # Round
                    'INPUT': input,
                    'JOIN_STYLE': 0,  # Round
                    'MITER_LIMIT': 2,
                    'SEGMENTS': 5,
                    'SEPARATE_DISJOINT': False,
                    'OUTPUT': output
                })
                self.add_layer_to_project(output)
                layers.update(self.get_layers())
                
            return True
        except Exception as e:
            QgsMessageLog.logMessage(f"Error in buffer: {e}", "StalpiAssist", level=Qgis.Critical)
            return False
        
    # Field Calculator
    def calc_field(self, input, field_length, field_name, field_precision, field_type, formula, output, base_dir, layers):
        if not input:
            QgsMessageLog.logMessage(f"No valid layers found for field calculation", "StalpiAssist", level=Qgis.Warning)
            return False
        
        try:
            # Check if the layer already exists
            existing_layer = QgsProject.instance().mapLayersByName(output)
            if existing_layer:
                QgsMessageLog.logMessage(f"Layer '{output}' already exists. Skipping field calculation.", "StalpiAssist", level=Qgis.Info)
                return True

            # QgsMessageLog.logMessage(f"Calculating field: {field} in {input} with {output}", "StalpiAssist", level=Qgis.Info)
            output = os.path.join(base_dir, f"{output}.shp") if output else QgsProcessing.TEMPORARY_OUTPUT
            if output:
                processing.run("native:fieldcalculator", {
                    'FIELD_LENGTH': field_length,
                    'FIELD_NAME': field_name,
                    'FIELD_PRECISION': field_precision,
                    'FIELD_TYPE': field_type,
                    'FORMULA': formula,
                    'INPUT': input,
                    'OUTPUT': output
                })
                self.add_layer_to_project(output)
                layers.update(self.get_layers())
                
            return True
        except Exception as e:
            QgsMessageLog.logMessage(f"Error in calc_field: {e}", "StalpiAssist", level=Qgis.Critical)
            return False
        
        
    # Refactor Fields
    def refactor_field(self, input, fields_mapping, output, base_dir, layers):
        if not input:
            QgsMessageLog.logMessage(f"No valid layers found for field refactoring", "StalpiAssist", level=Qgis.Warning)
            return False
        
        try:
            # Check if the layer already exists
            existing_layer = QgsProject.instance().mapLayersByName(output)
            if existing_layer:
                QgsMessageLog.logMessage(f"Layer '{output}' already exists. Skipping field refactoring.", "StalpiAssist", level=Qgis.Info)
                return True

            # QgsMessageLog.logMessage(f"Refactoring fields: {fields_mapping} in {input} with {output}", "StalpiAssist", level=Qgis.Info)
            output = os.path.join(base_dir, f"{output}.shp") if output else QgsProcessing.TEMPORARY_OUTPUT
            if output:
                processing.run("native:refactorfields", {
                    'FIELDS_MAPPING': fields_mapping,
                    'INPUT': input,
                    'OUTPUT': output
                })
                self.add_layer_to_project(output)
                layers.update(self.get_layers())
                
            return True
        except Exception as e:
            QgsMessageLog.logMessage(f"Error in refactor_field: {e}", "StalpiAssist", level=Qgis.Critical)
            return False
        
    # Extract Specific Vertices
    def extract_specific_vertices(self, input, vertices, output, base_dir, layers):
        if not input:
            QgsMessageLog.logMessage(f"No valid layers found for extracting vertices", "StalpiAssist", level=Qgis.Warning)
            return False
        
        try:
            # Check if the layer already exists
            existing_layer = QgsProject.instance().mapLayersByName(output)
            if existing_layer:
                QgsMessageLog.logMessage(f"Layer '{output}' already exists. Skipping vertex extraction.", "StalpiAssist", level=Qgis.Info)
                return True

            # QgsMessageLog.logMessage(f"Extracting vertices: {vertices} in {input} with {output}", "StalpiAssist", level=Qgis.Info)
            output = os.path.join(base_dir, f"{output}.shp") if output else QgsProcessing.TEMPORARY_OUTPUT
            if output:
                processing.run("native:extractspecificvertices", {
                    'INPUT': input,
                    'VERTICES': vertices,
                    'OUTPUT': output
                })
                self.add_layer_to_project(output)
                layers.update(self.get_layers())
                
            return True
        except Exception as e:
            QgsMessageLog.logMessage(f"Error in extract_specific_vertices: {e}", "StalpiAssist", level=Qgis.Critical)
            return False
        
    # Retain Fields
    def retain_fields(self, input, fields, output, base_dir, layers):
        if not input:
            QgsMessageLog.logMessage(f"No valid layers found for retaining fields", "StalpiAssist", level=Qgis.Warning)
            return False
        
        try:
            # Check if the layer already exists
            existing_layer = QgsProject.instance().mapLayersByName(output)
            if existing_layer:
                QgsMessageLog.logMessage(f"Layer '{output}' already exists. Skipping field retention.", "StalpiAssist", level=Qgis.Info)
                return True

            # QgsMessageLog.logMessage(f"Retaining fields: {fields} in {input} with {output}", "StalpiAssist", level=Qgis.Info)
            output = os.path.join(base_dir, f"{output}.shp") if output else QgsProcessing.TEMPORARY_OUTPUT
            if output:
                processing.run("native:retainfields", {
                    'FIELDS': fields,
                    'INPUT': input,
                    'OUTPUT': output
                })
                self.add_layer_to_project(output)
                layers.update(self.get_layers())
                
            return True
        except Exception as e:
            QgsMessageLog.logMessage(f"Error in retain_fields: {e}", "StalpiAssist", level=Qgis.Critical)
            return False
        
    # Extract By Attribute
    def extract_by_attr(self, input, field, operator, value, output, base_dir, layers):
        if not input:
            QgsMessageLog.logMessage(f"No valid layers found for extracting by attribute", "StalpiAssist", level=Qgis.Warning)
            return False
        
        try:
            # Check if the layer already exists
            existing_layer = QgsProject.instance().mapLayersByName(output)
            if existing_layer:
                QgsMessageLog.logMessage(f"Layer '{output}' already exists. Skipping attribute extraction.", "StalpiAssist", level=Qgis.Info)
                return True

            # QgsMessageLog.logMessage(f"Extracting by attribute: {field} in {input} with {output}", "StalpiAssist", level=Qgis.Info)
            output = os.path.join(base_dir, f"{output}.shp") if output else QgsProcessing.TEMPORARY_OUTPUT
            if output:
                processing.run("native:extractbyattribute", {
                    'FIELD': field,
                    'INPUT': input,
                    'OPERATOR': operator,
                    'VALUE': value,
                    'OUTPUT': output
                })
                self.add_layer_to_project(output)
                layers.update(self.get_layers())
                
            return True
        except Exception as e:
            QgsMessageLog.logMessage(f"Error in extract_by_attr: {e}", "StalpiAssist", level=Qgis.Critical)
            return False
        
    # Delete Column
    def delete_column(self, input, column, output, base_dir, layers):
        if not input:
            QgsMessageLog.logMessage(f"No valid layers found for deleting column", "StalpiAssist", level=Qgis.Warning)
            return False
        
        try:
            # Check if the layer already exists
            existing_layer = QgsProject.instance().mapLayersByName(output)
            if existing_layer:
                QgsMessageLog.logMessage(f"Layer '{output}' already exists. Skipping column deletion.", "StalpiAssist", level=Qgis.Info)
                return True

            # QgsMessageLog.logMessage(f"Deleting column: {column} in {input} with {output}", "StalpiAssist", level=Qgis.Info)
            output = os.path.join(base_dir, f"{output}.shp") if output else QgsProcessing.TEMPORARY_OUTPUT
            if output:
                processing.run("native:deletecolumn", {
                    'COLUMN': column,
                    'INPUT': input,
                    'OUTPUT': output
                })
                self.add_layer_to_project(output)
                layers.update(self.get_layers())
                
            return True
        except Exception as e:
            QgsMessageLog.logMessage(f"Error in delete_column: {e}", "StalpiAssist", level=Qgis.Critical)
            return False
    
    # Join by Nearest
    
    
    # Aggregate
    def aggregate(self, input, group_by, aggregates, output, base_dir, layers):
        if not input:
            QgsMessageLog.logMessage(f"No valid layers found for aggregating", "StalpiAssist", level=Qgis.Warning)
            return False
        
        try:
            # Check if the layer already exists
            existing_layer = QgsProject.instance().mapLayersByName(output)
            if existing_layer:
                QgsMessageLog.logMessage(f"Layer '{output}' already exists. Skipping aggregation.", "StalpiAssist", level=Qgis.Info)
                return True

            # QgsMessageLog.logMessage(f"Aggregating: {input} with {output}", "StalpiAssist", level=Qgis.Info)
            output = os.path.join(base_dir, f"{output}.shp") if output else QgsProcessing.TEMPORARY_OUTPUT
            if output:
                processing.run("native:aggregate", {
                    'AGGREGATES': aggregates,
                    'GROUP_BY': group_by,
                    'INPUT': input,
                    'OUTPUT': output
                })
                self.add_layer_to_project(output)
                layers.update(self.get_layers())
                
            return True
        except Exception as e:
            QgsMessageLog.logMessage(f"Error in aggregate: {e}", "StalpiAssist", level=Qgis.Critical)
            return False
    
    # Export Add Geometry Columns
    def export_add_geometry_columns(self, input, output, base_dir, layers):
        if not input:
            QgsMessageLog.logMessage(f"No valid layers found for adding geometry columns", "StalpiAssist", level=Qgis.Warning)
            return False
        
        try:
            # Check if the layer already exists
            existing_layer = QgsProject.instance().mapLayersByName(output)
            if existing_layer:
                QgsMessageLog.logMessage(f"Layer '{output}' already exists. Skipping geometry column addition.", "StalpiAssist", level=Qgis.Info)
                return True

            # QgsMessageLog.logMessage(f"Adding geometry columns: {input} with {output}", "StalpiAssist", level=Qgis.Info)
            output = os.path.join(base_dir, f"{output}.shp") if output else QgsProcessing.TEMPORARY_OUTPUT
            if output:
                processing.run("native:exportaddgeometrycolumns", {
                    'INPUT': input,
                    'OUTPUT': output
                })
                self.add_layer_to_project(output)
                layers.update(self.get_layers())
                
            return True
        except Exception as e:
            QgsMessageLog.logMessage(f"Error in export_add_geometry_columns: {e}", "StalpiAssist", level=Qgis.Critical)
            return False
    
    
    # Explode Lines
    def explode_lines(self, input, output, base_dir, layers):
        if not input:
            QgsMessageLog.logMessage(f"No valid layers found for exploding lines", "StalpiAssist", level=Qgis.Warning)
            return False
        
        try:
            # Check if the layer already exists
            existing_layer = QgsProject.instance().mapLayersByName(output)
            if existing_layer:
                QgsMessageLog.logMessage(f"Layer '{output}' already exists. Skipping line explosion.", "StalpiAssist", level=Qgis.Info)
                return True

            # QgsMessageLog.logMessage(f"Exploding lines: {input} with {output}", "StalpiAssist", level=Qgis.Info)
            output = os.path.join(base_dir, f"{output}.shp") if output else QgsProcessing.TEMPORARY_OUTPUT
            if output:
                processing.run("native:explodelines", {
                    'INPUT': input,
                    'OUTPUT': output
                })
                self.add_layer_to_project(output)
                layers.update(self.get_layers())
                
            return True
        except Exception as e:
            QgsMessageLog.logMessage(f"Error in explode_lines: {e}", "StalpiAssist", level=Qgis.Critical)
            return False
        
        
        # Merge Vector Layers
    def merge_layers(self, layer_list, output, base_dir, layers):
        QgsMessageLog.logMessage(f"Entered merge_layers with layer_list: {layer_list} and folder: {folder}", "StalpiAssist", level=Qgis.Info)
        if not layer_list:
            QgsMessageLog.logMessage(f"No valid layers found for merging in layer_list: {layer_list}", "StalpiAssist", level=Qgis.Warning)
            return False
        
        # QgsMessageLog.logMessage(f"Entered merge_layers with layer_list: {layer_list} and folder: {folder}", "StalpiAssist", level=Qgis.Info)
        try:
            valid_layers = [layer for layer in layer_list if layer is not None]
            output = os.path.join(base_dir, f"{output}.shp") if output else QgsProcessing.TEMPORARY_OUTPUT
            if output and not QgsVectorLayer(output, '', 'ogr').isValid():
                processing.run("qgis:mergevectorlayers", {
                    'LAYERS': valid_layers, 
                    'CRS': 'EPSG:3844', 
                    'OUTPUT': output
                })
                self.add_layer_to_project(output)
                layers.update(self.get_layers())
            else:
                QgsMessageLog.logMessage(f"Merge output already exists and is valid: {output}", "StalpiAssist", level=Qgis.Info)
                
            return True
        except Exception as e:
            QgsMessageLog.logMessage(f"Error in merge_layers: {e}", "StalpiAssist", level=Qgis.Critical)
            return False


    # Join Attributes by Location
    def join_attributes_by_location(self, input_file, join_file, output, method, base_dir, layers):
        if not input_file or not join_file:
            QgsMessageLog.logMessage(f"No valid layers found for joining in input_file: {input_file} and join_file: {join_file} for the layers - {layers}", "StalpiAssist", level=Qgis.Warning)
            return False
        
        QgsMessageLog.logMessage(f"Entered join_attributes_by_location with input_file: {input_file}, join_file: {join_file}, output_name: {output}, method: {method}", "StalpiAssist", level=Qgis.Info)
        try:
            # Check if the layer already exists
            existing_layer = QgsProject.instance().mapLayersByName(output)
            if existing_layer:
                QgsMessageLog.logMessage(f"Layer '{output}' already exists. Skipping join.", "StalpiAssist", level=Qgis.Info)
                return True

            # QgsMessageLog.logMessage(f"Joining attributes by location: {input_file} with {join_file}", "StalpiAssist", level=Qgis.Info)
            output = os.path.join(base_dir, f"{output}.shp") if output else QgsProcessing.TEMPORARY_OUTPUT
            if output:
                processing.run("qgis:joinattributesbylocation", {
                    'INPUT': input_file,
                    'JOIN': join_file,
                    'PREDICATE': [0],  # intersects
                    'JOIN_FIELDS': [''],
                    'METHOD': 0 if method == 'One-to-Many' else 1,  # One-to-Many or One-to-One
                    'DISCARD_NONMATCHING': False,
                    'OUTPUT': output
                })
                self.add_layer_to_project(output)
                layers.update(self.get_layers())
                
            return True
        except Exception as e:
            QgsMessageLog.logMessage(f"Error in join_attributes_by_location: {e}", "StalpiAssist", level=Qgis.Critical)
            return False
    
    # MARK: OTHER STEPS
    # Complete field based on mapping
    def complete_fields_based_on_mapping(self, params):
        """
        Completes multiple fields in a QGIS layer based on a mapping derived from a CSV file.

        :param params: Dictionary with the following keys:
            - layer: QgsVectorLayer object to update.
            - csv_file: Path to the CSV file used for mapping.
            - search_value: The specific value to search for in the CSV.
            - csv_key_column: Column name in the CSV to match the search value.
            - csv_value_column: List of column names in the CSV whose values will be written to corresponding QGIS fields.
            - field_to_complete: List of QGIS field names to write the mapped values into.
        """
        # Validate inputs
        if not isinstance(params['csv_value_column'], list) or not isinstance(params['field_to_complete'], list):
            raise ValueError("Both 'csv_value_column' and 'field_to_complete' must be lists.")

        # Load the mapping from the CSV file
        mapping = {}
        with open(params['csv_file'], mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                key = row[params['csv_key_column']]
                if key == params['search_value']:  # Only add matching key-value pairs
                    mapping[key] = {column: row[column] for column in params['csv_value_column']}

        if not mapping:
            try:
                raise ValueError(f"The search value '{params['search_value']}' was not found in the CSV.")
            except ValueError as e:
                return False
        

        # Start editing the layer
        layer = params['layer']
        if not layer.isEditable():
            layer.startEditing()

        # Iterate through the layer features and update the fields
        for feature in layer.getFeatures():
            if params['search_value'] in mapping:  # Check if the key exists in the mapping
                if len(params['field_to_complete']) == 1:
                    # Concatenate multiple CSV values for a single field
                    concatenated_values = "-".join([mapping[params['search_value']][column] for column in params['csv_value_column']])
                    feature[params['field_to_complete'][0]] = concatenated_values
                else:
                    # Map CSV values to corresponding fields
                    for csv_column, field in zip(params['csv_value_column'], params['field_to_complete']):
                        feature[field] = mapping[params['search_value']][csv_column]

                layer.updateFeature(feature)

        # Save changes
        return layer.commitChanges()


    # Add "Nr.crt" column and populate with @row_number + X
    def add_and_populate_nr_crt_column(self, layer, offset=0):
        """
        Adds a 'Nr.crt' column to the given layer and populates it with @row_number + offset.
        
        :param layer: QgsVectorLayer object to modify.
        :param offset: Integer to start numbering from. Defaults to 0.
        """
        # Ensure the layer is editable
        if not layer.isEditable():
            layer.startEditing()
        
        # Add the 'Nr.crt' column if it doesn't already exist
        if not layer.fields().indexFromName('Nr.crt') >= 0:
            layer.dataProvider().addAttributes([QgsField("Nr.crt", QVariant.Int)])
            layer.updateFields()
        else:
            return True

        # Populate the 'Nr.crt' column with sequential numbers
        row_number = offset
        for feature in layer.getFeatures():
            feature['Nr.crt'] = row_number
            row_number += 1
            layer.updateFeature(feature)

        return layer.commitChanges()
        
    # Calculate geometry with four decimal points for linestring #NOTE: have the script 
    def round_wkt_coordinates(self, geometry):
        QgsMessageLog.logMessage(f"Entered round_wkt_coordinates with geometry: {geometry}", "StalpiAssist", level=Qgis.Info)
        def format_point(point):
            return f"{round(point.x(), 4):.4f} {round(point.y(), 4):.4f}"
        try: 
            if geometry.isMultipart():
                if geometry.type() == QgsWkbTypes.LineGeometry:
                    parts = [
                        "(" + ", ".join(format_point(point) for point in line) + ")"
                        for line in geometry.asMultiPolyline()
                    ]
                    wkt = f"MULTILINESTRING ({', '.join(parts)})"
                else:
                    wkt = geometry.asWkt()  # For other geometry types, default to asWkt
            else:
                if geometry.type() == QgsWkbTypes.LineGeometry:
                    points = ", ".join(format_point(point) for point in geometry.asPolyline())
                    wkt = f"LINESTRING ({points})"
                else:
                    wkt = geometry.asWkt()  # For other geometry types, default to asWkt
            return wkt
        except Exception as e:
            QgsMessageLog.logMessage(f"Error in round_wkt_coordinates, entered with {geometry}: {e}", "StalpiAssist", level=Qgis.Critical)
            return None
    
    def verify_null(self, layer, field):
        """
        Verifies if the given field contains any NULL values in the layer.
        
        :param layer: QgsVectorLayer object to check.
        :param field: Name of the field to verify.
        """
        null_count = 0
        for feature in layer.getFeatures():
            if feature[field] in ["NULL", None, "nan"]:
                null_count += 1
                
        if null_count:
            return False
        else:
            return True
            
    
    
    # Preprocess photos
    def copy_photos(self, base_dir):
            # Function to copy a single file
        def copy_file(src, dest):
            try:
                shutil.copy(src, dest)
            except Exception as e:
                print(f"Error copying file {src} to {dest}: {e}")

        # Access the layer STALP_XML_
        layer = QgsProject.instance().mapLayersByName('STALP_XML_')[0]

        # Collect file operations in a list
        file_operations = []

        for feature in layer.getFeatures():
            for img_field, name_field in zip(
                ['IMG_FILE_1', 'IMG_FILE_2', 'IMG_FILE_3', 'IMG_FILE_4'],
                ['new_name_1', 'new_name_2', 'new_name_3', 'new_name_4']
            ):
                img_file = feature[img_field]
                new_name = feature[name_field]

                if img_file and os.path.exists(img_file):
                    new_path = os.path.join(base_dir, new_name + os.path.splitext(img_file)[1])
                    file_operations.append((img_file, new_path))

        # Use threading to copy files in parallel
        with ThreadPoolExecutor(max_workers=8) as executor:
            executor.map(lambda op: copy_file(*op), file_operations)

        print("Photos copied and renamed successfully.")

    # Update column path #NOTE: have the script
    def update_column_path(self, layer):
        # Access the layer named "STALP_XML_"
        layer = QgsProject.instance().mapLayersByName("STALP_XML_")[0]

        # Prompt the user to enter the base text using a pop-up window
        base_text, ok = QInputDialog.getText(None, "Enter Base Text", "Enter the base text for IMG_FILE fields:")

        # Proceed only if the user pressed OK and entered a text
        if ok and base_text:
            # Start an edit session for the layer
            layer.startEditing()

            # Use a single list to store the updates
            features_to_update = []

            # Loop through each feature to prepare updates
            for feature in layer.getFeatures():
                # Update field values in memory
                feature['IMG_FILE_1'] = f"{base_text}/{feature['new_name_1']}.JPG"
                feature['IMG_FILE_2'] = f"{base_text}/{feature['new_name_2']}.JPG"
                feature['IMG_FILE_3'] = f"{base_text}/{feature['new_name_3']}.JPG"
                feature['IMG_FILE_4'] = f"{base_text}/{feature['new_name_4']}.JPG"
                
                # Add feature to the update list
                features_to_update.append(feature)

            # Use a batch update to apply all changes at once
            layer.dataProvider().changeAttributeValues({
                feature.id(): {
                    layer.fields().indexOf('IMG_FILE_1'): feature['IMG_FILE_1'],
                    layer.fields().indexOf('IMG_FILE_2'): feature['IMG_FILE_2'],
                    layer.fields().indexOf('IMG_FILE_3'): feature['IMG_FILE_3'],
                    layer.fields().indexOf('IMG_FILE_4'): feature['IMG_FILE_4'],
                }
                for feature in features_to_update
            })

            # Save the edits
            layer.commitChanges()

            print("IMG_FILE_1, IMG_FILE_2, IMG_FILE_3, and IMG_FILE_4 have been updated with the entered base text.")
        else:
            print("Operation canceled or no text entered.")
            
    # Offset 3 on both sides
    def offset_sides(self, layer, offset=3):
        pass
    
    
    # Generate xml/xlsx files, replace blanks with apostrophes
    # def generate_files(self, layers, base_dir):
    #     """
    #     Generates XML and XLSX files for the columns of given layers, skipping any column named 'fid'.
    #     Replaces blanks in column names with apostrophes.
        
    #     :param layers: List of QgsVectorLayer objects to process.
    #     :param base_dir: Directory where the files will be saved.
    #     """
    #     if not os.path.exists(base_dir):
    #         os.makedirs(base_dir)
        
    #     for layer in layers:
    #         layer_name = layer.name()
    #         safe_layer_name = layer_name.replace(" ", "_")  # Replace spaces in layer name
            
    #         # XML file generation
    #         xml_path = os.path.join(base_dir, f"{safe_layer_name}.xml")
    #         root = ET.Element("Layer")
    #         root.set("name", layer_name)
            
    #         for field in layer.fields():
    #             if field.name().lower() != "fid":  # Skip 'fid'
    #                 field_elem = ET.SubElement(root, "Field")
    #                 field_name = field.name().replace(" ", "'")  # Replace blanks with apostrophes
    #                 field_elem.set("name", field_name)
    #                 field_elem.set("type", field.typeName())
            
    #         tree = ET.ElementTree(root)
    #         tree.write(xml_path, encoding="utf-8-sig", xml_declaration=True)
            
    #         # XLSX file generation
    #         xlsx_path = os.path.join(base_dir, f"{safe_layer_name}.xlsx")
    #         workbook = xlsxwriter.Workbook(xlsx_path)
    #         worksheet = workbook.add_worksheet()
            
    #         # Write header row
    #         headers = [field.name().replace(" ", "'") for field in layer.fields() if field.name().lower() != "fid"]
    #         for col_idx, header in enumerate(headers):
    #             worksheet.write(0, col_idx, header)
            
    #         # Write rows (data for illustration, can include actual feature data if needed)
    #         for row_idx, feature in enumerate(layer.getFeatures(), start=1):
    #             for col_idx, field in enumerate(layer.fields()):
    #                 if field.name().lower() != "fid":  # Skip 'fid'
    #                     value = feature[field.name()]
    #                     worksheet.write(row_idx, col_idx, value)
            
    #         workbook.close()
            
    #         print(f"Generated files for layer '{layer_name}':")
        
    # MARK: HELPER
    def update_step(self, steps_list, index, success=True):
        """Marks a step as done by updating the list item."""
        try:
            item = steps_list.item(index)
            # QgsMessageLog.logMessage(f"Updating step {index}: {item.text()}", "StalpiAssist", level=Qgis.Info)
            if success:
                item.setText("✓ " + item.text())  # Add a checkmark
                item.setForeground(QColor("green"))  # Change text color to green to indicate completion
            elif success is None:
                item.setText("⚠ " + item.text())
                item.setForeground(QColor("orange"))  # Change text color to orange to indicate partial completion
            else:
                item.setText("✗ " + item.text())
                item.setForeground(QColor("red"))  # Change text color to red to indicate failure
            item.setFont(QFont("Arial", 10, QFont.Bold))  # Make the completed step bold
            QApplication.processEvents()  # Force UI update after each step
        except Exception as e:
            QgsMessageLog.logMessage(f"Error updating step {index}: {e}", "StalpiAssist", level=Qgis.Critical)
            pass

    # Retrieve layers by name from the QGIS project
    def get_layers(self):
        '''
        Get layers by name from the QGIS project and add them to self.layers
        '''
        QgsMessageLog.logMessage("Retrieving layers from the QGIS project...", "StalpiAssist", level=Qgis.Info)
        layers = {}
        layer_names = ['STALP_JT', 'TRONSON_JT', 'BRANS_FIRI_GRPM_JT', 'FB pe C LES', 'FIRIDA_RETEA_JT', 'GRID_GEIOD', 'PTCZ_PTAB', 'TRONSON_XML_', 'TRONSON_ARANJARE', 'poze', 'FIRIDA_XML_', 'BRANSAMENT_XML_', 'GRUP_MASURA_XML_', 'STALP_XML_', 'DESCHIDERI_XML_', 'TRONSON_predare_xml', 'LINIE_MACHETA', 'STALPI_MACHETA', 'TRONSON_MACHETA', 'FIRIDA MACHETA', 'GRUP MASURA MACHETA', 'DESCHIDERI MACHETA', 'BRANSAMENTE MACHETA', 'LINIE_JT']
        
        # Get all layers in the current QGIS project (keep the layer objects)
        qgis_layers = QgsProject.instance().mapLayers().values()
        QgsMessageLog.logMessage(f"----------- QGIS LAYERS: {qgis_layers}", "StalpiAssist", level=Qgis.Info)

        # Iterate through the actual layer objects
        for layer_name in layer_names:
            layer = next((l for l in qgis_layers if l.name() == layer_name), None)
            layers[layer_name] = layer  # Add the layer if found, else None
            # QgsMessageLog.logMessage(f"Layer found: key: {layer_name}, value: {layer}", "StalpiAssist", level=Qgis.Info)

        # QgsMessageLog.logMessage(f"Layers found with IDs: {layers}", "StalpiAssist", level=Qgis.Info)
        return layers
    
    def update_layer_names(self):
        '''
        Rename layer names - InceputLinie = 1InceputLinie, Cutii = 2Cutii, Stalpi = 3Stalpi, BMPnou = 4BMPnou, AUXILIAR = 5AUXILIAR, pct_vrtx = 6pct_vrtx
        '''
        
        # Get all layers in the current QGIS project
        qgis_layers = QgsProject.instance().mapLayers().values()
        # QgsMessageLog.logMessage(f"----------- QGIS LAYERS: {qgis_layers}", "StalpiAssist", level=Qgis.Info)
        
        # Iterate through the actual layer objects
        for layer in qgis_layers:
            layer_name = layer.name()
            if layer_name.endswith('InceputLinie'):
                layer.setName('1InceputLinie')
            elif layer_name.endswith('Cutii'):
                layer.setName('2Cutii')
            elif layer_name.endswith('Stalpi'):
                layer.setName('3Stalpi')
            elif layer_name.endswith('BMPnou'):
                layer.setName('4BMPnou')
            elif layer_name.endswith('AUXILIAR'):
                layer.setName('5AUXILIAR')
            elif layer_name.endswith('pct_vrtx'):
                layer.setName('6pct_vrtx')
            else:
                pass
            # QgsMessageLog.logMessage(f"Layer renamed: {layer_name}", "StalpiAssist", level=Qgis.Info)

    def add_layer_to_project(self, layer_path):
        try:
            # Get the name of the layer without the file extension and the full path
            layer_name = os.path.splitext(os.path.basename(layer_path))[0]
            
            # Load the merged layer from the output path
            merged_layer = QgsVectorLayer(layer_path, layer_name, 'ogr')
            
            # Check if the layer is valid
            if not merged_layer.isValid():
                QgsMessageLog.logMessage(f"Invalid layer: {layer_path}", "StalpiAssist", level=Qgis.Critical)
                return
            
            # Add the layer to the project with the proper name
            QgsProject.instance().addMapLayer(merged_layer)
            # QgsMessageLog.logMessage(f"Layer added to project with name '{layer_name}': {layer_path}", "StalpiAssist", level=Qgis.Info)
            
        except Exception as e:
            QgsMessageLog.logMessage(f"Error adding layer to project: {e}", "StalpiAssist", level=Qgis.Critical)
            
            
    def run_algorithm(algorithm, params, context, feedback, outputs):
        try:
            results = algorithm.processAlgorithm(params, context, feedback)
            
            # Check if `outputs` is a list and validate all items
            if isinstance(outputs, list):
                found_all = True
                found_any = False
                
                for output in outputs:
                    if output in results and results[output]:
                        found_any = True
                    else:
                        found_all = False
                
                if found_all:
                    return True  # All outputs found and valid
                elif found_any:
                    return None  # Some outputs found but not all
                else:
                    return False  # No outputs found
            else:
                # Single output validation
                if outputs in results and results[outputs]:
                    return True
                return False
        except Exception as e:
            # Log the error for debugging
            print(f"Error running algorithm: {e}")
            return False
