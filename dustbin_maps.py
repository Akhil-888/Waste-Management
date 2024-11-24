from flask import Flask, request, jsonify
import googlemaps
import os

app = Flask(__name__)

# Initialize the Google Maps client using environment variables
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))

@app.route('/nearby-recycling', methods=['POST'])
def nearby_recycling():
    try:
        # Get location data from the request
        data = request.json
        user_location = data.get("location")  # Format: {"location": "latitude,longitude"}

        if not user_location:
            return jsonify({"status": "error", "message": "No location provided"}), 400

        # Query Google Places API for recycling centers within 10km
        results = gmaps.places_nearby(
            location=user_location,
            radius=10000,  # Radius in meters (10km)
            keyword="recycling",  # Look for waste/recycling-related areas
            type="establishment"  # General establishments
        )

        # Extract useful information
        places = [
            {
                "name": place["name"],
                "address": place.get("vicinity", "Address not available"),
                "location": place["geometry"]["location"]
            }
            for place in results.get("results", [])
        ]

        if not places:
            return jsonify({"status": "success", "message": "No recycling centers found within 10km", "places": []})

        return jsonify({"status": "success", "places": places})

    except googlemaps.exceptions.ApiError as e:
        return jsonify({"status": "error", "message": f"API error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": f"Unexpected error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
