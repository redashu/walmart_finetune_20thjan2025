# -*- coding: utf-8 -*-
"""ashuday2_finetuneGPT4omini.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QbodCPUkw66PqNR-TOBapzQuOi3BcQzx
"""

#pip install openai

from collections import defaultdict
import json
from openai import OpenAI

# connecting to openai API
ashuKey = ""
client = OpenAI(api_key=ashuKey)

# lets verify that we have correct json data
mydata_path = "/content/ashudataset.jsonl"
dataset = []
# loading this dataset
with open(mydata_path, 'r') as f:
    for line in f:
        data = json.loads(line)
        dataset.append(data)

# info about data
print("number of examples in datasets ",len(dataset))
print("first sample of dataset")
for firstdata in dataset[0]["messages"]:
  print(firstdata)

"""**validataion of internal structure of jsonl data is also required**"""

# Format error checks
format_errors = defaultdict(int)

for ex in dataset:
    if not isinstance(ex, dict):
        format_errors["data_type"] += 1
        continue

    messages = ex.get("messages", None)
    if not messages:
        format_errors["missing_messages_list"] += 1
        continue

    for message in messages:
        if "role" not in message or "content" not in message:
            format_errors["message_missing_key"] += 1

        if any(k not in ("role", "content", "name", "function_call", "weight") for k in message):
            format_errors["message_unrecognized_key"] += 1

        if message.get("role", None) not in ("system", "user", "assistant", "function"):
            format_errors["unrecognized_role"] += 1

        content = message.get("content", None)
        function_call = message.get("function_call", None)

        if (not content and not function_call) or not isinstance(content, str):
            format_errors["missing_content"] += 1

    if not any(message.get("role", None) == "assistant" for message in messages):
        format_errors["example_missing_assistant_message"] += 1

if format_errors:
    print("Found errors:")
    for k, v in format_errors.items():
        print(f"{k}: {v}")
else:
    print("No errors found")

# cost estimation
# compute token lenght for each messages
convo_lens = [sum(len(data2["content"]) for data2 in data1["messages"]) for data1 in dataset]
# Pricing and default n_epochs estimate
MAX_TOKENS_PER_EXAMPLE = 16385

TARGET_EPOCHS = 3
MIN_TARGET_EXAMPLES = 100
MAX_TARGET_EXAMPLES = 25000
MIN_DEFAULT_EPOCHS = 1
MAX_DEFAULT_EPOCHS = 25

n_epochs = TARGET_EPOCHS
n_train_examples = len(dataset)
if n_train_examples * TARGET_EPOCHS < MIN_TARGET_EXAMPLES:
    n_epochs = min(MAX_DEFAULT_EPOCHS, MIN_TARGET_EXAMPLES // n_train_examples)
elif n_train_examples * TARGET_EPOCHS > MAX_TARGET_EXAMPLES:
    n_epochs = max(MIN_DEFAULT_EPOCHS, MAX_TARGET_EXAMPLES // n_train_examples)

n_billing_tokens_in_dataset = sum(min(MAX_TOKENS_PER_EXAMPLE, length) for length in convo_lens)
print(f"Dataset has ~{n_billing_tokens_in_dataset} tokens that will be charged for during training")
print(f"By default, you'll train for {n_epochs} epochs on this dataset")
print(f"By default, you'll be charged for ~{n_epochs * n_billing_tokens_in_dataset} tokens")

# using file to openai for fine tuning
ashu_file_response = client.files.create(
  file=open(mydata_path, "rb"),
  purpose='fine-tune'
)
# printing file id
ashu_file_id = ashu_file_response.id
print(ashu_file_id)

# defining the suffix name of my model
ashu_model_suffix = "ashu_modelsarcastic_openaicode"
# creating a job to fine tune gpt4o-mini using above file id
ashu_fine_tune_response = client.fine_tuning.jobs.create(
    training_file=ashu_file_id,
    model="gpt-4o-mini-2024-07-18",
    suffix=ashu_model_suffix,
    hyperparameters={
        "n_epochs": 4
    }
)
# list events of fine tuning progress
ashu_fine_tune_events = client.fine_tuning.jobs.list_events(fine_tuning_job_id=ashu_fine_tune_response.id)
print(ashu_fine_tune_events)

# list all models in my account
ashu_models = client.models.list()
for model in ashu_models.data:
  if "openaicode" in model.id:
    print(model.id)