from typing import Any

from anthropic.types import Message, RawContentBlockDeltaEvent, RawContentBlockStartEvent, RawContentBlockStopEvent, \
    RawMessageDeltaEvent, RawMessageStartEvent, RawMessageStopEvent
from dotenv import load_dotenv
from anthropic import Anthropic, Stream


def main():
    # load environment variable
    load_dotenv()

    # automatically looks for an "ANTHROPIC_API_KEY" environment variable
    client = Anthropic()

    # our_first_message = build_format_string_requests(client)

    # build chatbot with given criteria
    # it's a multi-turn conversation, so we need to keep track of the conversation history
    # keep a list to store the conversation history
    # ask user for input, and append it to the conversation history
    # send message history to the model, and get the response
    # add Claude assistant's response to the conversation history
    # Go back to step 1 and repeat until the user wants to exit
    build_chatbot(client)


def build_chatbot(client: Anthropic) -> None:
    conversation_history = []

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chatbot...")
            break

        conversation_history.append({"role": "user", "content": user_input})

        response = client.messages.create(
            model="claude-haiku-5-5",
            max_tokens=200,
            messages=conversation_history,
        )

        assistant_response = response.content[0].text
        print(f"Claude: {assistant_response}")

        conversation_history.append({"role": "assistant", "content": assistant_response})


def build_format_string_requests(client: Anthropic) -> Any:
    # create a translation request from english to another language
    # using string format
    language = input("Enter the target language: ")
    english_text = input("Enter the English text to translate: ")

    our_first_message = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=200,
        messages=[
            {"role": "user", "content": f"Translate the following English text to {language}: {english_text}"}
        ],
    )

    print(our_first_message.content[0].text)

    return our_first_message


if __name__ == "__main__":
    main()
