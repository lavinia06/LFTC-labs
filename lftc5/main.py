from FA import FiniteAutomaton

def custom_menu(automaton):
    while True:
        user_input = input("Select an option (0-7): ")
        if user_input == "1":
            print("States: ", automaton.states_set)
        elif user_input == "2":
            print("Alphabet: ", automaton.input_alphabet)
        elif user_input == "3":
            print("Transitions: ", automaton.transitions)
        elif user_input == "4":
            print("Initial state: ", automaton.start_state)
        elif user_input == "5":
            print("Final states: ", automaton.accept_states)
        elif user_input == "6":
            print(automaton)
        elif user_input == "7":
            print("Sequence check result: ", check_sequence(automaton))
        elif user_input == "0":
            break
        else:
            print("Invalid option!")

def check_sequence(automaton):
    user_input = input("Enter a sequence (comma-separated): ").strip().replace(" ", "").split(",")
    return automaton.check_sequence(user_input)

def print_custom_menu():
    print("1. Print the set of states\n"
          "2. Print the alphabet\n"
          "3. Print the transition functions\n"
          "4. Print the initial state\n"
          "5. Print the set of final states\n"
          "6. Print everything\n"
          "7. Check a sequence\n"
          "0. Exit\n\n")

if __name__ == "__main__":
    my_fa = FiniteAutomaton("fa.in")
    print_custom_menu()
    custom_menu(my_fa)
    print(f"My finite automaton is deterministic: {my_fa.is_deterministic()}")
