import numpy as np
import math 

angle_array = None  # Initialize the 2D NumPy array for storing angles
average_angle = 0
number_positive_entries = 0

def history_reader():
    history_file = open("history.txt", "r")
    customer_num, item_num, transaction_num = map(int, history_file.readline().split())
    vectors = vector_writer(customer_num, item_num)

    for customer_id, item_id in transaction_reader(history_file, transaction_num):
        vector_editor(vectors, customer_id, item_id)
    history_file.close()
    return vectors

def vector_writer(customer_num, item_num):
    vectors = np.zeros((item_num, customer_num), dtype=int)
    return vectors

def vector_editor(vectors, customer_id, item_id):
    vectors[item_id - 1, customer_id - 1] = 1
    return vectors

def transaction_reader(file, transaction_num):
    for _ in range(transaction_num):
        line = file.readline()
        if not line:
            break
        customer_id, item_id = map(int, line.split())
        yield customer_id, item_id

def angle_calculator(vectors):
    global angle_array
    num_items = vectors.shape[0]
    angle_array = np.full((num_items, num_items), np.nan)  # Initialize with NaN

    for i in range(num_items):
        for j in range(i + 1, num_items):
            dot_product = np.dot(vectors[i], vectors[j])
            norm_i = np.linalg.norm(vectors[i])
            norm_j = np.linalg.norm(vectors[j])
            if norm_i == 0 or norm_j == 0:
                continue
            angle = math.acos(dot_product / (norm_i * norm_j))
            angle = math.degrees(angle)

            if 0 <= angle <= 90.0:
                angle_array[i, j] = angle
                angle_array[j, i] = angle  # Symmetric

    global number_positive_entries
    valid_angles = ~np.isnan(angle_array)
    number_positive_entries = np.sum(valid_angles) // 2  # Count unique pairs
    total_sum = np.nansum(angle_array) / 2  # Sum of unique pairs
    global average_angle
    average_angle = round(total_sum / number_positive_entries, 2)

def query_reader():
    queries = []
    query_file = open("queries.txt", "r")
    for line in query_file:
        queries.append(list(map(int, line.split())))
    return queries

def find_best_match(item, query, angle_array):
    if item >= angle_array.shape[0]:
        return None, None

    min_angle = float("inf")
    best_match = None

    for potential_match in range(angle_array.shape[1]):
        angle = angle_array[item, potential_match]
        if not np.isnan(angle) and potential_match not in query and angle < min_angle:
            min_angle = angle
            best_match = potential_match

    return best_match, min_angle if best_match is not None else (None, None)

def recommendation_writer(queries, angle_array):
    with open("output.txt", "w") as output:
        output.write(f"Positive entries: {number_positive_entries}\n")
        output.write(f"Average angle: {average_angle}\n")

        for query in queries:
            output.write(f"Shopping cart: {' '.join(map(str, query))}\n")
            recommendations = {}

            for item in query:
                best_match, min_angle = find_best_match(item, query, angle_array)
                if best_match is not None:
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
    vectors = history_reader()
    angle_calculator(vectors)
    queries = query_reader()
    recommendation_writer(queries, angle_array)
    print(average_angle)
    print(number_positive_entries)

if __name__ == "__main__":
    main()