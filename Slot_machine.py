import random

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {"A": 2, "B": 4, "C": 6, "D": 8}
symbol_value = {"A": 5, "B": 4, "C": 3, "D": 2}

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        if all(column[line] == columns[0][line] for column in columns):
            winnings += values[columns[0][line]] * bet
            winning_lines.append(line + 1)
    return winnings, winning_lines

def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = [symbol for symbol, count in symbols.items() for _ in range(count)]
    return [[random.choice(all_symbols) for _ in range(rows)] for _ in range(cols)]

def print_slot_machine(columns):
    for row in zip(*columns):
        print(" | ".join(row))

def get_input(prompt, check_func):
    while True:
        user_input = input(prompt)
        if check_func(user_input):
            return user_input

def deposit():
    return int(get_input("What would you like to deposit? $", lambda x: x.isdigit() and int(x) > 0))

def get_number_of_lines():
    return int(get_input(f"Enter the number of lines to bet on (1-{MAX_LINES})? ", lambda x: x.isdigit() and 1 <= int(x) <= MAX_LINES))

def get_bet():
    return int(get_input(f"What would you like to bet on each line? (${MIN_BET}-${MAX_BET}) $", lambda x: x.isdigit() and MIN_BET <= int(x) <= MAX_BET))

def spin(balance):
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines
        if total_bet > balance:
            print(f"You do not have enough to bet that amount, your current balance is: ${balance}")
        else:
            break

    print(f"You are betting ${bet} on {lines} lines. Total bet is equal to: ${total_bet}")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won ${winnings}.")
    print(f"You won on lines:", *winning_lines)
    return winnings - total_bet

def main():
    balance = deposit()
    while True:
        print(f"Current balance is ${balance}")
        answer = input("Press enter to play (q to quit).")
        if answer == "q":
            break
        balance += spin(balance)
    print(f"You left with ${balance}")

if __name__ == "__main__":
    main()