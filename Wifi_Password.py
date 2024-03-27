import subprocess

print("List of all the Saved Networks: \n")
try:
    # Retrieve Wi-Fi profiles
    data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
    profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]

    # Print Wi-Fi profiles and passwords (if available)
    for profile in profiles:
        try:
            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']).decode('utf-8').split('\n')
            password = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
            print("{:<30}|  {:<}".format(profile, password[0] if password else ""))
        except (subprocess.CalledProcessError, IndexError):
            print("{:<30}|  {:<}".format(profile, "Error retrieving password"))
    input("Press Enter to exit...")
except Exception as e:
    print(f"An error occurred: {e}")
    input("Press Enter to exit...")