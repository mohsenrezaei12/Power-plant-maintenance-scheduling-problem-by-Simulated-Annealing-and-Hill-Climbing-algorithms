import random
from random import randrange
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd
import seaborn as sns


def get_information(input_file_txt_1,input_file_txt_2):

    unit_capacity_list = list()
    interval_numbers_list = list()

    with open(input_file_txt_1) as f:
        reader = f.readlines()
        for row in reader[2::3]:
            unit_capacity_list.append(int(row.rstrip('\n')))


    maintenance_intervals_list = list()

    with open(input_file_txt_1) as f:
        reader = f.readlines()
        for row in reader[3::3]:
            maintenance_intervals_list.append(int(row.rstrip('\n')))


    minimum_production_list = list()
    i = 1
    with open(input_file_txt_2) as f:
        reader = f.readlines()
        for row in reader[1:]:
            if (i % 2 == 0):
                minimum_production_list.append(int(row.rstrip('\n')))
            i += 1

    for i in range(0,len(minimum_production_list)):
        interval_numbers_list.append(i+1)


    return unit_capacity_list,minimum_production_list,maintenance_intervals_list,interval_numbers_list




def intial_state(input_unit_capacity,input_minimum_production,input_repair_interval_number):



    unit_capacity = input_unit_capacity
    repair_interval_number = input_repair_interval_number
    minimum_production = input_minimum_production
    maintenance_units_names = []


    initial_state = list()
    initial_net_reserves = list()
    adding = 0
    unit_capacity_temp = list()
    unit_capacity_temp = list(unit_capacity)

    repair_interval_number_temp = list(repair_interval_number)
    counter = 0


    while (True):


        for i in range (len(minimum_production)):

            for i in range(len(unit_capacity_temp)):

                if (repair_interval_number_temp[i] == 0):

                    adding = adding + unit_capacity_temp[i]
                    unit_capacity_temp[i] = 0



            for i in range (len(unit_capacity_temp)):
                column = []

                if (adding >= minimum_production[counter]):

                    initial_state.append(adding)

                    for i in range(len(unit_capacity_temp)):

                        if (unit_capacity_temp[i] != 0):

                            repair_interval_number_temp[i] = repair_interval_number_temp[i] - 1

                            column.append(i)

                    maintenance_units_names.append(column)


                    unit_capacity_temp = list(unit_capacity)
                    adding = 0
                    counter = counter + 1

                    break


                random_item = 0


                while (random_item == 0):

                    random_index = randrange(len(unit_capacity_temp))

                    random_item = unit_capacity_temp[random_index]



                adding = adding + random_item

                unit_capacity_temp[random_index] = 0




        if (all(x == 0 for x in repair_interval_number_temp)):


            for i in range(len(minimum_production)):

                initial_net_reserves.append((initial_state[i] - minimum_production[i]))


            return initial_state,initial_net_reserves,maintenance_units_names

            break

        initial_state.clear()
        repair_interval_number_temp = list(repair_interval_number)
        counter = 0
        adding = 0



def neighborhood(input_minimum_production,input_initial_state,input_initial_net_reserves,input_maintenance_units_names):
    minimum_production = input_minimum_production
    initial_state = input_initial_state
    initial_net_reserves = input_initial_net_reserves
    maintenance_units_names = input_maintenance_units_names


    neighbour_production = list()
    neighbour_net_reserves = list()
    neighbour_production = list(initial_state)
    neighbour_maintenance_units_names = list(maintenance_units_names)

    min_net_reserves_index = initial_net_reserves.index(min(initial_net_reserves))

    for i in range(len(initial_state)):

        if (initial_state[min_net_reserves_index] < initial_state[i] and
                initial_state[min_net_reserves_index] >= minimum_production[i]):


                neighbour_production[min_net_reserves_index], neighbour_production[i] = neighbour_production[i], neighbour_production[min_net_reserves_index]



                neighbour_maintenance_units_names[min_net_reserves_index], neighbour_maintenance_units_names[i] = neighbour_maintenance_units_names[i], neighbour_maintenance_units_names[min_net_reserves_index]


    for i in range(len(initial_state)):

        neighbour_net_reserves.append(neighbour_production[i] - minimum_production[i])



    return neighbour_production,neighbour_net_reserves, neighbour_maintenance_units_names





def fitness (input_neighbour_net_reserves,input_initial_net_reserves,input_initial_state):

    min_neighbour_net_reserves = min(input_neighbour_net_reserves)


    min_initial_net_reserves = min(input_initial_net_reserves)


    if (min_neighbour_net_reserves > min_initial_net_reserves):


        return True

    else:

        return False


def find_best(state, net):
    state_best = list()
    net_best = list()


    if(min(net) > min(net_best)):

        state_best = list(state)
        net_best = list(net)

    return state_best,net_best


def barplot(input_interval_numbers, input_minimum_production, input_net_reserves,input_maintenance_units,input_units_capacity):

    # Data
    r = input_interval_numbers
    raw_data = {'minimum_production': input_minimum_production, 'net_reserves': input_net_reserves, 'maintenance_units': input_maintenance_units}
    df = pd.DataFrame(raw_data)

    #sum of units capacity
    sum_units_capacity = sum(input_units_capacity)

    # From raw value to percentage
    totals = [i + j + k for i, j, k in zip(df['minimum_production'], df['net_reserves'], df['maintenance_units'])]
    minimum_production = [i / j * sum_units_capacity for i, j in zip(df['minimum_production'], totals)]
    net_reserves = [i / j * sum_units_capacity for i, j in zip(df['net_reserves'], totals)]
    maintenance_units = [i / j * sum_units_capacity for i, j in zip(df['maintenance_units'], totals)]

    # plot
    barWidth = 0.85
    names = input_interval_numbers
    # Create green Bars
    plt.bar(r, minimum_production, color='#b5ffb9', edgecolor='white', width=barWidth , label="minimum production")
    # Create orange Bars
    plt.bar(r, net_reserves, bottom=minimum_production, color='#f9bc86', edgecolor='white', width=barWidth , label="net reserves")
    # Create blue Bars
    plt.bar(r, maintenance_units, bottom=[i + j for i, j in zip(minimum_production, net_reserves)], color='#bfc7c7', edgecolor='white',
            width=barWidth ,  label="maintenance units")

    # Custom x axis
    plt.xticks(r, names)
    plt.xlabel("Time interval")
    plt.ylabel("MW")

    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=1)
    plt.subplots_adjust(right=0.85)
    # Show graphic
    plt.show()



def maintenance(input_unit_capacity,input_initial_state):
    maintenance_list = list()
    max = sum(input_unit_capacity)
    for i in range(len(input_initial_state)):
        maintenance_list.append(max - input_initial_state[i])


    return maintenance_list

def line_chart(generations,min_net_reserve):

    df = pd.DataFrame({'x_values': range(1, generations+1 ), 'y_values': min_net_reserve})

    # Draw plot
    plt.plot('x_values', 'y_values', data=df, color='skyblue')
    plt.xlabel("generations")
    plt.ylabel("minimum of net reserves")
    plt.show()







best_state = list()
best_net = [-1,-1,-1,-1,-1,-1]

minimum_net_reserves_list = list()

generation = 100

for i in range(0,generation):


    while_condition = True

    primary_info = get_information("txt_1.txt","txt_2.txt")


    intial_state_info = intial_state(primary_info[0],primary_info[1],primary_info[2])

    intial_state_temp = intial_state_info[0]
    intial_net_temp = intial_state_info[1]
    initial_maintenance_units_names_temp = intial_state_info[2]

    while(while_condition):

        neighbor_info = neighborhood(primary_info[1],intial_state_temp,intial_net_temp,initial_maintenance_units_names_temp)

        neighbor_state_temp = neighbor_info[0]
        neighbor_net_temp = neighbor_info[1]
        neighbor_maintenance_units_names_temp = neighbor_info[2]

        fitness_info = fitness(neighbor_net_temp,intial_net_temp,intial_state_temp)
        while_condition = fitness_info

        if(while_condition == False):

            print("intial_state_temp:",intial_state_temp)
            print("intial_net_temp:",intial_net_temp)

            minimum_net_reserves_list.append(min(intial_net_temp))

            if(min(intial_net_temp) > min(best_net)):

                best_state = list(intial_state_temp)
                best_net = list(intial_net_temp)
                best_maintenance_units_names = list(initial_maintenance_units_names_temp)




        intial_state_temp = list(neighbor_state_temp)
        intial_net_temp = list(neighbor_net_temp)
        initial_maintenance_units_names_temp = list(neighbor_maintenance_units_names_temp)

print("############################################################################")
print("best state: ",best_state)
print("best net reserves: ",best_net)
print("maintenance_units_names: ", best_maintenance_units_names)







maintenance_list = maintenance(primary_info[0],best_state)

barplot(primary_info[3],primary_info[1],best_net,maintenance_list,primary_info[0])

line_chart(generation,minimum_net_reserves_list)
