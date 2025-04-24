from flask import Flask, request, jsonify
from utils import generate_answer

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query():
    try:
        # Get the user query from the request body
        user_query = request.json.get('query')
        if not user_query:
            return jsonify({"error": "Query is required"}), 400
        
        # For now, use placeholder content for concatenated articles (this would come from scraping)
        concatenated_content = "This is the content you fetched from articles."

        # Generate the answer using the updated function
        answer = generate_answer(concatenated_content, user_query)
        
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='localhost', port=5001)
