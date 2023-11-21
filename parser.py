from typing import List
import sys
import os
import subprocess

CELL_ON = "L"
CELL_AT = "D"
BUTTON_AT = "d"
BUTTON_ON = "l"
POSITION = "position"

SOLVER = ""
PROBLEM_PATH = ""
DOMAIN_PATH = ""

def generate_cell_on_button_at(len_lines, len_columns):
    predicates_cell_on = []
    for i in range(1, len_lines+1):
        for j in range(1, len_columns+1):
            if(lines[i-1][j-1] == CELL_ON):
                predicates_cell_on.append(f"(cell-on x{i} y{j})")
            if(lines[i-1][j-1] == BUTTON_AT):
                predicates_cell_on.append(f"(button-at x{i} y{j})")
            if(lines[i-1][j-1] == BUTTON_ON):
                predicates_cell_on.append(f"(button-at x{i} y{j})")
                predicates_cell_on.append(f"(cell-on x{i} y{j})")

    return " ".join(predicates_cell_on)

def generate_edge(len_lines, len_columns):
    predicates_edge = []
    for i in range(1, len_lines+1):
        for j in range(1, len_columns+1):
            if ((j == 1 and i!=1 and i != len_lines) or (j == len_columns and i!=1 and i != len_lines) or (i == 1 and j!=1 and j != len_columns) or (i == len_lines and j!=1 and j != len_columns)):
                predicates_edge.append(f"(is-edge x{i} y{j})")
    return " ".join(predicates_edge)

def generate_vertice(len_lines, len_columns):
    predicates_vertice = []
    predicates_vertice.append(f"(is-vertice x{1} y{1})")
    predicates_vertice.append(f"(is-vertice x{1} y{len_columns})")
    predicates_vertice.append(f"(is-vertice x{len_lines} y{1})")
    predicates_vertice.append(f"(is-vertice x{len_lines} y{len_columns})")
    return " ".join(predicates_vertice)


def generate_incs(len_lines, len_columns):
    predicates_x = []
    predicates_y = []
    for i in range(1, len_lines):
        predicates_x.append(f"(inc x{i} x{i+1})")
    for i in range(1, len_columns):
        predicates_y.append(f"(inc y{i} y{i+1})")
    return " ".join(predicates_x), " ".join(predicates_y)

def generate_decs(len_lines, len_columns):
    predicates_x = []
    predicates_y = []
    for i in range(len_lines, 1, -1):
        predicates_x.append(f"(dec x{i} x{i-1})")
    for i in range(len_columns, 1, -1):
        predicates_y.append(f"(dec y{i} y{i-1})")
    return " ".join(predicates_x), " ".join(predicates_y)

def generate_problem(map_path):
    problem_path = map_path + ".pddl"
    y_positions = []

    x_positions = []

    for i in range(num_lines):
        x_positions.append(f"x{i+1}")

    for j in range(num_columns):
        y_positions.append(f"y{j+1}")

    inc_x, inc_y = generate_incs(num_lines, num_columns)
    dec_x, dec_y = generate_decs(num_lines, num_columns)
    cell_on = generate_cell_on_button_at(num_lines, num_columns)
    is_vertice = generate_vertice(num_lines, num_columns)
    is_edge = generate_edge(num_lines, num_columns)

    with open(problem_path, 'w') as problem_file:
        problem_file.write(f"""
            (define (problem {map_path})
                (:domain lightsout)
                (:objects {" ".join(x_positions)} - x_position {" ".join(y_positions)} - y_position)
                (:init
                    {inc_x}
                    {inc_y}
                    {dec_x}
                    {dec_y}
                    {cell_on}
                    {is_vertice}
                    {is_edge}
                )
                (:goal
                    (and
                        (forall (?x - x_position ?y - y_position)
                            (not (cell-on ?x ?y))
                        )
                    )
                )
            )
            """)

def generate_domain():
    domain_path = "domainOptimizedTeste.pddl"
    with open(domain_path, 'w') as domain_file:
        domain_file.write(f"""
            (define (domain lightsout)
            (:requirements :strips)
            (:types
                x_position y_position - position
            )

            (:predicates
                    (button-at ?a - x_position ?b - y_position)
                    (inc ?a ?b - position)
                    (dec ?a ?b - position)
                    (cell-on ?a - x_position ?b - y_position)
                    (is-vertice ?a - x_position ?b - y_position)
                    (is-edge ?a - x_position ?b - y_position)
            )

            (:action INVERT_CELL
                :parameters (?x ?x2 ?x0 - x_position ?y ?y2 ?y0 - y_position)
                    :precondition (and  (inc ?y ?y2)
                                        (inc ?x ?x2)
                                        (dec ?y ?y0)
                                        (dec ?x ?x0)
                                )
                    :effect (and
                            (when (and (cell-on ?x ?y) (not(button-at ?x ?y)))  (not (cell-on ?x ?y)))
                            (when (and (not (cell-on ?x ?y)) (not(button-at ?x ?y))) (cell-on ?x ?y))

                            (when (cell-on ?x ?y2)  (not (cell-on ?x ?y2)))
                            (when (not (cell-on ?x ?y2)) (cell-on ?x ?y2))

                            (when (cell-on ?x ?y0)  (not (cell-on ?x ?y0)))
                            (when (not (cell-on ?x ?y0)) (cell-on ?x ?y0))

                            (when (cell-on ?x0 ?y)  (not (cell-on ?x0 ?y)))
                            (when (not (cell-on ?x0 ?y)) (cell-on ?x0 ?y))

                            (when (cell-on ?x2 ?y)  (not (cell-on ?x2 ?y)))
                            (when (not (cell-on ?x2 ?y)) (cell-on ?x2 ?y))
                            )
            )
            (:action INVERT_VERTICE
                :parameters(?x ?x2 - x_position ?y ?y2 - y_position)
                :precondition (and
                                    (is-vertice ?x ?y)
                                    (or
                                        (and (inc ?x ?x2) (dec ?y ?y2))
                                        (and (inc ?y ?y2) (inc ?x ?x2))
                                        (and (dec ?x ?x2) (dec ?y ?y2))
                                        (and (dec ?x ?x2) (inc ?y ?y2))
                                    )
                            )
                :effect (and

                        (when (and (cell-on ?x ?y) (not(button-at ?x ?y)))  (not (cell-on ?x ?y)))
                        (when (and (not (cell-on ?x ?y))(not(button-at ?x ?y))) (cell-on ?x ?y))

                        (when (cell-on ?x ?y2)  (not (cell-on ?x ?y2)))
                        (when (not (cell-on ?x ?y2)) (cell-on ?x ?y2))

                        (when (cell-on ?x2 ?y)  (not (cell-on ?x2 ?y)))
                        (when (not (cell-on ?x2 ?y)) (cell-on ?x2 ?y))
                        )
            )

            (:action INVERT_EDGE
            :parameters (?x ?a - x_position ?y ?c - y_position ?b - position)
                :precondition (and
                                    (is-edge ?x ?y)
                                    (or
                                        (and (inc ?x ?a) (dec ?x ?b) (dec ?y ?c))
                                        (and (inc ?x ?a) (dec ?x ?b) (inc ?y ?c))
                                        (and (inc ?x ?a) (inc ?y ?b) (dec ?y ?c))
                                        (and (dec ?x ?a) (inc ?y ?b) (dec ?y ?c))
                                    )
                            )
                :effect (and
                        (when (and (cell-on ?x ?y) (not(button-at ?x ?y)))  (not (cell-on ?x ?y)))
                        (when (and (not (cell-on ?x ?y))(not(button-at ?x ?y))) (cell-on ?x ?y))

                        (when (cell-on ?a ?y)  (not (cell-on ?a ?y)))
                        (when (not (cell-on ?a ?y)) (cell-on ?a ?y))

                        (when (cell-on ?x ?c)  (not (cell-on ?x ?c)))
                        (when (not (cell-on ?x ?c)) (cell-on ?x ?c))

                        (when (and (cell-on ?b ?y)(dec ?x ?b))  (not (cell-on ?b ?y)))
                        (when (and (not (cell-on ?b ?y))(dec ?x ?b)) (cell-on ?b ?y))

                        (when (and (cell-on ?x ?b) (inc ?y ?b))  (not (cell-on ?x ?b)))
                        (when (and (not (cell-on ?x ?b)) (inc ?y ?b)) (cell-on ?x ?b))

                    )
        )
)
""")

def main():
    global lines
    lines = []
    global num_lines
    num_lines = 0
    global num_columns
    num_columns = 0
    while True:
        try:
            user_input = input()
            lines.append(user_input)
            num_lines += 1
        except EOFError:
            break

    num_columns = len(lines[0])
    generate_domain()
    generate_problem("problemaOptimizedTeste")
    command = " /tmp/dir/software/planners/madagascar/M -S 1 domainOptimizedTeste.pddl problemaOptimizedTeste.pddl"

    result = subprocess.check_output(command, shell=True, text=True)
    clicks = result.split("\n")

    # Deixando apenas as linhas com invert nela
    only_invert = []
    for line in clicks:
        if "STEP" in line:
            index_begin = line.find("i")
            line = line[index_begin:]
            only_invert.append(line)

    # Para cada linha da lista, um comando invert
    one_invert_per_line = []
    for line in only_invert:
        # Checando numero de ocorrencias do invert
        count = line.count("invert")
        if count > 1:
            # Separar a linha em varias linhas, um invert em cada
            new_lines = line.split()
            # A lista se torna ela + as linhas separadas
            one_invert_per_line = one_invert_per_line + new_lines
        else:
            # Se so tiver um invert, some a linha a nova lista
            one_invert_per_line.append(line)

    # Lista final com as coordenadas conforme enunciado do exercicio
    final_list = []
    for line in one_invert_per_line:
        index_x = line.find("x")
        first_comma = line.find(",")
        index_y = line.find("y")
        second_comma = line.find(",", first_comma+1)
        third_comma = line.find(",", second_comma+1)
        if "cell" in line:
            final_comma = line.find(",", third_comma+1)
        else:
            final_comma = third_comma
        x = int(line[index_x+1 : first_comma]) - 1
        y = int(line[index_y+1:final_comma]) - 1
        text = "(" + str(x) + ", " + str(y) + ")"
        final_list.append(text)

    for i in range(len(final_list)-1):
        print(final_list[i]+";", end="")

    print(final_list[-1])

    #Ler saída do madascagar
    #Tratar a saída
    #Printar a saída


if __name__ == "__main__":
    """ if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <map_filepath>")
        print("Error: map path must be specified")
        exit(1) """
    main()
####################
