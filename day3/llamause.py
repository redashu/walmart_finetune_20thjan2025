# import section 
import json
from transformers import AutoTokenizer, AutoModelForCausalLM,pipeline
# loading token from config.json
config = json.load(open('config.json'))
my_token = config['HF_TOKEN']

# choosing model name to intract 
model_name = "meta-llama/Llama-3.2-1B"

# using tokenizer from transformers
my_tokenizer=AutoTokenizer.from_pretrained(model_name,
                              token=my_token)
# use this model with our device like cpu or GPU
my_loaded_model = AutoModelForCausalLM.from_pretrained(model_name,
                                     token=my_token,
                                     device_map='auto' # selecting cpu / gpu(gpu)
                                   ) 
# can be used for many purpose 
# for evaluation , fine tuning , parameter 
my_model_eval = my_loaded_model.eval() # setting model to evaluation mode

# using pipeline to generate response of particular type
my_pipeline = pipeline(
    model=my_model_eval,
    tokenizer=my_tokenizer,
    return_full_text=True,
    task='text-generation',
    max_new_tokens=256
)
