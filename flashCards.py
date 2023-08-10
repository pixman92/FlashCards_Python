import os
import readline

# Set the completion function for tab completion
def complete(text, state):
    options = [name for name in os.listdir(".") if name.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None

def complete_decks(text, state):
    options = [name for name in os.listdir(".") if name.startswith(text)]
    if state < len(options):
        return options[state] + " "
    else:
        return None

# Enable tab completion
readline.parse_and_bind("bind ^I rl_complete")
readline.set_completer_delims("")
readline.set_completer(complete)

def get_deck_name(prompt):
    try:
        readline.set_completer(complete_decks)
        return raw_input(prompt)
    except (KeyboardInterrupt, EOFError):
        return None

def save_deck(deck, deck_name):
    # Save the deck to a .dck file
    deck_filename = deck_name + '.dck'
    with open(deck_filename, 'w') as file:
        for card in deck:
            answer = card[0]
            question = card[1]
            file.write("[[" + answer + "],[" + question + "]]\n")

def load_deck(deck_name):
    deck_filename = deck_name + '.dck'
    try:
        # Load the deck from the .dck file
        with open(deck_filename, 'r') as file:
            deck = []
            for line in file:
                line = line.strip()
                if line:
                    # Extract the answer and question
                    parts = line.split('],[')
                    answer = parts[0][2:]
                    question = parts[1][:-2]

                    card = [answer, question]
                    deck.append(card)
            return deck
    except IOError:
        print("Error: Deck file not found or cannot be opened.")
        return []

def add_cards():
    deck_name = get_deck_name("Enter the name of the deck: ")
    if deck_name is None:
        return

    deck = load_deck(deck_name)

    if not deck:
        print("Deck not found. Creating new deck: " + deck_name)
        deck = []

    while True:
        question = raw_input("Enter the question (or leave blank to exit): ")
        if not question:
            break

        answer = raw_input("Enter the answer (or leave blank to exit): ")
        if not answer:
            break

        card = [answer, question]
        deck.append(card)

    save_deck(deck, deck_name)

def edit_cards():
    deck_name = get_deck_name("Enter the name of the deck to edit: ")
    if deck_name is None:
        return

    deck = load_deck(deck_name)

    if not deck:
        print("Deck not found.")
        return

    print("Editing deck: " + deck_name)
    for i, card in enumerate(deck):
        print("Card " + str(i + 1) + ":")
        question = raw_input("Enter the new question: ")
        answer = raw_input("Enter the new answer: ")
        card[0] = answer
        card[1] = question

    save_deck(deck, deck_name)

def delete_card():
    deck_name = get_deck_name("Enter the name of the deck to delete a card from: ")
    if deck_name is None:
        return

    deck = load_deck(deck_name)

    if not deck:
        print("Deck not found.")
        return

    print("Deck: " + deck_name)
    for i, card in enumerate(deck):
        print("Card " + str(i + 1) + ": " + card[1])

    card_index = raw_input("Enter the index of the card to delete: ")
    try:
        card_index = int(card_index)
        if card_index < 1 or card_index > len(deck):
            print("Invalid card index.")
        else:
            del deck[card_index - 1]
            save_deck(deck, deck_name)
            print("Card deleted.")
    except ValueError:
        print("Invalid card index.")

def study_cards():
    deck_name = get_deck_name("Enter the name of the deck to study: ")
    if deck_name is None:
        return

    deck = load_deck(deck_name)

    if not deck:
        print("Deck not found.")
        return

    print("Studying deck: " + deck_name)
    cards = deck[:]

    while cards:
        for card in cards:
            print("\nQuestion:\n" + card[1])
            raw_input("Press Enter to see the answer.")
            print("\nAnswer: " + card[0])

            correct = raw_input("Did you answer correctly? (y/n): ")
            if correct.lower() == 'y':
                card.append('understood')

        # Filter out the understood cards
        cards = [card for card in cards if len(card) < 3]

        if not cards:
            print("Congratulations! You have understood all the cards.")
        else:
            reset = raw_input("Enter 'reset' to start over, 'end' to exit, or press Enter to continue: ")
            if reset.lower() == 'reset':
                for card in deck:
                    card.pop(2, None)  # Remove 'understood' tag
                cards = deck[:]
            elif reset.lower() == 'end':
                return

    save_deck(deck, deck_name)

def reset_cards():
    deck_name = get_deck_name("Enter the name of the deck to reset: ")
    if deck_name is None:
        return

    deck = load_deck(deck_name)

    if not deck:
        print("Deck not found.")
        return

    for card in deck:
        card.pop(2, None)  # Remove 'understood' tag
    save_deck(deck, deck_name)
    print("Deck has been reset.")

def main():
    while True:
        print("\n--- Flashcards ---")
        print("1. Add Cards")
        print("2. Edit Cards")
        print("3. Delete Card")
        print("4. Study Cards")
        print("5. Reset Cards")
        print("6. Quit")

        choice = raw_input("Enter your choice (1-6): ")

        if choice == '1':
            add_cards()
        elif choice == '2':
            edit_cards()
        elif choice == '3':
            delete_card()
        elif choice == '4':
            study_cards()
        elif choice == '5':
            reset_cards()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
