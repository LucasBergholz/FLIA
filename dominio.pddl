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