from transformers import pipeline
from sagemaker_huggingface_inference_toolkit.handler_service import HuggingFaceHandlerService

class ObsolescenceHandler(HuggingFaceHandlerService):
    def initialize(self, context):
        self.classifier = pipeline("text-classification", model="roberta-base")
        self.label_map = {
            "LABEL_0": "✅ Not Obsolete / Safe",
            "LABEL_1": "⚠️ Possibly Obsolete or Risky"
        }

    def infer(self, data, *args, **kwargs):
        inputs = data.get("inputs", "")
        results = self.classifier(inputs)
        # Replace labels with human-readable ones
        for result in results:
            result["label"] = self.label_map.get(result["label"], result["label"])
        return results
