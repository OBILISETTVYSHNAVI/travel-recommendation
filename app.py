
def recommend_places(state, place_type, best_time):
     # Check if all selections are None
    if state == "None" and place_type == "None" and best_time == "None":
        return "Please select at least one option to get recommendations."

    # Convert input text to encoded values
    if state == "None":
        state_encoded = None
    elif state in label_encoders['State'].classes_:
        state_encoded = label_encoders['State'].transform([state])[0]
    else:
        return "Invalid state selection."

    if place_type == "None":
        type_encoded = None
    elif place_type in label_encoders['Type'].classes_:
        type_encoded = label_encoders['Type'].transform([place_type])[0]
    else:
        return "Invalid place type selection."

    if best_time == "None":
        best_time_encoded = None
    elif best_time in label_encoders['BestTimeToVisit'].classes_:
        best_time_encoded = label_encoders['BestTimeToVisit'].transform([best_time])[0]
    else:
        return "Invalid best time selection."

    # Filter based on given inputs
    filtered_data = data.copy()
    if state_encoded is not None:
        filtered_data = filtered_data[filtered_data['State'] == state_encoded]
    if type_encoded is not None:
        filtered_data = filtered_data[filtered_data['Type'] == type_encoded]
    if best_time_encoded is not None:
        filtered_data = filtered_data[filtered_data['BestTimeToVisit'] == best_time_encoded]

    # If no recommendations found, use manual fallback
    if filtered_data.empty:
        if state in manual_recommendations and place_type in manual_recommendations[state]:
            return manual_recommendations[state][place_type]
        else:
            return "No recommendations found. Try different selections."

    # Decode the recommended place names
    recommendations = label_encoders['Name'].inverse_transform(filtered_data['Name'].unique())

    return recommendations if len(recommendations) > 0 else "No recommendations found."
    
demo = gr.Interface(
    fn=recommend_places,
    inputs=[
        gr.Dropdown(choices=["None"] + list(label_encoders['State'].inverse_transform(range(len(label_encoders['State'].classes_)))), label='State'),
        gr.Dropdown(choices=["None"] + list(label_encoders['Type'].inverse_transform(range(len(label_encoders['Type'].classes_)))), label='Type'),
        gr.Dropdown(choices=["None"] + list(label_encoders['BestTimeToVisit'].inverse_transform(range(len(label_encoders['BestTimeToVisit'].classes_)))), label='Best Time to Visit'),
    ],
    outputs="text",
    title="Travel Destination Recommender",
    description="Get recommended travel destinations based on your selected state, place type, and best time to visit."
)

# Launch the app
if __name__ == "__main__":
    demo.launch()
