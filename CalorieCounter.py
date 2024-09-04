import requests

# Nutritionix API credentials
app_id = 'f9f1895e'
api_key = 'c8cdaff4b8d656b4b7f9d0e53405f424'

def get_nutrition_info(food_item):
    # API endpoint for Nutritionix
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    
    # Request headers including app ID and API key
    headers = {
        'x-app-id': app_id,
        'x-app-key': api_key,
        'Content-Type': 'application/json'
    }
    
    # Request payload with the food item
    payload = {
        "query": food_item,
        "timezone": "US/Eastern"
    }
    
    # Making a POST request to the API
    response = requests.post(url, headers=headers, json=payload)
    
    # Checking if the request was successful
    if response.status_code == 200:
        data = response.json()
        if 'foods' in data:
            food_data = data['foods'][0]
            print(f"Food: {food_data['food_name']}")
            print(f"Calories: {food_data['nf_calories']} kcal")
            print(f"Total Fat: {food_data['nf_total_fat']} g")
            print(f"Carbohydrates: {food_data['nf_total_carbohydrate']} g")
            print(f"Protein: {food_data['nf_protein']} g")
        else:
            print("No data found for the given food item.")
    else:
        print(f"Error: Unable to fetch data (Status code: {response.status_code})")

if __name__ == "__main__":
    # Taking user input
    food_item = input("Enter a food item: ")
    
    # Fetching nutrition information
    get_nutrition_info(food_item)
