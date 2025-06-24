from transformers import pipeline
import re

label_map = {
    "LABEL_0": "Not Obsolete",
    "LABEL_1": "Obsolete",
    "LABEL_2": "Uncertain"
}

def parse_packages(text):
    """
    Parse package names and versions from requirements.txt or similar text.
    Returns a list of tuples: (package_name, version)
    """
    pattern = re.compile(r'^\s*([a-zA-Z0-9_\-]+)\s*==\s*([^\s]+)', re.MULTILINE)
    packages = pattern.findall(text)
    return packages

import re

def clean_version_string(version):
    """
    Clean and normalize version strings by removing repetitive or redundant parts.
    """
    # Remove repeated '-SNAPSHOT' or similar patterns
    cleaned = re.sub(r'(-SNAPSHOT)+', '-SNAPSHOT', version)
    # Remove excessive repeated version numbers separated by dots or dashes
    cleaned = re.sub(r'(\d+)(\.\1)+', r'\1', cleaned)
    cleaned = re.sub(r'(\d+)(-\1)+', r'\1', cleaned)
    # Remove trailing dots or dashes
    cleaned = re.sub(r'[\.-]+$', '', cleaned)
    return cleaned

def classify_obsolescence(text):
    classifier = pipeline("text-classification", model="roberta-base")
    raw_output = classifier(text)
    mapped_output = []
    packages = parse_packages(text)
    # Use a more capable model for generation if available
    try:
        generator = pipeline("text-generation", model="gpt2-medium")
    except Exception:
        generator = pipeline("text-generation", model="gpt2")
    for item in raw_output:
        label = item.get("label")
        human_label = label_map.get(label, label)
        result_item = {"label": human_label, "score": item.get("score")}
        if human_label in improvement_suggestions:
            if human_label == "Obsolete":
                # Generate dynamic suggestion including package update info
                suggestions = []
                for pkg, ver in packages:
                    clean_ver = clean_version_string(ver)
                    prompt = f"Suggest improvements or upgrades for package {pkg} version {clean_ver}:"
                    outputs = generator(prompt, max_length=150, num_return_sequences=1)
                    suggestion_text = outputs[0]['generated_text'].replace(prompt, '').strip()
                    # Fallback if suggestion is empty or too short
                    if len(suggestion_text) < 10:
                        suggestion_text = "No specific suggestions available."
                    suggestions.append({"package": pkg, "current_version": clean_ver, "suggestion": suggestion_text})
                result_item["suggestion"] = suggestions
            else:
                result_item["suggestion"] = improvement_suggestions.get(human_label)
        mapped_output.append(result_item)
    return mapped_output

#   New function to generate improvement suggestions dynamically using text-generation pipeline
def generate_improvement_suggestion(package_info):
    """
    Generate improvement suggestions for a specific package version using a text-generation model.

    Args:
        package_info (str): Description of the package and version, e.g. "package X version 1.2.3"

    Returns:
        str: Generated suggestion text
    """
    generator = pipeline("text-generation", model="gpt2")
    prompt = f"Suggest improvements or upgrades for {package_info}:"
    outputs = generator(prompt, max_length=100, num_return_sequences=1)
    suggestion = outputs[0]['generated_text'].replace(prompt, '').strip()
    return suggestion

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
        if human_label in improvement_suggestions:
            # Use dynamic suggestion generation for obsolete label
            if human_label == "Obsolete":
                suggestion = generate_improvement_suggestion(text)
                result_item["suggestion"] = suggestion
            else:
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
        if human_label in improvement_suggestions:
            result_item["suggestion"] = improvement_suggestions.get(human_label)
        mapped_output.append(result_item)
    return mapped_output
