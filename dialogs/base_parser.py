from qgis.core import QgsProject, QgsVectorLayer, QgsMessageLog, Qgis # type: ignore
import os
import pandas as pd
import traceback

class BaseParser:
    def __init__(self, layer: QgsVectorLayer, layer_name: str):
        self.layer = None
        for l in QgsProject.instance().mapLayers().values():
            if l.name() == layer_name:
                self.layer = l
                break

        if self.layer is None:
            raise ValueError(f"Layer named '{layer_name}' not found in the project.")

        self.invalid_elements = []

    def validate(self):
        self.invalid_elements = []

        def append_error(obj, field, error_msg, rule):
            """Helper function to append validation errors."""
            friendly_name = getattr(obj, 'denumire', None) or getattr(obj, 'denumire_a', None) or f"ID {obj.friendly_id}"
            self.invalid_elements.append({
                'layer_name': self.layer.name(),
                'id': obj.internal_id,
                'tag': field,
                'friendly_name': friendly_name,
                'error': error_msg,
                'suggestions': rule
            })

        for obj in self.data:
            obj_dict = obj.to_dict()
            for field, rule_config in self.validation_rules.items():
                value = obj_dict.get(field, None)
                rule = rule_config.get('rule')
                required = rule_config.get('required', False)
                
                QgsMessageLog.logMessage(f"Validating field {field} with value {value} and rule {rule}", "StalpiAssist", level=Qgis.Info)

                # QgsMessageLog.logMessage(f"Validating field {field} with value {value} and rule {rule}", "StalpiAssist", level=Qgis.Info)

                # Check if the field is required but missing
                if value is None and required:
                    append_error(obj, field, f"Câmpul {field} trebuie să fie completat!", rule)
                    continue
                # Type validation: Check if value is a string
                elif rule == "str" and value is not None and not isinstance(value, str):
                    append_error(obj, field, f"Valoarea '{value}' nu este de tip text", rule)
                    # QgsMessageLog.logMessage(f"Field {field} with value {value} is not of type 'str'", "StalpiAssist", level=Qgis.Warning)
                # Type validation: Check if value is an integer
                elif rule == "int" and value is not None and not isinstance(value, int):
                    append_error(obj, field, f"Valoarea '{value}' nu este de tip număr întreg", rule)
                    # QgsMessageLog.logMessage(f"Field {field} with value {value} is not of type 'int'", "StalpiAssist", level=Qgis.Warning)
                # List validation: Check if value is in a list of valid values
                elif isinstance(rule, list) and value is not None and value not in rule:
                    append_error(obj, field, f"Valoarea '{value}' nu este în lista de valori posibile", rule)
                    # QgsMessageLog.logMessage(f"Field {field} with value {value} is not in the list of valid values", "StalpiAssist", level=Qgis.Warning)

        return self.invalid_elements if self.invalid_elements else []


    def update_feature(self, feature_id, field, value):
        for obj in self.data:
            QgsMessageLog.logMessage(f"Comparing obj.internal_id with feature_id - {obj.internal_id} == {feature_id}?", "StalpiAssist", level=Qgis.Info)
            if obj.internal_id == feature_id:
                # QgsMessageLog.logMessage(f"Found feature {feature_id} in data. Updating field {field} with value {value}", "StalpiAssist", level=Qgis.Info)
                setattr(obj, field, value)
                print(f"Value was changed for Feature {feature_id}: {field} - {value}")
                break
            else:
                QgsMessageLog.logMessage(f"Feature {feature_id} not found in data.", "StalpiAssist", level=Qgis.Warning)

    def save_to_layer(self):
        if not self.layer:
            raise ValueError("Layer is not loaded.")

        if not self.layer.isEditable():
            if not self.layer.startEditing():
                QgsMessageLog.logMessage("Failed to start editing the layer.", "StalpiAssist", Qgis.Warning)
                return

        for obj in self.data:
            if obj.ignored:
                continue
            feature = self.layer.getFeature(obj.internal_id)
            if feature.isValid():
                fields = self.layer.fields()
                QgsMessageLog.logMessage(f"Feature ID {obj.internal_id} found in layer. - {fields}", "StalpiAssist", Qgis.Info)

                success = True
                
                for internal_field, layer_field in self.mapping.items():
                    new_value = getattr(obj, internal_field, None)

                    QgsMessageLog.logMessage(f"Updating field '{layer_field}' with value '{new_value}'", "StalpiAssist", Qgis.Info)
                    
                    field_index = fields.indexFromName(layer_field)
                    if field_index == -1:
                        QgsMessageLog.logMessage(f"Field '{layer_field}' not found in layer.", "StalpiAssist", Qgis.Warning)
                        continue

                    if not self.layer.changeAttributeValue(feature.id(), field_index, new_value):
                        success = False
                        QgsMessageLog.logMessage(f"Failed to update field '{layer_field}' for feature ID {obj.internal_id}.", "StalpiAssist", Qgis.Warning)
                    else:
                        QgsMessageLog.logMessage(f"Feature ID {obj.internal_id}: Field '{layer_field}' updated successfully.", "StalpiAssist", Qgis.Info)


                if not success:
                    QgsMessageLog.logMessage(f"Some attributes could not be updated for feature ID {obj.internal_id}. Rolling back changes.", "StalpiAssist", Qgis.Warning)
                    self.layer.rollBack()
                    return

        if not self.layer.commitChanges():
            QgsMessageLog.logMessage("Failed to commit changes to the layer.", "StalpiAssist", Qgis.Warning)
        else:
            QgsMessageLog.logMessage("Changes successfully committed to the layer.", "StalpiAssist", Qgis.Info)
    

    def export_to_excel(self, output_dir, filename):
        try:
            QgsMessageLog.logMessage("Starting export to CSV...", "StalpiAssist", level=Qgis.Info)

            # Step 1: Validate data
            if not self.data:
                raise ValueError("No data to export.")
            if not filename:
                raise ValueError("Filename not provided.")

            # Step 2: Ensure output directory exists
            if not os.path.exists(output_dir):
                try:
                    os.makedirs(output_dir)
                    QgsMessageLog.logMessage(f"Created output directory: {output_dir}", "StalpiAssist", level=Qgis.Info)
                except Exception as e:
                    raise OSError(f"Failed to create output directory '{output_dir}': {e}")

            # Step 3: Define output path for CSV file and check if file exists
            csv_output_path = os.path.join(output_dir, f"{filename}.csv")

            if os.path.exists(csv_output_path):
                QgsMessageLog.logMessage(f"File '{csv_output_path}' already exists. Skipping export.", "StalpiAssist", level=Qgis.Info)
                return  # Skip if file already exists

            # Step 4: Create DataFrame
            try:
                df = pd.DataFrame([
                    {key: getattr(obj, key, "") for key in self.column_names}
                    for obj in self.data
                ])
                QgsMessageLog.logMessage(f"DataFrame created successfully with columns: {self.column_names}", "StalpiAssist", level=Qgis.Info)
            except Exception as e:
                raise ValueError(f"Failed to create DataFrame: {e}")

            # Step 5: Export DataFrame to CSV
            try:
                df.to_csv(csv_output_path, index=False, encoding='utf-8-sig')
                QgsMessageLog.logMessage(f"Data successfully exported to {csv_output_path}", "StalpiAssist", level=Qgis.Info)

            except Exception as e:
                raise RuntimeError(f"Failed to write CSV file '{csv_output_path}': {e}")

        except Exception as e:
            # Log the detailed error and stack trace for debugging
            error_message = f"An error occurred during the export to CSV: {str(e)}\n{traceback.format_exc()}"
            QgsMessageLog.logMessage(error_message, "StalpiAssist", level=Qgis.Critical)
            # Optionally, inform the user with a message box
            # QMessageBox.critical(None, "Export Error", error_message)




