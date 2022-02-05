----------------------------
-- Code for Running the Script from the Command Line
----------------------------

--------------------------------------------------------------------
-- the following is the library with the layers code
--------------------------------------------------------------------


load "find_layers.m2"


--------------------------------------------------------------------
-- routine to build polynomial rings with variables of the form "xi"
--------------------------------------------------------------------

makeVars = method(TypicalValue => List);
makeVars(ZZ) := (n) -> apply(1..n, i -> value ("x"|i));

-----------------------
--setting up for test polys
-----------------------

--variables
n = 16;
V = makeVars n;

--rings
S = ZZ/2[V];
I = ideal apply(gens S, x->x^2-x);
Q = S/I;

-- this next line is instead run at the command line
--findLayersI("testfiles_poly_nmin4_nmax16_nstep2_real_seed0.txt", "testfiles_poly_nmin4_nmax16_nstep2_real_seed0_layers.txt")

end


