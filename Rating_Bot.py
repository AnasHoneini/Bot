import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def main():
    input_file = './Data.xlsx'
    data = pd.read_excel(input_file, sheet_name='SampleConvos')

    for index, row in data.iterrows():
        conversation = row['Conversation']
        industry = row['Industry']
        rating, tokens_used = rate_conversation(conversation, industry)
        data.at[index, 'Rating'] = rating
        data.at[index, 'Cost'] = f"input: {tokens_used} tokens / output: 1 token"

    data.to_excel(input_file, sheet_name='SampleConvos', index=False)
    
def rate_conversation(conversation, industry):
    prompt = f"Rate the following conversation:\n{conversation} in the {industry} industry\n\nChoose only one word for the rating: Excellent, Good, Average, Poor, Terrible."
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an assistant that rates conversations."},
            {"role": "user", "content": prompt}
        ],
       
    )
    rating = response.choices[0].message.content.strip()
    tokens_used = response.usage.total_tokens
    return rating, tokens_used

if __name__ == "__main__":
    main()
