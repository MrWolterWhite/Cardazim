from flask import Flask, jsonify, request
import json
from card_manager import CardManager
from card import Card
import os
import copy
from server import run_server
app = Flask(__name__)

@app.route("/")
def greet():
    return "Welcome to my Cardazim!"

@app.route("/secret_message")
def greet_secret():
    return "Welcome to my Cardazim's secret message!"

@app.route("/creators")
def get_creators():
    manager = CardManager("sql://cards", os.path.join("sql://cards".split("//")[1],"images"))
    return jsonify(manager.driver.GetCreators())
    #return "Welcome to my Cardazim!"

@app.route("/creators/<string:creator>/cards")
def get_creator_cards(creator):
    manager = CardManager("sql://cards", os.path.join("sql://cards".split("//")[1],"images"))
    cards = manager.driver.GetCreatorCards(creator)
    return jsonify([{'creator': card.creator, 'name': card.name, 'riddle': card.riddle, "solution": card.solution, "image_path": os.path.join(manager.driver.image_url,card.generate_identifier(), "image.png")} for card in cards])

@app.route("/creators/<string:creator>/cards/<string:card_name>")
def get_creator_card(creator, card_name):
    manager = CardManager("sql://cards", os.path.join("sql://cards".split("//")[1],"images"))
    card = manager.driver.GetCreatorCard(creator, card_name)
    return jsonify({'creator': card.creator, 'name': card.name, 'riddle': card.riddle, "solution": card.solution, "image_path": os.path.join(manager.driver.image_url,card.generate_identifier(), "image.png")})

@app.route("/creators/<string:creator>/cards/<string:card_name>/image.png")
def get_creator_card_image(creator, card_name):
    manager = CardManager("sql://cards", os.path.join("sql://cards".split("//")[1],"images"))
    card = manager.driver.GetCreatorCard(creator, card_name)
    return jsonify(os.path.join(manager.driver.image_url,card.generate_identifier(), "image.png"))

@app.route("/creators/<string:creator>/cards/solved")
def get_creator_solved_cards(creator):
    manager = CardManager("sql://cards", os.path.join("sql://cards".split("//")[1],"images"))
    
    cards = manager.driver.GetCreatorSolvedCards(creator)
    return jsonify([{'creator': card.creator, 'name': card.name, 'riddle': card.riddle, "solution": card.solution, "image_path": os.path.join(manager.driver.image_url,card.generate_identifier(), "image.png")} for card in cards])

@app.route("/creators/<string:creator>/cards/unsolved")
def get_creator_unsolved_cards(creator):
    manager = CardManager("sql://cards", os.path.join("sql://cards".split("//")[1],"images"))
    cards = manager.driver.GetCreatorUnsolvedCards(creator)
    return jsonify([{'creator': card.creator, 'name': card.name, 'riddle': card.riddle, "solution": card.solution, "image_path": os.path.join(manager.driver.image_url,card.generate_identifier(), "image.png")} for card in cards])

@app.route("/cards/<string:card_id>/solve", methods=['GET','POST'])
def solve_card(card_id):
    solution = request.args.get('sol')
    manager = CardManager("sql://cards", os.path.join("sql://cards".split("//")[1],"images"))
    (creator, name) = Card.generate_creator_name_from_identifier(card_id)
    card = manager.driver.GetCreatorCard(creator, name)
    if card.solution is not None:
        return "Card Already Solved!"
    if card.image.decrypt(solution):
        prev_card = copy.deepcopy(card)
        card.solution = solution
        manager.driver.replace(prev_card, card)
        return "Solved!"
    else:
        return "Wrong Solution :("

@app.route("/cards/find")
def get_cards_by_filter():
    name_filter = request.args.get('name', default= '', type = str)
    creator_filter = request.args.get('creator', default= '', type = str)
    riddle_filter = request.args.get('riddle', default= '', type = str)
    solution_filter = request.args.get('sol', default= '', type = str)
    manager = CardManager("sql://cards", os.path.join("sql://cards".split("//")[1],"images"))
    cards = manager.driver.GetFilteredCards(creator_filter, name_filter, riddle_filter, solution_filter)
    return jsonify([{'creator': card.creator, 'name': card.name, 'riddle': card.riddle, "solution": card.solution, "image_path": os.path.join(manager.driver.image_url,card.generate_identifier(), "image.png")} for card in cards])


def run_api_server(host, port):
    app.run(host=host, port=port)
    run_server(host,port, "sql://cards")

if __name__ == "__main__":
    run_api_server("127.0.0.1", "8080")