import numpy as np
import math

angle_dictionary = {}  
angle_list = []
average_angle = 0

def history_reader():
    # Opens the history file and processes it to be passed onto the vector writer function to generate the appropriate vectors
    with open("history.txt", "r") as history_file:
        customer_num, item_num, transaction_num = map(int, history_file.readline().split())  # First line determines dimensions of the matrix
        vectors = vector_writer(customer_num, item_num)  # Initialize the NumPy array

        # The file is read line by line, and the customer ID and item ID are extracted. The vector editor function updates the matrix.
        for customer_id, item_id in transaction_reader(history_file, transaction_num):
            vector_editor(vectors, customer_id, item_id)
    return vectors

# This helper function creates a 2D NumPy array initialized to zero.
def vector_writer(customer_num, item_num):
    # Create a 2D NumPy array with dimensions (item_num, customer_num), initialized to zeros
    vectors = np.zeros((item_num, customer_num), dtype=int)
    return vectors

# This helper function updates the NumPy array for a specific item and customer, accounting for zero-based indexing.
def vector_editor(vectors, customer_id, item_id):
    # Update the matrix at the position corresponding to the item and customer
    vectors[item_id - 1, customer_id - 1] = 1  # Subtract 1 to account for zero-based indexing
    return vectors

# This helper function reads the transaction file line by line, extracting customer and item IDs for use by the history_reader function.
def transaction_reader(file, transaction_num):
    for _ in range(transaction_num):
        line = file.readline()
        if not line:
            break
        customer_id, item_id = map(int, line.split())
        yield customer_id, item_id

# Calculate the angle between each pair of vectors in the NumPy array and then calculate the average angle.
def angle_calculator(vectors):
    global angle_list, angle_dictionary
    for i in range(vectors.shape[0]):
        for j in range(i + 1, vectors.shape[0]):
            dot_product = np.dot(vectors[i], vectors[j])
            norm_i = np.linalg.norm(vectors[i])
            norm_j = np.linalg.norm(vectors[j])
            if norm_i == 0 or norm_j == 0:
                continue  # Avoid division by zero
            angle = math.acos(dot_product / (norm_i * norm_j))
            angle = math.degrees(angle)
            angle = round(angle, 2)

            angle_dictionary_writer(i, j, angle)
            print(f"Angle for vector {i} and {j}: {angle}")

    # Calculate the positive entries and update angle_list accordingly
    positive_threshold = 0  # Define the threshold for counting a positive entry (e.g., angle < 90 degrees)
    positive_entries = 0
    for key, inner_dict in angle_dictionary.items():
        for sub_key, angle in inner_dict.items():
            if angle < positive_threshold:
                positive_entries += 1
                angle_list.append(angle)

    print(f"Positive entries: {positive_entries}")

    # Calculate the average angle
    if angle_list:
        average_angle = sum(angle_list) / len(angle_list)
        average_angle = round(average_angle, 2)
    else:
        average_angle = 0

    return average_angle

def angle_dictionary_writer(vector_i, vector_j, angle):
    # Store the angle between vectors i and j in the dictionary
    if vector_i not in angle_dictionary:
        angle_dictionary[vector_i] = {}
    # Use the min function to ensure that the smallest angle is stored between any pair of vectors
    angle_dictionary[vector_i][vector_j] = min(angle_dictionary.get(vector_i, {}).get(vector_j, angle), angle)
    return angle_dictionary

def query_reader():
    queries = []
    with open("queries.txt", "r") as query_file:
        for line in query_file: 
            queries.append(list(map(int, line.split())))

    return queries

def find_best_match(item, query, angle_dictionary):
    if item not in angle_dictionary:
        return None, None  # No match found

    min_angle = float("inf")
    best_match = None

    for potential_match, angle in angle_dictionary[item].items():
        if potential_match not in query and angle < min_angle:  
            min_angle = angle
            best_match = potential_match

    return best_match, min_angle if best_match else (None, None)

def recommendation_writer(queries, angle_dictionary):
    with open("output.txt", "w") as output:  # Open file in write mode
        output.write(f"Positive entries: {len(angle_list)}\n")
        output.write(f"Average angle: {average_angle}\n")

        for query in queries:
            output.write(f"Shopping cart: {' '.join(map(str, query))}\n")
            recommendations = {}

            for item in query:
                best_match, min_angle = find_best_match(item, query, angle_dictionary)
                if best_match:
                    output.write(f"Item: {item}; match: {best_match}; angle: {min_angle:.2f}\n")
                    recommendations[best_match] = min_angle
                else:
                    output.write(f"Item: {item} no match\n")

            if recommendations:
                sorted_recommendations = sorted(recommendations.keys(), key=lambda x: recommendations[x])
                output.write(f"Recommend: {' '.join(map(str, sorted_recommendations))}\n\n")
            else:
                output.write("Recommend:\n\n")

def main():
    vectors = history_reader()  # Read the file and process transactions
    global average_angle
    average_angle = angle_calculator(vectors)  # Calculate angles between vectors
    queries = query_reader()  # Read the queries from the file
    recommendation_writer(queries, angle_dictionary)  # Write recommendations to file

if __name__ == "__main__":
    main()