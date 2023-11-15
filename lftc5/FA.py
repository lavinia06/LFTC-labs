class FiniteAutomaton:
    def __init__(self, file_path):
        self.states_set = []
        self.input_alphabet = []
        self.transitions = {}
        self.start_state = ""
        self.accept_states = []
        self.load_from_file(file_path)

    def load_from_file(self, file_path):
        with open(file_path) as file:
            self.states_set = [state.strip() for state in file.readline().strip('{} \n').split(",")]
            if len(self.states_set) == 0:
                raise RuntimeError("Error while parsing states")

            self.input_alphabet = [symbol.strip() for symbol in file.readline().strip('{} \n').split(",")]
            if len(self.input_alphabet) == 0:
                raise RuntimeError("Error while parsing alphabet")

            self.start_state = file.readline().strip()
            if len(self.start_state) == 0:
                raise RuntimeError("Error while parsing start state")

            self.accept_states = [state.strip() for state in file.readline().strip('{}').split(",")]
            if len(self.accept_states) == 0:
                raise RuntimeError("Error while parsing accept states")

            for line in file:
                parts = line.strip('{}').replace(" ", "").split("=")
                pair = parts[0].strip().split(",")
                if len(pair) != 2 or len(parts) == 0:
                    raise RuntimeError("Error while parsing transition functions")
                transition_result = parts[1].strip('\n')  # Remove newline character
                self.transitions.setdefault((pair[0], pair[1]), []).append(transition_result)

    def is_deterministic(self):
        visited = set()  # Keep track of visited state-symbol pairs
        for (state, symbol), next_states in self.transitions.items():
            key = (state, symbol)
            if key in visited or len(next_states) != 1:
                return False
            visited.add(key)
        return True

    def check_sequence(self, sequence):
        if self.is_deterministic():
            current_state = self.start_state
            for symbol in sequence:
                if (current_state, str(symbol)) not in self.transitions.keys():
                    return False
                current_state = self.transitions[(current_state, str(symbol))][0]
            return current_state in self.accept_states
        return False

    def __repr__(self):
        return " States: " + str(self.states_set) + "\n Alphabet: " + str(
            self.input_alphabet) + "\n Transitions: " + str(
            self.transitions) + "\n Start state: " + self.start_state + "\n Accept states: " + str(self.accept_states)
