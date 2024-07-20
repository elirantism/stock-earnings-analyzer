import openai
import os
from combine import organize_all_data

openai.api_key = os.getenv('NEW_OPEN_AI_KEY')

def get_chatgtp_suggestion(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a financial assistant that will provide suggestions on the top 3 stocks to invest in based on the provided data."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1500,
        temperature=0.7,
    )
    return response.choices[0].message['content'].strip()

def create_prompt():
    data = organize_all_data()
    prompt = ""
    prompt += """It is your job to provide people with the best suggestions for which stocks to invest in. I am going to provide you with a list of 10 companies that are all having their earnings this week. Starting from Monday, the list will provide you with 2 companies per day until Friday. Each company in the list will have an abundance of historical and current data that will help you make your suggestion. The data consists of historical data, financials, marketcap, current price, eps (earnings per share), and recent news headlines. It is your job to use this information to provide me with the top 3 companies that you suggest I should invest in for that given week."""

    prompt += '\n'
    prompt += '\n'
    prompt += '\n'
    prompt += "COMPANY DATA:"
    prompt += '\n'
    prompt += data

    return prompt


print(get_chatgtp_suggestion(create_prompt()))
    