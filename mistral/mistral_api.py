import os
import openai

def get_mistral_response(prompt):

    client = openai.OpenAI(
        api_key=os.environ['mistral_api_token'],
        base_url="https://api.mistral.ai/v1"  # <- required!
    )
    response = client.chat.completions.create(
        model="mistral-medium",
        messages=[
            {"role": "system", "content": "You write a description of this data in a humurous way that is extremely concise like maybe 7 words max"},
            {"role": "user", "content":prompt}
        ]
    )
    return response.choices[0].message.content

