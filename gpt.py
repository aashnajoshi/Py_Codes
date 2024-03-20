#openai==0.28
import openai
import pytz
import datetime
import geoip2.database

# Set up GeoIP2 reader
geo_reader = geoip2.database.Reader('GeoLite2-City.mmdb')

api_key = "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"
openai.api_key = api_key

print("Welcome! How can I assist you today?\n")

def get_local_time(timezone):
    now = datetime.datetime.now(pytz.timezone(timezone))
    return now.strftime('%I:%M %p')

while True:
    ques = input("You: ")

    # Check if the input is a greeting
    greetings = ["hi", "hello", "hey", "hi there", "hello there"]
    if any(greeting in ques.lower() for greeting in greetings):
        print("Bot: Hello! How can I help you?")
        continue

    # Check if the input is about time
    if "time" in ques.lower():
        # Check if the user asked for time in a specific location
        if "in" in ques.lower():
            location = ques.split("in")[-1].strip()
            try:
                response = geo_reader.city("8.8.8.8")  # Dummy IP, replace with actual user IP
                timezone = response.location.time_zone
                local_time = get_local_time(timezone)
                print(f"Bot: The current time in {location} is {local_time}.")
            except geoip2.errors.AddressNotFoundError:
                print("Bot: Sorry, I couldn't determine the location.")
            continue
        else:
            local_time = datetime.datetime.now().strftime('%I:%M %p')
            print(f"Bot: It is currently {local_time}.")
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
