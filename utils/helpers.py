def format_response(data, message="Success"):
    return {
        "status": "success",
        "message": message,
        "data": data
    }

def calculate_distance(coord1, coord2):
    # Ví dụ: Tính khoảng cách giữa hai tọa độ (giả sử tọa độ là (latitude, longitude))
    from geopy.distance import geodesic
    return geodesic(coord1, coord2).kilometers
