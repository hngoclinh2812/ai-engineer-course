from dotenv import load_dotenv
import os
from anthropic import Anthropic

#define main function to run the code
def main():
    load_dotenv()
    my_api_key = os.getenv("ANTHROPIC_API_KEY")
    client = Anthropic()

    our_first_message = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": "Give me a joke about how fat my cat is"}
        ],
    )

    print(our_first_message.content[0].text)

if __name__ == "__main__":
    main()
