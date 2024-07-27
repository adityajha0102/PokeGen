import os
from langchain_huggingface.llms import HuggingFaceEndpoint

llm = HuggingFaceEndpoint(
    endpoint_url = os.environ.get('LLM_ENDPOINT'),
    task="text-generation",
    max_new_tokens=4096,
    do_sample=False,
    huggingfacehub_api_token = os.environ.get('HF_TOKEN')
)



