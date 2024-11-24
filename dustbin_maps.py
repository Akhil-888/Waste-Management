from flask import Flask, request, jsonify
import googlemaps

app = Flask(__name__)

# Initialize the Google Maps client
gmaps = googlemaps.Client(key="YOUR_GOOGLE_MAPS_API_KEY")

@app.route('/nearby-recycling', methods=['POST'])
def nearby_recycling():
    try:
        # Get location data from the request
        data = request.json
        user_location = data.get("location")  # Format: {"location": "latitude,longitude"}

        # Query Google Places API for recycling centers within 10km
        results = gmaps.places_nearby(
            location=user_location,
            radius=10000,  # Radius in meters (10km)
            keyword="recycling",  # Look for waste/recycling-related areas
            type="establishment"  # General establishments
        )

        # Return the names and addresses of nearby places
        places = [
            {
                "name": place["name"],
                "address": place.get("vicinity", "Address not available"),
                "location": place["geometry"]["location"]
            }
            for place in results.get("results", [])
        ]
        return jsonify({"status": "success", "places": places})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

