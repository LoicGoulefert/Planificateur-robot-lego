
(define (domain maze)
  (:requirements :strips :typing)
  (:types agent position)

  (:predicates 
    (inc ?a ?b - position)
    (dec ?a ?b - position)
    (at ?a - agent ?x ?y - position)
    (wall ?x ?y ?axis)
    )
   
  (:action move-up
    :parameters (?omf - agent ?x ?y ?yn - position)
    :precondition ()
    :effect (when 
                (and (at ?omf ?x ?y)
                     (dec ?y ?yn)
                     (not (wall ?x ?y ?yn))) ;; condition
                (and (not (at ?omf ?x ?y))   ;; effect
                     (at ?omf ?x ?yn))
                )
                    
    )
    
  (:action move-down
    :parameters (?omf - agent ?x ?y ?yn - position)
    :precondition ()
    :effect (when 
                (and (at ?omf ?x ?y)
                     (inc ?y ?yn)
                     (not (wall ?x ?y ?yn)))
                (and (not (at ?omf ?x ?y))
                     (at ?omf ?x ?yn))
              )
    )

  (:action move-right
    :parameters (?omf - agent ?x ?y ?xn - position)
    :precondition ()
    :effect (when 
              (and (at ?omf ?x ?y)
                   (inc ?x ?xn)
                   (not (wall ?x ?y ?xn)))
              (and (not (at ?omf ?x ?y))
                   (at ?omf ?xn ?y))
              )
    )


  (:action move-left
    :parameters (?omf - agent ?x ?y ?xn - position)
    :precondition ()
    :effect (when 
              (and (at ?omf ?x ?y)
                   (dec ?x ?xn)
                   (not (wall ?x ?y ?xn)))
              (and (not (at ?omf ?x ?y))
                   (at ?omf ?xn ?y))
              )
    )
  )
