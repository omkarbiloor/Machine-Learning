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
            self.log_writer.log(
                self.file_object,
                f"📑 Schema Extracted | DateStamp: {LengthOfDateStampInFile}, TimeStamp: {LengthOfTimeStampInFile}, Columns: {noofcolumns}"
            )

            # Generate regex pattern and validate filenames
            regex = self.raw_data.manualRegexCreation()
            self.log_writer.log(self.file_object, f"🔍 Regex Pattern for Validation: {regex}")
            self.raw_data.validationFileNameRaw(regex, LengthOfDateStampInFile, LengthOfTimeStampInFile)

            # Validate columns
            self.raw_data.validateColumnLength(noofcolumns)
            self.raw_data.validateMissingValuesInWholeColumn()
            self.log_writer.log(self.file_object, "✅ Column Validation Completed")

            # Transform data
            self.log_writer.log(self.file_object, "🔄 Replacing missing values with NULL")
            self.dataTransform.replaceMissingWithNull()
            self.log_writer.log(self.file_object, "✅ Data Transformation Completed")

            # Create Prediction DB & Table
            self.log_writer.log(self.file_object, "🛠️ Creating Prediction Database and Table")
            self.dBOperation.createTableDb('Prediction', column_names)
            self.log_writer.log(self.file_object, "✅ Table Creation Successful")

            # Insert Good Data
            self.log_writer.log(self.file_object, "📥 Inserting Cleaned Data into Prediction Table")
            self.dBOperation.insertIntoTableGoodData('Prediction')
            self.log_writer.log(self.file_object, "✅ Data Insertion Successful")

            # Clean Good Data Folder
            self.log_writer.log(self.file_object, "🧹 Deleting Good Data Folder")
            self.raw_data.deleteExistingGoodDataTrainingFolder()
            self.log_writer.log(self.file_object, "✅ Good Data Folder Deleted")

            # Archive Bad Files
            self.log_writer.log(self.file_object, "📦 Archiving Bad Files")
            self.raw_data.moveBadFilesToArchiveBad()
            self.log_writer.log(self.file_object, "✅ Bad Files Archived")

            # Export CSV
            self.log_writer.log(self.file_object, "📤 Exporting Final Prediction File")
            self.dBOperation.selectingDatafromtableintocsv('Prediction')
            self.log_writer.log(self.file_object, "🎯 Prediction Validation Completed Successfully")

        except Exception as e:
            self.log_writer.log(self.file_object, f"❌ Exception during validation: {str(e)}")
            raise e
