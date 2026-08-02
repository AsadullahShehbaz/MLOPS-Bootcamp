from flask import Flask , jsonify , request 

app = Flask(__name__)

# Sample Database
items = [
    {"id":1,"name":"item1","description":"This is item1"},
    {"id":2,"name":"item2","description":"This is item2"},
]

@app.route("/")
def home():
    return "This is home page"

# Get all items 
@app.route("/items")
def get_items():
    return jsonify(items)

# Get a specific item by id 
@app.route("/items/<int:item_id>")
def get_specific_items(item_id):

    item = next((item for item in items if item["id"] == item_id),None)
    if item is None:
        return jsonify({"error":"Item not found"})
    return jsonify(item)

# Create a new item 
@app.route("/items",methods=["POST"])
def create_items():
    if not request.json or "name" not in request.json:
        return jsonify({"error":"Item is invalid"})
    new_item = {
        "id": items[-1]["id"] + 1 if items else 1,
        "name": request.json["name"],
        "description":request.json["description"]
    }
    items.append(new_item)
    return jsonify(new_item)

# Update an existing item
@app.route("/items/<int:item_id>",methods=["PUT"])
def update_item(item_id):
    item = next((item for item in items if item["id"] == item_id),None)
    if item is None:
        return jsonify({"error":"Item not found"})
    item["name"]=request.json.get("name",item["name"]),
    item["description"]=request.json.get("description",item["description"])

    return jsonify(item)

# delete an item 
@app.route("/items/<int:item_id>",methods=["DELETE"])
def delete_item(item_id):
    global items 
    items = next((item for item in items if item["id"] != item_id),None)

    return jsonify({"result":"Item deleted"})

app.run(debug=True)