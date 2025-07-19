import pandas as pd
import numpy as np
from file_operations import file_methods
from data_preprocessing import preprocessing
from data_ingestion import data_loader_prediction
from application_logging import logger
from Prediction_Raw_Data_Validation.predictionDataValidation import Prediction_Data_validation


class prediction:

    def __init__(self, path):
        self.file_object = open("Prediction_Logs/Prediction_Log.txt", 'a+')
        self.log_writer = logger.App_Logger()
        self.pred_data_val = Prediction_Data_validation(path)

    def predictionFromModel(self):
        try:
            # Step 1: Clean up previous predictions
            self.pred_data_val.deletePredictionFile()
            self.log_writer.log(self.file_object, 'Start of Prediction')

            # Step 2: Load data
            data_getter = data_loader_prediction.Data_Getter_Pred(self.file_object, self.log_writer)
            data = data_getter.get_data()

            # Step 3: Preprocess data
            preprocessor = preprocessing.Preprocessor(self.file_object, self.log_writer)
            is_null_present, cols_with_missing_values = preprocessor.is_null_present(data)
            if is_null_present:
                data = preprocessor.impute_missing_values(data, cols_with_missing_values)
            X = preprocessor.scale_numerical_columns(data)

            # Step 4: Load KMeans model and predict clusters
            file_loader = file_methods.File_Operation(self.file_object, self.log_writer)
            kmeans = file_loader.load_model('KMeans')
            clusters = kmeans.predict(X)
            X['clusters'] = clusters

            # Step 5: Predict with correct model for each cluster
            predictions = []
            for cluster_id in X['clusters'].unique():
                cluster_data = X[X['clusters'] == cluster_id].drop(['clusters'], axis=1)
                model_name = file_loader.find_correct_model_file(cluster_id)
                model = file_loader.load_model(model_name)
                cluster_predictions = model.predict(cluster_data)
                predictions.extend(cluster_predictions)

            # Step 6: Save and return predictions
            final = pd.DataFrame(predictions, columns=['Predictions'])
            output_path = "Prediction_Output_File/Predictions.csv"
            final.to_csv(output_path, header=True, mode='w', index=False)

            self.log_writer.log(self.file_object, 'End of Prediction')

            # Step 7: Return preview to frontend
            preview = final.head(10).to_string(index=False)
            return f"Prediction File created at {output_path}\n\nSample Predictions:\n{preview}"

        except Exception as ex:
            self.log_writer.log(self.file_object, f'Error occurred during prediction: {ex}')
            raise ex
