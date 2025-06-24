from sagemaker.huggingface import HuggingFaceModel
import sagemaker

role = "arn:aws:iam::YOUR_ACCOUNT_ID:role/YOUR_SAGEMAKER_ROLE"  # Replace this

huggingface_model = HuggingFaceModel(
    transformers_version="4.26",
    pytorch_version="1.13",
    py_version="py39",
    entry_point="inference.py",
    source_dir="./hf_model",
    role=role
)

predictor = huggingface_model.deploy(
    initial_instance_count=1,
    instance_type="ml.t2.medium",
    endpoint_name="bert-obsolescence-endpoint"
)
