from openai import OpenAI
# my api keys 
ashu_apiKey = ""
# Initializing openAI client with my api KEy 
api_client = OpenAI(api_key=ashu_apiKey)

# define user input 
my_query = input("enter query to sarcastic GPT model : ")
# lets query the fine tuned model 
api_response = api_client.chat.completions.create(
    model="ft:gpt-4o-mini-2024-07-18:delvex:ashu-modelsarcastic-openaicode:As2elBnD",
    messages=[
        {"role": "system", "content": "Ashutoshh is a factual chatbot that is also sarcastic."},
        {"role": "user", "content": my_query}
    ]
)
# print the response 
print(api_response.choices[0].message.content)