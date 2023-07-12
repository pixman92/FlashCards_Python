import pickle

def save_decks(decks):
    with open('flashcards.dck', 'wb') as file:
        pickle.dump(decks, file)

def load_decks():
    try:
        with open('flashcards.dck', 'rb') as file:
            return pickle.load(file)
    except IOError:
        return []

def add_cards(decks):
    deck_name = raw_input("Enter the name of the deck: ")
    deck = [deck_name, []]

    while True:
        question = raw_input("Enter the question (or leave blank to exit): ")
        if not question:
            break

        answer = raw_input("Enter the answer (or leave blank to exit): ")
        if not answer:
            break

        card = [question, answer]
        deck[1].append(card)

    decks.append(deck)
    save_decks(decks)

def edit_cards(decks):
    deck_name = raw_input("Enter the name of the deck to edit: ")
    for deck in decks:
        if deck[0] == deck_name:
            print("Editing deck: " + deck_name)
            for i, card in enumerate(deck[1]):
                print("Card " + str(i + 1) + ":")
                question = raw_input("Enter the new question: ")
                answer = raw_input("Enter the new answer: ")
                card[0] = question
                card[1] = answer
            save_decks(decks)
            return

    print("Deck not found.")

def delete_cards(decks):
    deck_name = raw_input("Enter the name of the deck to delete: ")
    for deck in decks:
        if deck[0] == deck_name:
            decks.remove(deck)
            save_decks(decks)
            print("Deck deleted: " + deck_name)
            return

    print("Deck not found.")

def study_cards(decks):
    deck_name = raw_input("Enter the name of the deck to study: ")
    for deck in decks:
        if deck[0] == deck_name:
            print("Studying deck: " + deck_name)
            cards = deck[1]
            understood_cards = []

            while cards:
                for card in cards:
                    print("Question: " + card[0])
                    raw_input("Press Enter to see the answer.")
                    print("Answer: " + card[1])

                    correct = raw_input("Did you answer correctly? (y/n): ")
                    if correct.lower() == 'y':
                        understood_cards.append(card)

                cards = [card for card in cards if card not in understood_cards]
                if not cards:
                    print("Congratulations! You have understood all the cards.")
                else:
                    reset = raw_input("Enter 'reset' to start over, or press Enter to continue: ")
                    if reset.lower() == 'reset':
                        cards = deck[1]
                        understood_cards = []
            return

    print("Deck not found.")

def reset_cards(decks):
    for deck in decks:
        for card in deck[1]:
            if 'understood' in card:
                del card['understood']
    save_decks(decks)
    print("All decks have been reset.")

def main():
    decks = load_decks()

    while True:
        print("\n--- Flashcards ---")
        print("1. Add Cards")
        print("2. Edit Cards")
        print("3. Delete Cards")
        print("4. Study Cards")
        print("5. Reset Cards")
        print("6. Quit")

        choice = raw_input("Enter your choice (1-6): ")

        if choice == '1':
            add_cards(decks)
        elif choice == '2':
            edit_cards(decks)
        elif choice == '3':
            delete_cards(decks)
        elif choice == '4':
            study_cards(decks)
        elif choice == '5':
            reset_cards(decks)
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
