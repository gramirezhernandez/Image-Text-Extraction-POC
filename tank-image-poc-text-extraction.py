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
key = os.getenv("TEXT_EXTRACTION_KEY")

endpoint = "https://docintelligenceramar1.cognitiveservices.azure.com/"
model_id = "Model2024.04.28-1"  # use "prebuilt-document" or custom ID

document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)
#Open file (read as binary data)
with open("PropaneTank1.PNG", "rb") as f:
    poller = document_analysis_client.begin_analyze_document(
        model_id=model_id, document=f
    )

result = poller.result()

# Known (expected) field names based on the created model
expected_fields = {"Seria Number", "Date", "Certified"} 

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