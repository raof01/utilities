#lang racket

(require plot)
(require csv-reading)

(define (csv->number-list input-file)
  (map (λ (x) (string->number x))
       (flatten (csv->list (make-csv-reader
                            (open-input-file input-file))))))

(define (build-day-list n)
  (build-list n add1))

(define (list-min lst)
  (foldr (λ (x y) (if (< x y) x y)) 9999999 lst))

(define (list-max lst)
  (foldr (λ (x y) (if (> x y) x y)) 0 lst))

(define weight-all-avgs
  (csv->number-list "./avgs.csv"))

(define weight-periodic-avgs
  (csv->number-list "./periodical-avg.csv"))

(define weight-interpolated
  (csv->number-list "./interpolated.csv"))

(define height-all-avgs
  (csv->number-list "./height-avgs.csv"))

(define height-periodic-avgs
  (csv->number-list "./height-periodical-avg.csv"))

(define height-interpolated
  (csv->number-list "./height-interpolated.csv"))

(define weight-avg-min-half
  (/ (list-min weight-periodic-avgs) 2))

(define height-avg-min-half
  (/ (list-min height-periodic-avgs) 2))

(let* ([weight-avg-y-min weight-avg-min-half]
       [weight-avg-y-max (+ (list-max weight-periodic-avgs) weight-avg-min-half)]
       [weight-all-avg (car weight-all-avgs)])
  (plot
   (list (tick-grid)
         (lines (map vector (build-day-list (length weight-periodic-avgs)) weight-periodic-avgs)
                #:label "阶段性日均" #:color 'indigo #:width 1.5)
         (hrule weight-all-avg
                #:label (format "总体日均 ~a" (real->decimal-string weight-all-avg))
                #:color 'teal #:style 'long-dash #:width 1.5))
   #:legend-anchor 'top-right
   #:x-label "天数" #:y-label "体重增长值（克）" #:y-min weight-avg-y-min #:y-max weight-avg-y-max))

(let* ([weight-min (list-min weight-interpolated)]
       [weight-max (list-max weight-interpolated)]
       [weight-delta (- weight-max weight-min)]
       [weight-y-max (+ weight-max (* 20 weight-avg-min-half))])
  (plot
   (list (tick-grid)
         (lines (map vector (build-day-list (length weight-interpolated)) weight-interpolated)
                #:color 'indigo #:width 1.5
                #:label (format "出生:~a,目前:~a,增长:~a" weight-min weight-max weight-delta)))
   #:legend-anchor 'bottom-right
   #:x-label "天数" #:y-label "体重（克）" #:y-min 0 #:y-max weight-y-max))

(let* ([height-avg-y-min height-avg-min-half]
       [height-avg-y-max (+ (list-max height-periodic-avgs) height-avg-min-half)]
       [height-all-avg (car height-all-avgs)])
  (plot
   (list (tick-grid)
         (lines (map vector (build-day-list (length height-periodic-avgs)) height-periodic-avgs)
                #:label "阶段性日均" #:color 'black #:width 1.5)
         (hrule height-all-avg
                #:label (format "总体日均：~a" (real->decimal-string height-all-avg))
                #:color 'teal #:style 'long-dash #:width 1.5))
   #:legend-anchor 'top-right
   #:x-label "天数" #:y-label "身高增长值（厘米）" #:y-min height-avg-y-min #:y-max height-avg-y-max))

(let* ([height-min (list-min height-interpolated)]
       [height-max (list-max height-interpolated)]
       [height-delta (- height-max height-min)]
       [height-y-max (+ (list-max height-interpolated) (* 20 height-avg-min-half))])
  (plot
   (list (tick-grid)
         (lines (map vector (build-day-list (length height-interpolated)) height-interpolated)
                #:color 'black #:width 1.5
                #:label (format "出生:~a,目前:~a,增长:~a" height-min height-max height-delta)))
   #:legend-anchor 'bottom-right
   #:x-label "天数" #:y-label "身高（厘米）" #:y-min 0 #:y-max height-y-max))
