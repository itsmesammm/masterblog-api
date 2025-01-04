from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    # Validate info for new post
    if not data or 'title' not in data or 'content' not in data:
        missing = [field for field in ['title', 'content'] if field not in data]
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    # Generate new ID for new post
    new_id = max(post["id"] for post in POSTS) + 1 if POSTS else 1

    # Create new post
    new_post = {
        "id":new_id,
        "title": data["title"],
        "content": data["content"]
    }
    POSTS.append(new_post)
    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete(post_id):
    # Find the post by ID
    post = next((post for post in POSTS if post['id'] == post_id), None)

    if not post:
        return jsonify({"error": f"Post with id {post_id} not found"}), 404

    # Remove post from thr list
    POSTS.remove(post)

    # Returns success message
    return jsonify({"message": f"Post with id: {post_id}, successfully deleted."}), 200


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update(post_id):
    # Find the post by id
    post = next((post for post in POSTS if post['id'] == post_id), None)

    if not post:
        return jsonify({"error": f"Post with id {post_id} not found"}), 404

    # Get the request data
    data = request.get_json()

    # Update the fields
    if data.get('title'):
        post["title"] = data["title"]
    if data.get('content'):
        post["content"] = data["content"]

    return jsonify(post), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
