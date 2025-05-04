import logging

logging.basicConfig(level=logging.INFO)


def log_prediction(input_data, prediction):
    logging.info(f"Input: {input_data} => Prediction: {prediction}")
