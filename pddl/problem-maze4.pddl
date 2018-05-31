; 6
; 7
; It looks like this:
;      0   1   2   3   4   5
;    .___.___.___.___.___.___.
;    | Y |               | a | 0
;    |   |___.   .   .___|   |
;    |       |               | 1
;    |___.   |   .   .   .___|
;    |           |           | 2
;    |   .___.   |   .___.   |
;    |       |   |           | 3
;    |   .   |   |___.   .   |
;    |       |       |       | 4
;    |   .   |___.___|   .___|
;    |           |           | 5
;    |___.___.   |   .   .   |
;    |           |       |   | 6
;    |_X_.___.___|___.___|_b_|


(define (problem maze1)
  (:domain maze)
  (:objects c-0-0 c-0-1 c-0-2 c-0-3 c-0-4 c-0-5
            c-1-0 c-1-1 c-1-2 c-1-3 c-1-4 c-1-5
            c-2-0 c-2-1 c-2-2 c-2-3 c-2-4 c-2-5
            c-3-0 c-3-1 c-3-2 c-3-3 c-3-4 c-3-5
            c-4-0 c-4-1 c-4-2 c-4-3 c-4-4 c-4-5
            c-5-0 c-5-1 c-5-2 c-5-3 c-5-4 c-5-5
            c-6-0 c-6-1 c-6-2 c-6-3 c-6-4 c-6-5 - cell
            X Y - robot)
  (:init
    ;; Horizontal allowed moves
    (allowed c-0-1 c-0-2) (allowed c-0-2 c-0-3) (allowed c-0-3 c-0-4)
    (allowed c-1-0 c-1-1) (allowed c-1-2 c-1-3) (allowed c-1-3 c-1-4) (allowed c-1-4 c-1-5)
    (allowed c-2-0 c-2-1) (allowed c-2-1 c-2-2) (allowed c-2-3 c-2-4) (allowed c-2-4 c-2-5)
    (allowed c-3-0 c-3-1) (allowed c-3-3 c-3-4) (allowed c-3-4 c-3-5)
    (allowed c-4-0 c-4-1) (allowed c-4-2 c-4-3) (allowed c-4-4 c-4-5)
    (allowed c-5-0 c-5-1) (allowed c-5-1 c-5-2) (allowed c-5-3 c-5-4) (allowed c-5-4 c-5-5)
    (allowed c-6-0 c-6-1) (allowed c-6-1 c-6-2) (allowed c-6-3 c-6-4)

    (allowed c-0-2 c-0-1) (allowed c-0-3 c-0-2) (allowed c-0-4 c-0-3)
    (allowed c-1-1 c-1-0) (allowed c-1-3 c-1-2) (allowed c-1-4 c-1-3) (allowed c-1-5 c-1-4)
    (allowed c-2-1 c-2-0) (allowed c-2-2 c-2-1) (allowed c-2-4 c-2-3) (allowed c-2-5 c-2-4)
    (allowed c-3-1 c-3-0) (allowed c-3-4 c-3-3) (allowed c-3-5 c-3-4)
    (allowed c-4-1 c-4-0) (allowed c-4-3 c-4-2) (allowed c-4-5 c-4-4)
    (allowed c-5-1 c-5-0) (allowed c-5-2 c-5-1) (allowed c-5-4 c-5-3) (allowed c-5-5 c-5-4)
    (allowed c-6-1 c-6-0) (allowed c-6-2 c-6-1) (allowed c-6-4 c-6-3)


    ;; Vertical allowed moves
    (allowed c-0-0 c-1-0) (allowed c-2-0 c-3-0) (allowed c-3-0 c-4-0) (allowed c-4-0 c-5-0)
    (allowed c-1-1 c-2-1) (allowed c-3-1 c-4-1) (allowed c-4-1 c-5-1)
    (allowed c-0-2 c-1-2) (allowed c-1-2 c-2-2) (allowed c-2-2 c-3-2) (allowed c-3-2 c-4-2) (allowed c-5-2 c-6-2)
    (allowed c-0-3 c-1-3) (allowed c-1-3 c-2-3) (allowed c-2-3 c-3-3) (allowed c-5-3 c-6-3)
    (allowed c-1-4 c-2-4) (allowed c-3-4 c-4-4) (allowed c-4-4 c-5-4) (allowed c-5-4 c-6-4)
    (allowed c-0-5 c-1-5) (allowed c-2-5 c-3-5) (allowed c-3-5 c-4-5) (allowed c-5-5 c-6-5)

    (allowed c-1-0 c-0-0) (allowed c-3-0 c-2-0) (allowed c-4-0 c-3-0) (allowed c-5-0 c-4-0)
    (allowed c-2-1 c-1-1) (allowed c-4-1 c-3-1) (allowed c-5-1 c-4-1)
    (allowed c-1-2 c-0-2) (allowed c-2-2 c-1-2) (allowed c-3-2 c-2-2) (allowed c-4-2 c-3-2) (allowed c-6-2 c-5-2)
    (allowed c-1-3 c-0-3) (allowed c-2-3 c-1-3) (allowed c-3-3 c-2-3) (allowed c-6-3 c-5-3)
    (allowed c-2-4 c-1-4) (allowed c-4-4 c-3-4) (allowed c-5-4 c-4-4) (allowed c-6-4 c-5-4)
    (allowed c-1-5 c-0-5) (allowed c-3-5 c-2-5) (allowed c-4-5 c-3-5) (allowed c-6-5 c-5-5)

    ;; Initial robot position
    (at X c-6-0) (at Y c-0-0))

  (:goal
    (and (at X c-0-5) (at Y c-6-5))
  )
)
