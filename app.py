from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["todoDB"]
collection = db["tasks"]

# Home route: Display tasks
@app.route("/")
def home():
    tasks = list(collection.find())
    for task in tasks:
        task["_id"] = str(task["_id"])  # Convert ObjectId to string for template rendering
    return render_template("index.html", tasks=tasks)

# Add a new task
@app.route("/add", methods=["POST"])
def add_task():
    task_content = request.form.get("task")
    if task_content:
        collection.insert_one({"task": task_content, "completed": False})
    return redirect("/")

# Update task status
@app.route("/update/<task_id>")
def update_task(task_id):
    collection.update_one({"_id": ObjectId(task_id)}, {"$set": {"completed": True}})
    return redirect("/")

# Delete a task
@app.route("/delete/<task_id>")
def delete_task(task_id):
    collection.delete_one({"_id": ObjectId(task_id)})
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
