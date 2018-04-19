(define (domain maze)
  (:requirements :strips :typing)
  (:types robot cell)

  (:predicates 
    (allowed ?a ?b)
    (at ?r - robot ?a - cell)
  ) 
   
  (:action move
    :parameters (?robby - robot ?a ?b - cell)
    :precondition (and 
                    (allowed ?a ?b)
                    (at ?robby ?a)
                  )
    :effect (and 
              (not (at ?robby ?a))
              (at ?robby ?b)
            )               
  )
)
