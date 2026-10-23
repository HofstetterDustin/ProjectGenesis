from ai import AI

brain = AI()

while True:

    user = input("You: ")

    if user.lower() == "quit":
        break

    answer = brain.process(user)

    print("PG26:\n" + answer)