from transformers import pipeline

label_map = {
    "LABEL_0": "Not Obsolete",
    "LABEL_1": "Obsolete",
    "LABEL_2": "Uncertain"
}

improvement_suggestions = {
    "Not Obsolete": "No immediate action needed. The component is up to date.",
    "Obsolete": "Consider updating the component to the latest version or replacing it with a supported alternative.",
    "Uncertain": "Further analysis is recommended to determine the obsolescence status."
}

def classify_obsolescence(text):
    classifier = pipeline("text-classification", model="roberta-base")
    raw_output = classifier(text)
    # Map labels to human-readable labels and add suggestions if obsolete
    mapped_output = []
    for item in raw_output:
        label = item.get("label")
        human_label = label_map.get(label, label)
        result_item = {"label": human_label, "score": item.get("score")}
        if human_label == "Obsolete":
            result_item["suggestion"] = improvement_suggestions.get(human_label)
        mapped_output.append(result_item)
    return mapped_output

def query_sagemaker(text):
    import boto3, json
    client = boto3.client("sagemaker-runtime")
    response = client.invoke_endpoint(
        EndpointName="bert-obsolescence-endpoint",
        ContentType="application/json",
        Body=json.dumps({"inputs": text})
    )
    raw_output = json.loads(response["Body"].read())
    # Map labels to human-readable labels and add suggestions if obsolete
    mapped_output = []
    for item in raw_output:
        label = item.get("label")
        human_label = label_map.get(label, label)
        result_item = {"label": human_label, "score": item.get("score")}
        if human_label == "Obsolete":
            result_item["suggestion"] = improvement_suggestions.get(human_label)
        mapped_output.append(result_item)
    return mapped_output
