from pathlib import Path
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QProgressBar, QPushButton, QMessageBox
from qgis.core import QgsProject, QgsMessageLog, Qgis  # type: ignore
from .helper_functions import HelperBase, SHPProcessor
from PyQt5.QtCore import QThread, pyqtSignal
import os
import gc
import uuid
import time
from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException

class GenerateExcelDialog(QDialog):
    
    def __init__(self, base_dir):
        super().__init__()
        self.helper = HelperBase()
        self.base_dir = base_dir
        self.template_path = 'templates'
        self.processor = None
        
        self.setWindowTitle("Generate Anexa")
        self.layout = QVBoxLayout()

        self.progress_bar = QProgressBar(self)
        self.layout.addWidget(self.progress_bar)

        self.run_button = QPushButton("Generate Anexa", self)
        self.run_button.clicked.connect(self.__exec__)
        self.layout.addWidget(self.run_button)

        self.setLayout(self.layout)

    def __exec__(self):
        try:
            layer_names = ['LINIE_JT', 'STALP_XML_', 'BRANSAMENT_XML_', 'GRUP_MASURA_XML_', 'FIRIDA_XML_', 'DESCHIDERI_XML_', 'TRONSON_predare_xml']
            layers = []
            for name in layer_names:
                found_layers = QgsProject.instance().mapLayersByName(name)
                if not found_layers:
                    raise ValueError(f"Layer {name} not found!")
                layers.append(found_layers[0])

            self.progress_bar.setMaximum(len(layers))
            self.progress_bar.setValue(0)

            # Use a separate thread for generation to prevent UI freezing
            self.worker_thread = GenerateExcelWorker(self.base_dir, self.template_path)
            self.worker_thread.progress_updated.connect(self.progress_bar.setValue)
            self.worker_thread.finished.connect(self.on_generation_complete)
            self.worker_thread.start()
        except ValueError as e:
            QgsMessageLog.logMessage(str(e), level=Qgis.Warning)
            QMessageBox.warning(self, "Missing Layers", str(e))
        except Exception as e:
            QgsMessageLog.logMessage(f"Unexpected error: {str(e)}", level=Qgis.Critical)
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def on_generation_complete(self):
        # Notify user when all exports are complete
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Complete")
        msg_box.setText("File generation completed!")
        msg_box.setStandardButtons(QMessageBox.Ok)

        # Show the dialog and wait for the user's response
        if msg_box.exec_() == QMessageBox.Ok:
            self.close()  # Close the plugin dialog

class GenerateExcelWorker(QThread):
    progress_updated = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, base_dir, template_path):
        super().__init__()
        self.helper = HelperBase()
        self.layers = self.helper.get_layers()
        self.base_dir = base_dir
        self.template_path = template_path
        self.processor = None
        
    @staticmethod
    def plugin_path(*args) -> Path:
        """ Return the path to the plugin root folder or file. """
        path = Path(__file__).resolve().parent
        for item in args:
            path = path.joinpath(item)
        return path

    def run(self):
        try:
            self.generate_anexa()
        except Exception as e:
            QgsMessageLog.logMessage(f"Error during generation: {str(e)}", "StalpiAssist", level=Qgis.Critical)
        finally:
            self.finished.emit()
        
    def validate_excel_file(self, file_path):
        for _ in range(3):  # Retry mechanism for potential transient issues
            try:
                workbook = load_workbook(file_path, read_only=True)  # Open in read-only mode
                workbook.close()  # Explicitly close the file handle
                return True
            except (InvalidFileException, ValueError, FileNotFoundError) as e:
                QgsMessageLog.logMessage(f"Excel validation error: {str(e)}", "StalpiAssist", level=Qgis.Critical)
                time.sleep(1)  # Wait and retry
            except Exception as e:
                QgsMessageLog.logMessage(f"Unexpected error during validation: {str(e)}", "StalpiAssist", level=Qgis.Critical)
                return False
        return False
        
    def generate_anexa(self):
        try: 
            QgsMessageLog.logMessage("Starting to process layers.", "StalpiAssist", level=Qgis.Info)
            try:
                self.process_layers()
                QgsMessageLog.logMessage("Layer processing completed.", "StalpiAssist", level=Qgis.Info)
            except Exception as e:
                QgsMessageLog.logMessage(f"Error during layer processing: {str(e)}", "StalpiAssist", level=Qgis.Critical)
                QMessageBox.critical(None, "Layer Processing Error", f"An error occurred while processing layers: {e}")
                return

            # Copy template excel file (templates/anexa.xlsx) to a safe temporary file
            try:
                template_file = self.plugin_path('templates', 'anexa.xlsx')
                QgsMessageLog.logMessage(f"Resolved template file path: {template_file}", "StalpiAssist", level=Qgis.Info)

                if not template_file.exists():
                    raise FileNotFoundError(f"Template file not found at {template_file}")

                temp_copy_path = template_file.with_name(f"anexa_temp_{uuid.uuid4().hex}.xlsx")
                QgsMessageLog.logMessage(f"Creating unique temporary copy: {temp_copy_path}", "StalpiAssist", level=Qgis.Info)
                self.copy_file_with_os(template_file, temp_copy_path)

                if not self.validate_excel_file(temp_copy_path):
                    raise ValueError("Temporary Excel file validation failed.")

                # Edit the temporary file
                destination_path = Path(self.base_dir) / 'anexa.xlsx'
                parser_progress = 0

                for parser in self.processor.parsers:
                    if parser.get_name() in ['LINIE_JT', 'STALP_XML_', 'BRANSAMENT_XML_', 'GRUP_MASURA_XML_', 'FIRIDA_XML_', 'DESCHIDERI_XML_', 'TRONSON_predare_xml']:
                        try:
                            QgsMessageLog.logMessage(f"Processing parser: {parser}", "StalpiAssist", level=Qgis.Info)
                            parser.write_to_excel_sheet(temp_copy_path)
                            parser_progress += 1
                            self.progress_updated.emit(parser_progress)
                            QgsMessageLog.logMessage(f"Parser progress: {parser_progress}/{len(self.processor.parsers)}", "StalpiAssist", level=Qgis.Info)
                        except Exception as e:
                            QgsMessageLog.logMessage(f"Error processing parser {parser.get_name()}: {str(e)}", "StalpiAssist", level=Qgis.Warning)

                # Validate temporary file before moving
                if not self.validate_excel_file(temp_copy_path):
                    raise ValueError("Final Excel file validation failed.")

                # Retry mechanism for moving file
                retries = 3
                for attempt in range(retries):
                    try:
                        QgsMessageLog.logMessage(f"Moving file to final destination: {destination_path}", "StalpiAssist", level=Qgis.Info)
                        os.replace(temp_copy_path, destination_path)
                        break
                    except Exception as e:
                        if attempt < retries - 1:
                            QgsMessageLog.logMessage(f"Retrying file move (attempt {attempt + 1}): {str(e)}", "StalpiAssist", level=Qgis.Warning)
                            time.sleep(1)  # Pause before retry
                        else:
                            raise

            except FileNotFoundError as e:
                QgsMessageLog.logMessage(f"File not found: {str(e)}", "StalpiAssist", level=Qgis.Critical)
                QMessageBox.critical(None, "File Not Found", f"The template file could not be located: {e}")
                return
            except Exception as e:
                QgsMessageLog.logMessage(f"Error during file processing: {str(e)}", "StalpiAssist", level=Qgis.Critical)
                QMessageBox.critical(None, "File Processing Error", f"An error occurred while processing the file: {e}")
                return
        except Exception as e:
            QgsMessageLog.logMessage(f"Unexpected error in generate_anexa: {str(e)}", "StalpiAssist", level=Qgis.Critical)
            QMessageBox.critical(None, "Unexpected Error", f"An unexpected error occurred: {e}")
            return

    def copy_file_with_os(self, source, destination):
        """Copy file using os for better control."""
        try:
            with open(source, 'rb') as src, open(destination, 'wb') as dest:
                dest.write(src.read())
            QgsMessageLog.logMessage(f"File copied successfully from {source} to {destination}", "StalpiAssist", level=Qgis.Info)
        except Exception as e:
            QgsMessageLog.logMessage(f"Error copying file from {source} to {destination}: {str(e)}", "StalpiAssist", level=Qgis.Critical)
            raise

    def process_layers(self):
        old_layers = self.layers
        
        if not self.processor:
            try:
                QgsMessageLog.logMessage("No processor found. Creating new processor.", "StalpiAssist", level=Qgis.Info)
                self.processor = SHPProcessor(self.layers)
            except Exception as e:
                QgsMessageLog.logMessage(f"Error creating processor: {str(e)}", "StalpiAssist", level=Qgis.Critical)
                return
        
        try:
            QgsMessageLog.logMessage("Getting current layers.", "StalpiAssist", level=Qgis.Info)
            current_layers = self.helper.get_layers()
        except Exception as e:
            QgsMessageLog.logMessage(f"Error getting current layers: {str(e)}", "StalpiAssist", level=Qgis.Critical)
            return
        
        if current_layers != old_layers:
            QgsMessageLog.logMessage("Layers have changed. Creating new processor.", "StalpiAssist", level=Qgis.Info)
            self.processor = None
            
            try:
                QgsMessageLog.logMessage("Creating new processor.", "StalpiAssist", level=Qgis.Info)
                self.processor = SHPProcessor(current_layers)
            except Exception as e:
                QgsMessageLog.logMessage(f"Error creating new processor: {str(e)}", "StalpiAssist", level=Qgis.Critical)
                return
        else:
            QgsMessageLog.logMessage("No changes in layers. Processor remains unchanged.", "StalpiAssist", level=Qgis.Info)
