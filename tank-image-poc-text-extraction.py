from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import time
import os
from dotenv import load_dotenv

print("Initializing text extraction...")

start_time = time.time()


# Setup
# Load variables from .env
load_dotenv()

#key = os.getenv("TEXT_EXTRACTION_KEY")  # Use the key for the Text Extraction resource
#endpoint = "https://docintelligenceramar1.cognitiveservices.azure.com/" # Endpoint for the Azure Form Recognizer resource
#model_id = "Model2024.04.28-1"  # ID model created in Azure Form Recognizer Studio

key = os.getenv("TEXT_EXTRACTION_KEY_TB_SP")  # Use the key for the Text Extraction resource
endpoint = "https://docintelligencesp-inspection-development.cognitiveservices.azure.com/"  # Endpoint TB-SP
model_id = "Model2025.08.28-Trinity1-Dev"  # Model ID created in Azure Form Recognizer Studio (SP-PropaneInspection-OCR-Dev Project)

document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)
#Open file from local repo (read as binary data)
#image_path = "./Images/Trinity-model-test1.jpg" 
#image_path = "./Images/Trinity-model-test2.png" 
image_path = "./Images/Trinity-model-test3.png" 

with open(image_path, "rb") as f:
        poller = document_analysis_client.begin_analyze_document(
        model_id=model_id, document=f
    )

result = poller.result()

# Known (expected) field names based on the created model
# expected_fields = {"Seria Number", "Date", "Certified"} #Personal account
expected_fields = {
    "Serial",
    "Model",
    "Size",
    "Year"
}

# Print extracted fields and values
print("\n=== Fields Matched to Model Labels ===")
matched_fields = set()

for field_name, field in result.documents[0].fields.items():
    #print(f"Field: {field_name}, Value: {field.value}, Confidence: {field.confidence:.2f}, Bouding Box: {field.bounding_regions}")
    print(f"Field: {field_name}, Value: {field.value}, Confidence: {field.confidence:.2f}")
    matched_fields.add(field_name)

# Now print ALL raw text blocks that didn't match expected fields
print("\n=== Unmatched Extracted Text (Suspected Missing Fields) ===")
unmatched_texts = []

for page in result.pages:
    for line in page.lines:
        line_text = line.content.strip()
        if not any(expected.lower() in line_text.lower() for expected in expected_fields):
            unmatched_texts.append(line_text)

# Remove duplicates
unmatched_texts = list(set(unmatched_texts))

# Print them
for text in unmatched_texts:
    print(f"- {text}")

end_time = time.time()
duration = end_time - start_time

print("\n=============")
print(f"Execution time: {duration:.4f} seconds")