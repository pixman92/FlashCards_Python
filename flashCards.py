# -n, --newdeck <deck_name>     Create a new deck with the specified name
# -o, --output <deck_name>      Output the current deck as a JSON file with the specified name
# -i, --import <deck_file>      Import a deck from the specified JSON file
# -e, --edit                    Enter edit mode to modify the current deck
# -s, --study                   Enter study mode to review the current deck
# -r, --randomize               Enable randomized questions in study mode


# ======================
import argparse
import json
import os
import readline
import glob
import random


class FlashCard:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        self.correct = False


class FlashCardDeck:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def delete_card(self, index):
        if index >= 0 and index < len(self.cards):
            del self.cards[index]

    def get_random_card(self):
        unanswered_cards = [card for card in self.cards if not card.correct]
        if unanswered_cards:
            return random.choice(unanswered_cards)
        return None

    def mark_card_correct(self, card):
        card.correct = True


def create_deck(name):
    return FlashCardDeck(name)


def create_card(deck, question, answer):
    card = FlashCard(question, answer)
    deck.add_card(card)
    save_deck(deck)


def delete_card(deck, index):
    deck.delete_card(index)
    save_deck(deck)


def list_cards(deck):
    print("Deck:", deck.name)
    print()
    for i, card in enumerate(deck.cards):
        print("Index:", i)
        print("Question:", card.question)
        print("Answer:", card.answer)
        print()


def save_deck(deck):
    filename = deck.name + ".dck"
    with open(filename, "w") as file:
        data = {
            "name": deck.name,
            "cards": [
                {"question": card.question, "answer": card.answer, "correct": card.correct}
                for card in deck.cards
            ],
        }
        json.dump(data, file)


def load_deck(filename):
    with open(filename, "r") as file:
        data = json.load(file)
        deck = FlashCardDeck(data["name"])
        for card_data in data["cards"]:
            card = FlashCard(card_data["question"], card_data["answer"])
            card.correct = card_data["correct"]
            deck.add_card(card)
        return deck


def complete_filename(text, state):
    path = os.path.expanduser(text) + "*"
    return (glob.glob(path) + [None])[state]


def study_mode(deck, randomize=False):
    cards = deck.cards[:]
    if randomize:
        random.shuffle(cards)

    for card in cards:
        print("\n\nQuestion:", card.question)
        input("Press Enter to show the answer.")
        print("Answer:", card.answer)
        correct = input("(y/n): ").lower()
        if correct == "y":
            deck.mark_card_correct(card)
    save_deck(deck)


def edit_mode(deck):
    while True:
        print("Deck:", deck.name)
        print("Options:")
        print("1. Create a card")
        print("2. Delete a card")
        print("3. List all cards")
        print("4. Quit")

        choice = input("Enter your choice (1-4): ")
        if choice == "1":
            question = input("Enter the question: ")
            answer = input("Enter the answer: ")
            create_card(deck, question, answer)
            print("Card created.")
        elif choice == "2":
            list_cards(deck)
            index = input("Enter the index of the card to delete: ")
            try:
                index = int(index)
                delete_card(deck, index)
                print("Card deleted.")
            except ValueError:
                print("Invalid index.")
        elif choice == "3":
            list_cards(deck)
        elif choice == "4":
            break
        else:
            print("Invalid choice.")


def main():
    parser = argparse.ArgumentParser(description="Flash Card Script")
    parser.add_argument("-n", "--new", metavar="DECK_NAME", help="Create a new deck and save as a .dck file")
    parser.add_argument("-o", "--output", metavar="FILENAME", help="Output deck file in JSON format")
    parser.add_argument("-i", "--import_deck", metavar="FILENAME", help="Import a deck from a .dck file")
    parser.add_argument("-e", "--edit", action="store_true", help="Enter edit mode")
    parser.add_argument("-s", "--study", action="store_true", help="Enter study mode")
    parser.add_argument("-r", "--random", action="store_true", help="Randomize questions asked")

    args = parser.parse_args()

    if args.new:
        deck_name = args.new
        deck = create_deck(deck_name)
        save_deck(deck)
        print("Deck '{}' created and saved.".format(deck_name))
    elif args.output:
        deck_filename = args.output
        if os.path.exists(deck_filename):
            print("Error: File already exists.")
        else:
            deck = load_deck(deck_filename)
            save_deck(deck)
            print("Deck '{}' saved as {}.".format(deck.name, deck_filename))
    elif args.import_deck:
        deck_filename = args.import_deck
        if not os.path.exists(deck_filename):
            print("Error: File not found.")
        else:
            deck = load_deck(deck_filename)
            print("Deck '{}' imported.".format(deck.name))
            if args.edit:
                edit_mode(deck)
            elif args.study:
                study_mode(deck, randomize=args.random)
            else:
                print("No mode specified.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
