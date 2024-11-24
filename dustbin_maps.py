from flask import Flask, request, jsonify
import googlemaps
import os

app = Flask(__name__)

# Initialize the Google Maps client
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))

@app.route('/nearby-recycling', methods=['POST'])
def nearby_recycling():
    try:
        # Get location data from the request
        data = request.json
        user_location = data.get("location")  # Format: "latitude,longitude"

        if not user_location:
            return jsonify({"status": "error", "message": "Location is required and must be in 'latitude,longitude' format."}), 400

        # Query Google Places API for recycling centers within 10km
        results = gmaps.places_nearby(
            location=user_location,
            radius=10000,  # Radius in meters (10km)
            keyword="recycling",  # Look for waste/recycling-related areas
            type="establishment"  # General establishments
        )

        # Check if results are empty
        if not results.get("results"):
            return jsonify({"status": "success", "places": [], "message": "No nearby recycling centers found."})

        # Return the names and addresses of nearby places
        places = [
            {
                "name": place["name"],
                "address": place.get("vicinity", "Address not available"),
                "location": {
                    "latitude": place["geometry"]["location"]["lat"],
                    "longitude": place["geometry"]["location"]["lng"]
                }
            }
            for place in results["results"]
        ]
        return jsonify({"status": "success", "places": places})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
