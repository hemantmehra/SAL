# SAL
A simple programming language to implement rule 110.
SAL - Statement as List

https://en.wikipedia.org/wiki/Rule_110

Each statement is an S-Expression.
https://en.wikipedia.org/wiki/S-expression

Below is the example of a program in SAL with two function main and test.
```lisp
(def test (a b))
    (return (+ a b))
(end test)

(def main)
    (set a 3)
    (label loop1)
        (println a)
        (dec a)
    (jmp_g loop1 a  0)
    (println 'a')
    (return (test 100 201))
(end main)
```
## Rule 110

- Rule 110 is implemented in https://github.com/hemantmehra/SAL/blob/main/rule110.lsp
- Output of 256 iterations are in https://github.com/hemantmehra/SAL/blob/main/rule110-out.txt
