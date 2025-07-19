from datetime import datetime
from Prediction_Raw_Data_Validation.predictionDataValidation import Prediction_Data_validation
from DataTypeValidation_Insertion_Prediction.DataTypeValidationPrediction import dBOperation
from DataTransformation_Prediction.DataTransformationPrediction import dataTransformPredict
from application_logging import logger

class pred_validation:
    def __init__(self, path):
        self.raw_data = Prediction_Data_validation(path)
        self.dataTransform = dataTransformPredict()
        self.dBOperation = dBOperation()
        self.file_object = open("Prediction_Logs/Prediction_Log.txt", 'a+')
        self.log_writer = logger.App_Logger()

    def prediction_validation(self):
        try:
            self.log_writer.log(self.file_object, '▶️ Start of Validation on files for prediction!')

            # Extracting schema details
            LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, noofcolumns = self.raw_data.valuesFromSchema()
            self.log_writer.log(self.file_object, f"📑 Schema Details Extracted - DateStampLen: {LengthOfDateStampInFile}, TimeStampLen: {LengthOfTimeStampInFile}, Columns: {noofcolumns}")

            # Generate regex pattern and validate filenames
            regex = self.raw_data.manualRegexCreation()
            self.log_writer.log(self.file_object, f"🔍 Using Regex: {regex} for filename validation")
            self.raw_data.validationFileNameRaw(regex, LengthOfDateStampInFile, LengthOfTimeStampInFile)

            # Column validation
            self.raw_data.validateColumnLength(noofcolumns)
            self.raw_data.validateMissingValuesInWholeColumn()
            self.log_writer.log(self.file_object, "✅ Raw Data Validation Complete")

            # Data transformation
            self.log_writer.log(self.file_object, "🔄 Starting Data Transformation")
            self.dataTransform.replaceMissingWithNull()
            self.log_writer.log(self.file_object, "✅ Data Transformation Completed")

            # Create prediction DB and table
            self.log_writer.log(self.file_object, "🗄️ Creating Prediction Database and Tables")
            self.dBOperation.createTableDb('Prediction', column_names)
            self.log_writer.log(self.file_object, "✅ Table Creation Completed")

            # Insert good data into table
            self.log_writer.log(self.file_object, "📥 Inserting Validated Data into Table")
            self.dBOperation.insertIntoTableGoodData('Prediction')
            self.log_writer.log(self.file_object, "✅ Data Inserted Successfully")

            # Clean-up: Remove folders and archive bad files
            self.log_writer.log(self.file_object, "🧹 Cleaning Good Data Folder")
            self.raw_data.deleteExistingGoodDataTrainingFolder()
            self.log_writer.log(self.file_object, "✅ Good Data Folder Deleted")

            self.log_writer.log(self.file_object, "📦 Archiving Bad Files")
            self.raw_data.moveBadFilesToArchiveBad()
            self.log_writer.log(self.file_object, "✅ Bad Files Archived and Folder Deleted")

            # Export from DB to final CSV
            self.log_writer.log(self.file_object, "📤 Exporting Final Data from Table to CSV")
            self.dBOperation.selectingDatafromtableintocsv('Prediction')
            self.log_writer.log(self.file_object, "🎯 Prediction Validation Workflow Complete")

        except Exception as e:
            self.log_writer.log(self.file_object, f"❌ Error during prediction validation: {str(e)}")
            raise e
