from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

tasks = [
    {"id": 1, "title": "Learn Docker", "completed": True},
    {"id": 2, "title": "Learn Kubernetes", "completed": False},
    {"id": 3, "title": "Build Jenkins Pipeline", "completed": False},
]


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)


@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    if not data or not data.get("title"):
        return jsonify({"error": "Task title is required"}), 400

    new_task = {
        "id": max([task["id"] for task in tasks], default=0) + 1,
        "title": data["title"],
        "completed": False,
    }

    tasks.append(new_task)

    return jsonify(new_task), 201


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()

    if "completed" in data:
        task["completed"] = data["completed"]

    if "title" in data:
        task["title"] = data["title"]

    return jsonify(task)


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks

    task = next((task for task in tasks if task["id"] == task_id), None)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    tasks = [task for task in tasks if task["id"] != task_id]

    return jsonify({"message": "Task deleted"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
