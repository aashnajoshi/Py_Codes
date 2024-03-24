import requests
import random
import html

def fetch_random_question():
    url = "https://opentdb.com/api.php?amount=1&type=multiple&category=9&difficulty=medium"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['response_code'] == 0:
            question_data = data['results'][0]
            question = html.unescape(question_data['question'])
            correct_answer = html.unescape(question_data['correct_answer'])
            incorrect_answers = [html.unescape(ans) for ans in question_data['incorrect_answers']]
            return question, correct_answer, incorrect_answers

def check_guess(guess, correct_answer):
    return guess.lower() == correct_answer.lower()

def main():
    score = 0
    total_questions = 10  # Set total no. of Ques
    print("Welcome to the Quiz Game!")
    for i in range(1, total_questions + 1):
        print(f"\nQuestion {i}/{total_questions}:")
        question, correct_answer, incorrect_answers = fetch_random_question()
        answers = [correct_answer] + incorrect_answers
        random.shuffle(answers)
        print(question)
        for j, answer in enumerate(answers, start=1):
            print(f"{j}. {answer}")
        guess = input("Your answer (enter the number): ")
        if guess.isdigit() and 1 <= int(guess) <= len(answers):
            if check_guess(answers[int(guess) - 1], correct_answer):
                print("Correct Answer!")
                score += 1
            else:
                print("Wrong Answer! The correct answer is:", correct_answer)
        else:
            print("Invalid input. Skipping this question.")
        print(f"Your current score is: {score}/{i}")
    print("Quiz completed!")
    print(f"Your final score is: {score}/{total_questions}")

if __name__ == "__main__":
    main()