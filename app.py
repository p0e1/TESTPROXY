import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Get the Gemini API key from environment variables
GEMINI_API_KEY = os.environ.get("AIzaSyBBUOYsX2pxDJL33923sMtM4xA1QL4PTtY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

# Gemini API endpoint (replace with the actual endpoint)
GEMINI_API_ENDPOINT = "YOUR_GEMINI_API_ENDPOINT"  # Replace with the real endpoint

@app.route("/", methods=["POST"])
def handle_request():
    try:
        data = request.get_json()
        action = data.get("action")

        if action == "generate_text":
            prompt = data.get("prompt")
            if not prompt:
                return jsonify({"error": "Prompt is required."}), 400

            try:
                # Make the Gemini API call
                headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}  # Correct authorization
                gemini_response = requests.post(GEMINI_API_ENDPOINT, json={"prompt": prompt}, headers=headers)
                gemini_response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

                gemini_data = gemini_response.json()

                # Extract the generated text (adjust based on the Gemini API response structure)
                generated_text = gemini_data.get("choices")[0].get("text") # Example: Assuming a 'choices' array

                if not generated_text:
                    return jsonify({"error": "Could not extract text from Gemini response."}), 500

                return jsonify({"generated_text": generated_text}), 200

            except requests.exceptions.RequestException as e:
                return jsonify({"error": f"Error communicating with Gemini API: {str(e)}"}), 500
            except (KeyError, IndexError) as e:  # Handle potential issues with Gemini's response structure
                return jsonify({"error": f"Error parsing Gemini response: {str(e)}. Raw response: {gemini_data}"}), 500
        else:
            return jsonify({"error": "Invalid action."}), 400

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port) # debug=True for development only!
