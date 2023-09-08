# Université de Sherbrooke
# Code préparé par Audrey Corbeil Therrien
# Laboratoire 1 - Interaction avec prolog

from swiplserver import PrologMQI


if __name__ == '__main__':
       
    with PrologMQI() as mqi_file:
        with mqi_file.create_thread() as prolog_thread:
            #### NO 1 LAB1 ####
            #result = prolog_thread.query("[prolog/rest_op].")
            #print(result)

            #result = prolog_thread.query("repas(H, P, D).")
            #print(result)
            #### NO 2 LAB1 ####
            print(prolog_thread.query("[code_labo1/prolog/un_sur_deux]"))
            print(prolog_thread.query("appendop([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], X)."))
            print(prolog_thread.query("appendop([], X)."))
            print(prolog_thread.query("appendop([1], X)."))

            #### NO 3 LAB1 ####
            # print(prolog_thread.query("[code_labo1/prolog/action_possible]"))
            # print(prolog_thread.query("move()"))
