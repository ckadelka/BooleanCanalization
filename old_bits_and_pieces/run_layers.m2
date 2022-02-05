----------------------------
-- Code for Running Examples in Macaulay2
----------------------------

load "find_layers.m2"


-----------
-- examples
-----------

makeVars = method(TypicalValue => List);
makeVars(ZZ) := (n) -> apply(1..n, i -> value ("x"|i));

--variables
n = 7;
V = makeVars n;

--rings
S = ZZ/2[V];
I = ideal apply(gens S, x->x^2-x);
Q = S/I;

--polynomials

-- NCF (n=7)
f = (x1+1)*x2*((x3+1)*x4*(x5*x6+x7+1)+1)

-- polynomial with one layer and a core polynomial
g = (x1*x2 + x1 + x2+1)*(x3+x4)

-- nonNCF polynomial
h = x1*x2*x3 + x2*x3*x4 + x2*x3 + x1

--uncomment or run the appropriate line
--findLayersI(f)  --applying method to the poly f
--findLayersI(g)  --applying method to the poly g
--findLayersI(h)  --applying method to the poly h

--uncomment or run the appropriate line
--findLayersR(f)  --applying method to the poly f
--findLayersR(g)  --applying method to the poly g
--findLayersR(h)  --applying method to the poly h


end
