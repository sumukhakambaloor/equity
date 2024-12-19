from flask import Flask, request, jsonify
import requests
from flask_cors import CORS  # Import the CORS module

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Updated Gemini API URL and Key
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
GEMINI_API_KEY = "AIzaSyAJsm4NqIvOGAWnNQd8WNBsYlJNUQ1iqks"  # Ensure this key is valid

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    description = data.get('description', '')

    # If description is empty, return an error message
    if not description:
        return jsonify({"message": "Description is required!"}), 400

    try:
        # Prepare the payload as per the Gemini API documentation
        payload = {
            "contents": [{
                "parts": [{
                    "text": description
                }]
            }]
        }

        # Send the POST request to the Gemini API
        response = requests.post(
            GEMINI_API_URL,
            json=payload,
            params={"key": GEMINI_API_KEY},
            headers={"Content-Type": "application/json"}
        )

        # Check if the response status code is 200 OK
        if response.status_code == 200:
            gemini_data = response.json()
            
            # Extract the content from the API response safely
            candidates = gemini_data.get("candidates", [])
            if candidates:
                generated_content = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "No content generated.")
            else:
                generated_content = "No candidates found in the response."
            
            # Return the generated content as a response
            return jsonify({"message": generated_content})

        # If the response status code is not 200, return the error details
        else:
            return jsonify({
                "message": f"Gemini API error: {response.status_code}, {response.text}"
            }), 500

    except requests.exceptions.RequestException as req_error:
        # Handle network-related errors
        return jsonify({"message": f"Request error: {str(req_error)}"}), 500
    except Exception as e:
        # Handle any other exceptions
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
