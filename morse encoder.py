def convert_to_morse(code):
    morse_code = {'1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
                  '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----'}
    return ' '.join(morse_code[char] for char in code if char in morse_code)

def convert_from_morse(code):
    morse_code = {'.----': '1', '..---': '2', '...--': '3', '....-': '4', '.....': '5',
                  '-....': '6', '--...': '7', '---..': '8', '----.': '9', '-----': '0'}
    return ''.join(morse_code[word] for word in code.split() if word in morse_code)

def main():
    print("Welcome to Morse Code Converter!")
    while True:
        print("\nMENU:\n1. Encode to Morse Code\n2. Decode from Morse Code\n3. Exit")
        choice = input("Enter your choice (1/2/3): ")
        if choice == '1':
            print(f"Morse Code: {convert_to_morse(input('Enter numbers to be converted (with spaces in between): '))}")
        elif choice == '2':
            print(f"Decoded: {convert_from_morse(input('Enter Morse Code to be decoded (separate letters with spaces): '))}")
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option (1/2/3).")

if __name__ == "__main__":
    main()