from ai import AI

brain = AI()

mode = "discussion"

while True:

    user = input(f"You [{mode}]: ")

    if user.lower() == "quit":
        break

    if user.lower() == "teaching":
        mode = "teaching"
        print("PG26: Teaching Mode activated.")
        continue
        
    if user.lower() == "discussion":
        mode = "discussion"
        print("PG26: Discussion Mode activated.")
        continue
        
    answer = brain.process(user, mode)

    print("PG26: " + answer)