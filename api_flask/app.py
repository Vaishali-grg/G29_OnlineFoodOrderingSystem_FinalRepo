from flask import Flask, jsonify, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# In-memory database for demonstration
recipes_db = [
    {"id": 1, "title": "Pasta Carbonara", "ingredients": ["pasta", "eggs", "bacon", "cheese"], "instructions": "Cook pasta, mix with eggs and bacon, add cheese."},
    {"id": 2, "title": "Chicken Curry", "ingredients": ["chicken", "curry paste", "coconut milk"], "instructions": "Cook chicken, add curry paste and coconut milk, simmer."}
]

# Helper function to get the next ID
def get_next_id():
    return max(recipe['id'] for recipe in recipes_db) + 1 if recipes_db else 1

# API Routes
@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    return jsonify(recipes_db)

@app.route('/api/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = next((r for r in recipes_db if r['id'] == recipe_id), None)
    if recipe is None:
        abort(404)
    return jsonify(recipe)

@app.route('/api/recipes', methods=['POST'])
def create_recipe():
    if not request.json or 'title' not in request.json:
        abort(400)
    
    new_recipe = {
        'id': get_next_id(),
        'title': request.json['title'],
        'ingredients': request.json.get('ingredients', []),
        'instructions': request.json.get('instructions', '')
    }
    recipes_db.append(new_recipe)
    return jsonify(new_recipe), 201

@app.route('/api/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    recipe = next((r for r in recipes_db if r['id'] == recipe_id), None)
    if recipe is None:
        abort(404)
    if not request.json:
        abort(400)
    
    recipe['title'] = request.json.get('title', recipe['title'])
    recipe['ingredients'] = request.json.get('ingredients', recipe['ingredients'])
    recipe['instructions'] = request.json.get('instructions', recipe['instructions'])
    return jsonify(recipe)

@app.route('/api/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    global recipes_db
    recipe = next((r for r in recipes_db if r['id'] == recipe_id), None)
    if recipe is None:
        abort(404)
    recipes_db = [r for r in recipes_db if r['id'] != recipe_id]
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True, port=5000)