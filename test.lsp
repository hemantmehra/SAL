(def test (a b))
    (return (+ a b))
(end test)

(def main)
    (set a 3)
    (label loop)
        (println a)
        (dec a)
    (jmp_g loop a  0)
    (println 'a')
    (return (test 100 201))
(end main)
