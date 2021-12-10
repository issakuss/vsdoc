# How to use inlini
The inline allows you embed variables in your manuscript.
You can convert value ("var") with python code written after "!!".
Though you can't include "{" and "}", you can use some functions pval() and dround().
Don't use space also.

Now we can use csv instead of ini.

## Example
We used the %{method:stats.test}.
%{result:subject.n} participated the experiment.
The significant result was found (t = %{result:ttest.t}; p = %{result:ttest.p}).

The correlation in condition A was siginificant (p %{result:pearson.p1!!pval(var,0.001)})
The correlation in condition B was siginificant (p %{result:pearson.p2!!dround(var,2)})
The correlation in condition B was siginificant (p %{result:pearson.p2!!pval(dround(var,2),0.001)})

t = %{table:1.1} (p %{table:1.2!!pval(var,0.001)})
