"""labx.py - code to generate Mathematics Python Labs home assignments
2025, Sakari Lukkarinen
School of ICT
Metropolia University of Applied Sciences
"""
import numpy as np
import time

def generate_polynomial(seed = 0, order = 2):
    if seed == 0:
        seed = time.time_ns()
    rng = np.random.default_rng(seed)
    roots = rng.random(order)*15 - 7.5  # Generate two random roots
    p = np.round(np.poly(roots), 4)  # Get coefficients of the polynomial
    return p

def lab_1_problem_1(x, seed = 0):
    p = generate_polynomial(seed, 2)
    return np.polyval(p, x)

def lab_1_problem_3(x, seed = 0):
    p = generate_polynomial(seed, 3)
    return np.polyval(p, x)

def lab_2_problem_1(x, seed = 0):
    p = generate_polynomial(seed, 4)
    return np.polyval(p, x)

def lab_2_problem_2(seed = 0):
    if seed == 0:
        seed = time.time_ns()
    rng = np.random.default_rng(seed)
    k = rng.integers(20, 50).item()/10.0
    c = rng.integers(200, 700).item()/100.0

    md_txt = r"""
In this problem your task is to plot two functions and
graphically find the intersection points of the two functions.

The first functions is $$ f(x) = \sqrt{""" + f"{k:.1f}" + r"""x} $$ and 
the second function is $$ g(x) = (x - """ + f"{c:.2f}" + r""")^2 $$.
    
First, plot the two functions in the same graph. Make this first plot to show the functions in the 
larger range of $x$ values, say $x \in [0, 10]$.

Then plot the two functions in another graph, but now show the functions in the smaller range of 
$x$ values. In this second plot, make sure to show the intersection points of the two functions.
What are their values? Find the values *graphically*.

Finally, remember to decorate the plots with title, axis labels, and a legend. Add also grid
lines to the plots to make them easier to read."""

    return md_txt 

def lab_3_problem_1(seed = 0):
    if seed == 0:
        seed = time.time_ns()
    rng = np.random.default_rng(seed + 123)
    x0 = rng.integers(-20, 10).item()/10.0
    w = rng.integers(2, 5).item()

    txt = f"""
In this problem your task is to create and plot a piecwise
continuous function in range $ x \\in [-10, 10] $.

The function is defined as:<br>

$$ f(x)  = \\begin{{cases}} 
0 & x < {x0:.1f}  \\\\ 
{-x0:.1f} + x & {x0:.1f} \\leq x < {x0+w:.1f} \\\\
{x0+2*w:.1f} - x & {x0+w:.1f} \\leq x < {x0+2*w:.1f} \\\\ 
0 & x \\geq {x0+2*w:.1f} 
\\end{{cases}} $$

Draw the function within the given range of x.

Remember to decorate the plots with title, axis labels, and a legend. Add also grid
lines to the plots to make them easier to read."""

    return txt 

def lab_3_problem_2(seed = 0):
    if seed == 0:
        seed = time.time_ns()
    p = generate_polynomial(seed + 10000, 3)
    p = np.round(p, 2)
    rng = np.random.default_rng(seed + 10000)
    x0 = rng.integers(-80, -40).item()/10.0
    x1 = rng.integers(40, 80).item()/10.0
    y0 = np.polyval(p, x0)
    y1 = np.polyval(p, x1)  

    txt = f"""
In this problem your task is to create and plot a piecwise
continuous function in range $ x \\in [-10, 10] $.

The function is defined as:<br>

$$ f(x)  = \\begin{{cases}} 
{y0:.2f} & x < {x0}  \\\\ 
{p[0]}x^3 + {p[1]}x^2 + {p[2]}x + {p[3]} & {x0} \\leq x < {x1} \\\\
{y1:.2f} & x \\geq {x1} 
\\end{{cases}} $$

Draw the function within the given range of x.

Remember to decorate the plots with title, axis labels, and a legend. Add also grid
lines to the plots to make them easier to read."""

    return txt 
