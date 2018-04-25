; It looks like this:
;
; X|. . x
; .|Y . .
; .|. . .
; . . . y

(define (problem maze1)
  (:domain maze)
  (:objects c-0-0 c-0-1 c-0-2 c-0-3
            c-1-0 c-1-1 c-1-2 c-1-3
            c-2-0 c-2-1 c-2-2 c-2-3
            c-3-0 c-3-1 c-3-2 c-3-3 - cell
            X Y - robot)
  (:init
    ;; Horizontal allowed moves
    (allowed c-0-1 c-0-2) (allowed c-0-2 c-0-3)
    (allowed c-1-1 c-1-2) (allowed c-1-2 c-1-3)
    (allowed c-2-1 c-2-2) (allowed c-2-2 c-2-3)
    (allowed c-3-0 c-3-1) (allowed c-3-1 c-3-2) (allowed c-3-2 c-3-3)

    (allowed c-0-2 c-0-1) (allowed c-0-3 c-0-2)
    (allowed c-1-2 c-1-1) (allowed c-1-3 c-1-2)
    (allowed c-2-2 c-2-1) (allowed c-2-3 c-2-2)
    (allowed c-3-1 c-3-0) (allowed c-3-2 c-3-1) (allowed c-3-3 c-3-2)

    ;; Vertical allowed moves
    (allowed c-0-0 c-1-0) (allowed c-1-0 c-2-0) (allowed c-2-0 c-3-0)
    (allowed c-0-1 c-1-1) (allowed c-1-1 c-2-1) (allowed c-2-1 c-3-1)
    (allowed c-0-2 c-1-2) (allowed c-1-2 c-2-2) (allowed c-2-2 c-3-2)
    (allowed c-0-3 c-1-3) (allowed c-1-3 c-2-3) (allowed c-2-3 c-3-3)

    (allowed c-1-0 c-0-0) (allowed c-2-0 c-1-0) (allowed c-3-0 c-2-0)
    (allowed c-1-1 c-0-1) (allowed c-2-1 c-1-1) (allowed c-3-1 c-2-1)
    (allowed c-1-2 c-0-2) (allowed c-2-2 c-1-2) (allowed c-3-2 c-2-2)
    (allowed c-1-3 c-0-3) (allowed c-2-3 c-1-3) (allowed c-3-3 c-2-3)

    ;; Initial robot position
    (at X c-0-0) (at Y c-1-1))

  (:goal
    (and (at X c-0-3) (at Y c-3-3))
  )
)
