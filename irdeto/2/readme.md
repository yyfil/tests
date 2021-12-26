**Task:**

You are given a function f(x), x in R, delta(x) = 1/128.
Please write a code (a function in C or Python) which takes x as an argument and returns f(x). Write unit tests with cunit in case of C or pytest if Python. 
```
f(x) = -x^2, x==[-10..-2]
f(x) = (1-x)/(1+x), x==(-2..8), x!=-1
f(x) = abs(x-12), x==(8..35]
```

**Howto:**
```
pip3 install -r ../requirements.txt
pytest test_math_fuction.py
```