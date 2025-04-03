import numpy as np
import math
import os

path = os.path.dirname(os.path.realpath(__file__))
pathhistory = os.path.join(path, "history.txt")
pathqueries = os.path.join(path, "queries.txt")


##### CODE FOR CREATING THE VECTORS DONT TOUCH ####
def transaction_reader(file, transaction_num):
    for _ in range(transaction_num):
        line = file.readline()
        if not line:
            break
        item_id, customer_id = map(int, line.split())
        yield item_id, customer_id

def vector_generator(number_of_items, number_of_customers):
    vectors = np.zeros((number_of_items, number_of_customers), dtype=int)
    return vectors

def vector_editor(vectors, item_id, customer_id):
    vectors[item_id - 1, customer_id - 1] = 1 # Subtract 1 to account for zero-based indexing
    return vectors

def history_file_processor():
    history = open("history.txt", "r")
    number_of_customers, number_of_items, number_of_transactions = map(int, history.readline().split())
    vectors = vector_generator(number_of_items, number_of_customers)

    for item_id, customer_id in transaction_reader(history, number_of_transactions):
        vector_editor(vectors, customer_id, item_id)
    
    return vectors

#### CODE FOR PERFORMING CALCULATIONS ####

def calc_angle(x, y):
    norm_x = np.linalg.norm(x)
    norm_y = np.linalg.norm(y)
    if norm_x == 0 or norm_y == 0:  # Avoid division by zero
        return np.nan
    cos_theta = np.dot(x, y) / (norm_x * norm_y)
    theta = math.degrees(math.acos(cos_theta))
    return theta

def angle_calculator(vectors):
    num_items = vectors.shape[0]
    angle_array = np.full((num_items, num_items), np.nan)  # Initialize with NaN

    for i in range(num_items):
        for j in range(i + 1, num_items):  # Only calculate for upper triangle
            angle = calc_angle(vectors[i], vectors[j])
            if 0 <= angle <= 90.0:  # Only store angles in the range [0, 90]
                angle_array[i, j] = angle
                angle_array[j, i] = angle  # Symmetric

    return angle_array

def main():
    vectors = history_file_processor()
    print("Vectors:")
    print(vectors)

    angle_array = angle_calculator(vectors)
    print("\nAngle Array:")
    print(angle_array)

if __name__ == "__main__":
    main()