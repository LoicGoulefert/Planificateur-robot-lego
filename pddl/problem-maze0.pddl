; 2
; 2
; It looks like this:
;
;  +---+---+
;  | X |   |
;  +---+---+
;  |   | a |
;  +---+---+
;

(define (problem maze1)
  (:domain maze)
  (:objects c-0-0 c-0-1
            c-1-0 c-1-1 - cell
            X - robot)
  (:init
    ;; Horizontal allowed moves
    (allowed c-0-0 c-0-1)
    (allowed c-1-0 c-1-1)

    (allowed c-0-1 c-0-0)
    (allowed c-1-1 c-1-0)

    ;; Vertical allowed moves
    (allowed c-0-0 c-1-0)
    (allowed c-0-1 c-1-1)

    (allowed c-1-0 c-0-0)
    (allowed c-1-1 c-0-1)

    ;; Initial robot position
    (at X c-0-0))

  (:goal
    (at X c-1-1)
  )
)
