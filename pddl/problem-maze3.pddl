; 25
; It looks like this:
;
;    .___.___.___.___.___.
;    |   |               |
;    | X |   .___.___.   |
;    |           |       |
;    |   .___.   |   .   |
;    |       |   |   |   |
;    |   .___|___|   |_b_|
;    |                   |
;    |   .   .   .___.   |
;    |   |   |       |   |
;    |_Y_|___|___._a_|___|



(define (problem maze1)
  (:domain maze)
  (:objects c-0-0 c-0-1 c-0-2 c-0-3 c-0-4
            c-1-0 c-1-1 c-1-2 c-1-3 c-1-4
            c-2-0 c-2-1 c-2-2 c-2-3 c-2-4
            c-3-0 c-3-1 c-3-2 c-3-3 c-3-4
            c-4-0 c-4-1 c-4-2 c-4-3 c-4-4 - cell
            X Y - robot)
  (:init
    ;; Horizontal allowed moves
    (allowed c-0-1 c-0-2) (allowed c-0-2 c-0-3) (allowed c-0-3 c-0-4)
    (allowed c-1-0 c-1-1) (allowed c-1-1 c-1-2) (allowed c-1-3 c-1-4)
    (allowed c-2-0 c-2-1)
    (allowed c-3-0 c-3-1) (allowed c-3-1 c-3-2) (allowed c-3-2 c-3-3) (allowed c-3-3 c-3-4)
    (allowed c-4-2 c-4-3)

    (allowed c-0-2 c-0-1) (allowed c-0-3 c-0-2) (allowed c-0-4 c-0-3)
    (allowed c-1-1 c-1-0) (allowed c-1-2 c-1-1) (allowed c-1-4 c-1-3)
    (allowed c-2-1 c-2-0)
    (allowed c-3-1 c-3-0) (allowed c-3-2 c-3-1) (allowed c-3-3 c-3-2) (allowed c-3-4 c-3-3)
    (allowed c-4-3 c-4-2)

    ;; Vertical allowed moves
    (allowed c-0-0 c-1-0) (allowed c-1-0 c-2-0) (allowed c-2-0 c-3-0) (allowed c-3-0 c-4-0)
    (allowed c-0-1 c-1-1) (allowed c-3-1 c-4-1)
    (allowed c-1-2 c-2-2) (allowed c-3-2 c-4-2)
    (allowed c-1-3 c-2-3) (allowed c-2-3 c-3-3)
    (allowed c-0-4 c-1-4) (allowed c-1-4 c-2-4) (allowed c-3-4 c-4-4)

    (allowed c-1-0 c-0-0) (allowed c-2-0 c-1-0) (allowed c-3-0 c-2-0) (allowed c-4-0 c-3-0)
    (allowed c-1-1 c-0-1) (allowed c-4-1 c-3-1)
    (allowed c-2-2 c-1-2) (allowed c-4-2 c-3-2)
    (allowed c-2-3 c-1-3) (allowed c-3-3 c-2-3)
    (allowed c-1-4 c-0-4) (allowed c-2-4 c-1-4) (allowed c-4-4 c-3-4)

    ;; Initial robot position
    (at X c-0-0) (at Y c-4-0))

  (:goal
    (and (at X c-2-4) (at Y c-4-3))
  )
)
