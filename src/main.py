import sys

if __name__ == "__main__":
    user_input = len(sys.argv)

    if user_input == 1:
        while True:
            try:
                get_input = input()
                print("Scanner Not Implemented")
            except KeyboardInterrupt:
                break

    if user_input == 2:
        file = sys.argv[1]
        with open(file, "r") as f:
            get_input = f.read()

        print(get_input)
        print("Scanner Not Implemented")

    if user_input > 2:
        print("Error: Only at most 2 arguments are allowed")





