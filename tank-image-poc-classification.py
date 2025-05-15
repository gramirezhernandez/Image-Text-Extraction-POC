
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import time
import os
from dotenv import load_dotenv

print("Initializing clasiffication...")

ini_time = time.time()

# Setup
# Load variables from .env
load_dotenv()
prediction_key = os.getenv("CLASSIFICATION_PREDICTION_KEY")

endpoint = "https://predictionresourcegr1.cognitiveservices.azure.com/"
project_id = "08796df1-8077-4e92-bf91-69800419a481"
published_name = "Iteration1"

credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(endpoint, credentials)

# Prediction
with open("Trinity2_Image_1.png", "rb") as image_data:
    results = predictor.classify_image(project_id, published_name, image_data.read())

for prediction in results.predictions:
    print(f"{prediction.tag_name}: {prediction.probability:.2f}")

end_time = time.time()
exec_time = end_time - ini_time
print("--------")
print(f"Execution time: {exec_time:.4f} seconds")


