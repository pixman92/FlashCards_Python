import argparse
import json
import os
import random
import sys

DECK_EXTENSION = ".dck"

def create_deck(deck_name):
    deck = {"cards": []}
    save_deck(deck, deck_name)

def save_deck(deck, deck_name):
    deck_file = deck_name + DECK_EXTENSION
    with open(deck_file, "w") as file:
        json.dump(deck, file)

def load_deck(deck_name):
    deck_file = deck_name + DECK_EXTENSION
    if not os.path.isfile(deck_file):
        print("Deck file not found.")
        return None
    with open(deck_file, "r") as file:
        deck = json.load(file)
    return deck

def list_cards(deck):
    for i, card in enumerate(deck["cards"]):
        print("Index:", i)
        print("Question:", card["question"])
        print("Answer:", card["answer"])
        print()

def create_card(deck, question, answer):
    card = {"question": question, "answer": answer}
    deck["cards"].append(card)
    save_deck(deck, deck_name)

def delete_card(deck, index):
    if index >= 0 and index < len(deck["cards"]):
        deck["cards"].pop(index)
        save_deck(deck, deck_name)
        print("Card deleted.")
    else:
        print("Invalid card index.")

def study_deck(deck, randomize):
    cards = deck["cards"]
    if randomize:
        random.shuffle(cards)

    for card in cards:
        print("Question:", card["question"])
        input("Press Enter to reveal the answer...")
        print("Answer:", card["answer"])
        correct = input("Did you get the answer correct? (y/n): ")
        if correct.lower() == "y":
            deck["cards"].remove(card)
            save_deck(deck, deck_name)
            print("Card removed from the deck.")
        print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flash Card Script")

    # Create a new deck
    parser.add_argument("-n", "--new", metavar="deck_name", help="Create a new deck")

    # Output a deck file
    parser.add_argument("-o", "--output", metavar="deck_name", help="Output a deck file")

    # Edit a deck
    parser.add_argument("-e", "--importDeck", metavar="deck_file", help="Edit a deck")

    # Study a deck
    parser.add_argument("-s", "--study", metavar="deck_file", help="Study a deck")

    # Randomize questions
    parser.add_argument("-r", "--randomize", action="store_true", help="Randomize the order of cards")

    args = parser.parse_args()

    if args.new:
        create_deck(args.new)
    elif args.output:
        deck = load_deck(args.output)
        if deck:
            print(json.dumps(deck))
    elif args.importDeck:
        deck_name = os.path.splitext(args.importDeck)[0]
        deck = load_deck(deck_name)
        if deck:
            while True:
                print("Options:")
                print("1. Create a new card")
                print("2. Delete a card")
                print("3. List all cards")
                print("4. Exit")
                option = input("Enter an option (1-4): ")
                if option == "1":
                    question = input("Enter the question: ")
                    answer = input("Enter the answer: ")
                    create_card(deck, question, answer)
                elif option == "2":
                    index = int(input("Enter the index of the card to delete: "))
                    delete_card(deck, index)
                elif option == "3":
                    list_cards(deck)
                elif option == "4":
                    break
                else:
                    print("Invalid option.")
    elif args.study:
        deck_name = os.path.splitext(args.study)[0]
        deck = load_deck(deck_name)
        if deck:
            study_deck(deck, args.randomize)
