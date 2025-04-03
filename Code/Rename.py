import numpy as np
import math 
import os

# os implementation
pathCurrent = os.path.dirname(os.path.realpath(__file__))
pathHistory = os.path.join(pathCurrent, '../history.txt')
pathQuery = os.path.join(pathCurrent, '../queries.txt')

# This function opens the history file and creates an array of vectors to use for calculation
def history_reader():
    history_file = open(pathHistory, "r")
    customer_num, item_num, transaction_num = map(int, history_file.readline().split())
    vectors = vector_writer(customer_num, item_num)

    # for loop to create an empty array dependant on the dimensions stated by the history file and counts the positive entries
    positive_entries_array = np.zeros((int(customer_num), int(item_num)))
    positive_entries = 0
    for customer_id, item_id in transaction_reader(history_file, transaction_num):
        vector_editor(vectors, customer_id, item_id)
        if (positive_entries_array[customer_id-1][item_id-1] == 0):
            positive_entries += 1
        
    history_file.close()
    return vectors, customer_num, item_num, transaction_num, customer_id, item_id, positive_entries

# helper function to create empty variables
def vector_writer(customer_num, item_num):
    vectors = np.zeros((item_num, customer_num), dtype=int)
    return vectors

# helper function to edit the created variables
def vector_editor(vectors, customer_id, item_id):
    vectors[item_id - 1, customer_id - 1] = 1
    return vectors

# reads each transaction to generate a customer and item id for use with the vector editor
def transaction_reader(file, transaction_num):
    for _ in range(transaction_num):
        line = file.readline()
        if not line:
            break
        customer_id, item_id = map(int, line.split())
        yield customer_id, item_id

# calculates the angles for every unique pair of vectors and stores them to a 2d array for recommendation
def angle_calculator(vectors, item_num):
    angles_dimension = [[90.00]*int(item_num)]*int(item_num)
    angles_map = np.array(angles_dimension)
    angle_list = []

    # nested for loops to calculate the angle between each unique pair
    for i in range(item_num):
        for j in range(i + 1, item_num):
            dot_product = np.dot(vectors[i], vectors[j])
            norm_i = np.linalg.norm(vectors[i])
            norm_j = np.linalg.norm(vectors[j])
            if norm_i == 0 or norm_j == 0:
                continue
            angle = math.acos(dot_product / (norm_i * norm_j))
            angle = math.degrees(angle)
            angle_list.append(angle)

            # avarage angle calculation
            mean = np.mean(angle_list)
            rounded_mean = round(mean, 2)

            # Symetry check for the 2d array
            if 0 < angle or angle < 90.0:
                angles_map[i][j] = angle
                angles_map[j][i] = angle 
    
    return angles_dimension, angles_map, angle_list, rounded_mean

# this function performs the main comparisons for the queries and formats the outputs
def perform_query(angle_dimension):
    query_file = open(pathQuery, 'r')
    boolean_exit = True
    while boolean_exit:
        line_of_query = query_file.readline().strip().split()

        if line_of_query == []:
            break

        num_of_queries = []
        for query_element in line_of_query:
            if query_element == ' ':
                pass
            else:
                num_of_queries.append(query_element)
        
        # handles the output of the current query for the user
        print("Shopping cart:", end="") 
        for i in num_of_queries:
            print(f" {i}", end='')
        print()

        # algorithm to complete comparisons and output the result
        recommend = {}
        for element in num_of_queries:
            print(f"Item: {element}", end="")
            angle_comparitor = 90
            angle_number, angle_saved = 0, 0
            visible_array = angle_dimension[int(element) - 1, :]
            for angle in visible_array:
                angle_number = angle_number +1
                if float(angle) < angle_comparitor:
                    if str(angle_number) not in num_of_queries:
                        angle_comparitor = angle
                        angle_saved = angle_number
            if angle_comparitor < 90:
                print(f"; match: {angle_saved}; angle: {"{:.2f}".format(angle_comparitor, 2)}")
                recommend["{:.2f}".format(angle_comparitor)] = angle_saved
            else: print(f" no match")

        print("Recommend:", end="")
        recommend = sorted(recommend.items())

        for x, y in recommend:
            print(f" {y}", end="")
        print()

def main():
    # Call the history reader function to produce the vectors needed for pre calculation
    vectors, customer_num, item_num, transaction_num, customer_id, item_id, positive_entries = history_reader()
    print(f"Positive Entries: {positive_entries}")

    # call angle calculator function calculate the angles between each unique vector pair and store them in 2d array
    angle_dimensions, angles_map, angle_list, rounded_mean = angle_calculator(vectors, item_num)
    print(f"Average angle: {rounded_mean}")

    # call the perform query function to calculate the comparisons and output results
    perform_query(angles_map)

if __name__ == "__main__":
    main()