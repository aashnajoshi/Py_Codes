def convert_to_morse(code):

    code = code.replace("1", ".----")
    code = code.replace("2", "..---")
    code = code.replace("3", "...--")
    code = code.replace("4", "....-")
    code = code.replace("5", ".....")
    code = code.replace("6", "-....")
    code = code.replace("7", "--...")
    code = code.replace("8", "---..")
    code = code.replace("9", "---.")
    code = code.replace("0", "----")

    return code

lock_code = int(input("Enter numbers to be converted (with space on between)"))
print(f"Initial code:", lock_code)

morse = convert_to_morse(lock_code)
print(f"Morse Code: {morse}")
