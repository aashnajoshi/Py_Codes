# openai==0.28
import openai

api_key = ""
openai.api_key = api_key

print("Welcome! How can I assist you today?\n")

while True:
    ques = input("You: ")

    # Check if the input is a greeting
    greetings = ["hi", "hello", "hey", "hi there", "hello there"]
    if any(greeting in ques.lower() for greeting in greetings):
        print("Bot: Hello! How can I help you?")
        continue

    response = openai.Completion.create(
        prompt=ques,
        model="gpt-3.5-turbo-instruct",
        max_tokens=150,
    )

    print("Bot:", response.choices[0].text.strip(), "\n")

    further_question = input("Do you have any further questions? (Y/N): ").capitalize()
    while further_question not in {"Y", "N"}:
        print("Please enter 'Y' for Yes or 'N' for No.")
        further_question = input(
            "Do you have any further questions? (Y/N): "
        ).capitalize()

    if further_question == "Y":
        print("How can I assist you further?\n")
        continue
    else:
        print("Thank you for using our service. Goodbye!")
        break
