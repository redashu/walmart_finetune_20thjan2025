from openai import OpenAI
# my api keys 
ashu_apiKey = ""
# Initializing openAI client with my api KEy 
api_client = OpenAI(api_key=ashu_apiKey)

# lets query the fine tuned model 
api_response = api_client.chat.completions.create(
    model="",
    messages=[
        {"role": "system", "content": "Ashu is a factual chatbot that is also sarcastic."},
        {"role": "user", "content": "can i feel the speed of light ?"}
    ]
)
# print the response 
print(api_response.choices[0].message.content)