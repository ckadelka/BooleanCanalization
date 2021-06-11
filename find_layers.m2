----------------------------------------
-- Code for Finding Canalizing Layers for Boolean Polynomials
-- Authors: David Murrugarra and Brandilyn Stigler
-- Date: June 10, 2021
----------------------------------------

----------------------------------------
-- Output Structure
----------------------------------------
-- The output is an ordered pair (canalization structure, core function) where 
-- + canalization structure is a list of ordered pairs of layers (list) and canalized outputs (integer) of the form
--	{(layer 1, output 1),..., (layer k, output k)} 
--	and each layer is a list of variables and their canalizing inputs of the form 
--	{var 1 => input 1, var 2 => input 2,..., var m => input m}
-- + core function is defined in the paper by Dimitrova, Kadelka, Murrugarra, Stigler (2021)
----------------------------------------

----------------------------------------
-- Iterative method: one variable at a time
----------------------------------------

findLayersI = method()

----------------------------------------
--version with constant input
----------------------------------------

findLayersI(ZZ) := (f) -> (return ({}, f))


----------------------------------------
--version with polynomial input
----------------------------------------

findLayersI(RingElement) := (f) -> (

	if #support(f) == 0 then return ({}, f)   --constant is from the ring
	else if #support(f) == 1 then return ({ ({first support(f)=>0}, sub(f, first support(f)=>0)) }, sub(f, first support(f)=>1) )
	else 
	(
		Layers := {};				-- stores all layers  
		Can := {};				-- stores the canalizing variables with their canalizing inputs 
		NonCan := {};				-- stores the canalizing variables with their noncanalizing inputs 
		NewVar := support(f);
		Newf := f;				-- temp poly used for interim evaluation

		V := {0_(ring f), 1_(ring f)};

		while #NewVar>0 do 
		(
			k := #NewVar;
			NewLayer := {};			-- stores the current layer
			NewCan := {};			-- stores the canalizing variables (and canalizing inputs) in the current layer
    
			for i from 0 to k-1 do		-- k-1 = #NewVar-1
			(
				for j from 0 to 1 do	--   1 = #V-1
				(
					S := {NewVar_i=>V_j};
					if (#support(sub(Newf,S))==0) then	-- we have found new canalizing variables
					(
						NewLayer = append(NewLayer,NewVar_i);
						NewCan = append(NewCan,S);
						NonCan = append(NonCan,{NewVar_i=>V_j+1});
					);
				);
			);

			if #NewLayer == 0 then return (Can, Newf)
			else 
			(
				Layers = append(Layers,NewLayer);
				Can = append(Can, (flatten NewCan, sub(Newf,flatten NewCan)));
				NonCan = flatten(NonCan);
				NewVar = NewVar-set(NewLayer);
				Newf = sub(Newf,NonCan);	-- core function
			);
		);	--end while
		return (Can, Newf)
	);	--end else where #support(f)>1
);	--end method


----------------------------------------
--version with string for input file containing polynomials
--and string for output file for results
----------------------------------------

findLayersI(String, String) := (infile, outfile) -> (

	ps := lines get infile;
	--ps = apply(ps, s -> separateRegexp("[ ]+",s));	--old way to separate by spaces
	ps = apply(ps, s -> separate("\t",s));			--new way to separate by tabs
	ps = apply(ps, l -> {l_0, l_1, value l_2});
	cs := apply(ps, l -> {l_0, l_1, timing findLayersI(l_2)});

	--print to a file
	ofile := openOut outfile;
	ofile << "ID\tNumLayers\tDepth\tCanalizationStructure\tCpuTime\n";
	apply(cs, l-> outfile << concatenate(l_0, "\t", toString(#((last l_2)_0)), "\t", toString(#flatten apply(flatten (last l_2)_0, ll->first ll)), "\t", toString (last l_2), "\t", toString (first l_2), "\n"));
	ofile << close;
);


----------------------------------------
--version with string for input file containing polynomials
--output struct is a list of lists for each polynomial in the input file: 
-- {id, #layers, depth, canalization structure (see top of file for a description), CPUtime}
----------------------------------------

findLayersI(String) := (infile) -> (

	ps := lines get infile;
	--ps = apply(ps, s -> separateRegexp("[ ]+",s));	--old way to separate by spaces
	ps = apply(ps, s -> separate("\t",s));			--new way to separate by tabs
	ps = apply(ps, l -> {l_0, l_1, value l_2});
	cs := apply(ps, l -> {l_0, l_1, timing findLayersI(l_2)});

	return apply(cs, l-> {l_0, #((last l_2)_0), #flatten apply(flatten (last l_2)_0, ll->first ll), last l_2, first l_2});
);

-----------------
-- Recursive method: finds groups of canalizing variables recursively
-----------------

findLayersR = method()


----------------------------------------
--version with constant input
----------------------------------------

findLayersR(ZZ) := (f) -> (return ({}, f))

-----------------
-- version to be used at onset
-----------------

findLayersR(RingElement) := (f) -> (

	if #support(f) == 0 then return ({}, f)  --constant is from the ring
	else if #support(f) == 1 then return ({ ({first support(f)=>0}, sub(f, first support(f)=>0)) }, sub(f, first support(f)=>1) )
	else return (findLayersR(f, {}));
);

-----------------
-- recursive version
-----------------
findLayersR(RingElement, List) := (f, S) -> (

--assuming f has at least 2 vars in its support

	L = {};	--current layer
	Y = {}; --intersection of monomials before bitflipping
	Z = {}; --intersection of monomials after bitflipping

	Newf = f;		--this one is used inside the method (to not modify the original input)
	cout = "infinity";	--cout=canalized output, initialized to oo

	-----------------------------
	--can input = 0
	-----------------------------
	j = 0;

	M = (flatten entries (monomials Newf))/support;
	--removing constant term
	M = select(M, s->s!={});	
	M = sort (M/set);
	
	if #M == 1 then Y = first M 
	else 
	(
		Y = M_0*M_1;
		apply(#M-2, i->if #Y==0 then (Y) else (Y = Y*M_(i+2)));
	);
	
	if #(elements Y) > 0 then 
	(
		NewLayer = {};
		NonCan = {};
		apply(elements Y, x->
		(
			NewLayer = append(NewLayer, {x => j_(ring f)}); 
			NonCan = append(NonCan, {x => (j+1)_(ring f)});
		));

		L = append(L, flatten NewLayer);	
		--subbing in noncan values
		cout = sub(Newf, flatten NewLayer);
		Newf = sub(Newf, flatten NonCan);

		if #(support Newf) == 0 then 
		(
			if (#S==0) then S = append(S, (rsort flatten L, sub(f, flatten L)))
			--checking if we have switched layers by comparing the canalized outputs
			--else if (last last S == cout) then S = flatten {drop(S,-1),(flatten {first last S, rsort flatten L}, last last S)}
			else if (last last S == cout) then S = flatten {drop(S,-1),(rsort flatten {first last S, flatten L}, last last S)}
			else S = append(S, (rsort flatten L, sub(f, flatten L))); -- last layer gets added

			--return (S, 0_(ring f))  --should core function be Newf?
			return (S, Newf)
		);
		
	); -- end if statement for finding canalizing variables, #Y>0

	--bitflipping
	Newfp = sub(Newf, apply(support Newf, x-> x=>x+1));


	-----------------------------
	--can input = 1
	-----------------------------
	j = 1;

	M = (flatten entries (monomials Newfp))/support;
	--removing constant term
	M = select(M, s->s!={});	
	M = sort (M/set);

	if #M == 1 then Z = first M 
	else 
	(
		Z = M_0*M_1;
		apply(#M-2, i->if #Z==0 then (Z) else (Z = Z*M_(i+2)));
	);

	if (#(elements Y) > 0 and #(elements Z) == 0) then 
	(
		if #S==0 then S = append(S, (rsort flatten L, cout))
		--checking if we have switched layers by comparing the canalized outputs
		--else if (last last S == cout) then S = flatten{drop(S,-1),(flatten {first last S, rsort flatten L}, last last S)}
		else if (last last S == cout) then S = flatten {drop(S,-1),(rsort flatten {first last S, flatten L}, last last S)}
		else S = append(S, (rsort flatten L, cout)); 
	);

	if (#(elements Y) == 0 and #(elements Z) == 0) then return (S, Newf); 

	if #(elements Z) > 0 then 
	(
		NewLayer = {};
		NonCan = {};
		apply(elements Z, x->
		(
			NewLayer = append(NewLayer, {x => j_(ring f)}); 
			NonCan = append(NonCan, {x => (j+1)_(ring f)});
		));

		--if cout has been set to an integer and doesn't equal to the newly found canalized output (switched layers)
		if (cout=!="infinity" and cout=!=sub(Newf, flatten NewLayer))
		then 
		(
			if #S==0 then S = append(S, (rsort flatten L, cout))
			--checking if we have switched layers by comparing the canalized outputs
			--else if (last last S == cout) then S = flatten{drop(S,-1),(flatten {first last S, rsort flatten L}, last last S)}
			else if (last last S == cout) then S = flatten {drop(S,-1),(rsort flatten {first last S, flatten L}, last last S)}
			else S = append(S, (rsort flatten L, cout)); -- last layer gets added
			
			cout = sub(Newf, flatten NewLayer);
			
			if #S==0 then S = append(S, (rsort flatten NewLayer, cout))
			--checking if we have switched layers by comparing the canalized outputs
			--else if (last last S == cout) then S = flatten{drop(S,-1),(flatten {first last S, rsort flatten NewLayer}, last last S)}
			else if (last last S == cout) then S = flatten {drop(S,-1),(rsort flatten {first last S, flatten L}, last last S)}
			else S = append(S, (rsort flatten NewLayer, cout));
				
			Newf = sub(Newf, flatten NonCan);
			--if (Newf==0 or Newf==1) then return (S, 0_(ring f));  --should core function be Newf?
			if (Newf==0 or Newf==1) then return (S, Newf);  
			return findLayersR(Newf, S);
		
		)
		--cout hasn't been set or equals newly found canalized output
		else 
		(
			cout = sub(Newf, flatten NewLayer);

			L = append(L, flatten NewLayer);
			--subbing in noncan values
			cout = sub(Newf, flatten NewLayer);
			Newf = sub(Newf, flatten NonCan);--moved from line 258
		
			if #S==0 then S = append(S, (rsort flatten L, cout))
			--checking if we have switched layers by comparing the canalized outputs
			--else if (last last S == cout) then S = flatten{drop(S,-1),(flatten {first last S, rsort flatten L}, last last S)}
			else if (last last S == cout) then S = flatten {drop(S,-1),(rsort flatten {first last S, flatten L}, last last S)}
			else S = append(S, (rsort flatten L, cout));
		);

		--if #(support Newf) == 0 then return (S, 0_(ring f))  --should core function be Newf?
		if #(support Newf) == 0 then return (S, Newf)

	); -- end if statement for finding canalizing variables, #Z>0


	--if (Newf==0 or Newf==1) then return (S, 0_(ring f));  --should core function be Newf?
	if (Newf==0 or Newf==1) then return (S, Newf);
	return findLayersR(Newf, S);

); --end method



----------------------------------------
--version with string for input file containing polynomials
--and string for output file for results
----------------------------------------

findLayersR(String, String) := (infile, outfile) -> (

	ps := lines get infile;
	--ps = apply(ps, s -> separateRegexp("[ ]+",s));	--old way to separate by spaces
	ps = apply(ps, s -> separate("\t",s));			--new way to separate by tabs
	ps = apply(ps, l -> {l_0, l_1, value l_2});
	cs := apply(ps, l -> {l_0, l_1, timing findLayersR(l_2)});

	--print to a file
	ofile := openOut outfile;
	ofile << "ID\tNumLayers\tDepth\tCanalizationStructure\tCpuTime\n";
	apply(cs, l-> outfile << concatenate(l_0, "\t", toString(#((last l_2)_0)), "\t", toString(#flatten apply(flatten (last l_2)_0, ll->first ll)), "\t", toString (last l_2), "\t", toString (first l_2), "\n"));
	ofile << close;
);


----------------------------------------
--version with string for input file containing polynomials
--output struct is a list of lists for each polynomial in the input file: 
-- {id, #layers, depth, canalization structure (see top of file for a description), CPUtime}
----------------------------------------

findLayersR(String) := (infile) -> (

	ps := lines get infile;
	--ps = apply(ps, s -> separateRegexp("[ ]+",s));	--old way to separate by spaces
	ps = apply(ps, s -> separate("\t",s));			--new way to separate by tabs
	ps = apply(ps, l -> {l_0, l_1, value l_2});
	cs := apply(ps, l -> {l_0, l_1, timing findLayersR(l_2)});

	return apply(cs, l-> {l_0, #((last l_2)_0), #flatten apply(flatten (last l_2)_0, ll->first ll), last l_2, first l_2});
);


end 

--end of loaded code


