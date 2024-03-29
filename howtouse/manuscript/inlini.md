# How to use inlini
The inline allows you embed variables in your manuscript.
You can convert value ("var") with python code written after "!!".
Though you can't include "{" and "}", you can use some functions int2spell(), pval() and dround().
Don't use space also.

Now we can use csv instead of ini.

## Example
We used the %{method:stats.test}.
%{result:subject.n} participated the experiment.
Among them, %{result:subject.n_rm!!int2spell(var)} subjects were rejected.
%{result:subject.n_rm!!int2Spell(var)} subjects were rejected (said again).
The significant result was found (t = %{result:ttest.t}; p = %{result:ttest.p}).
The mean was %{result:mean.v} (%{result:mean.ci_low}--%{result:mean.ci_high}).

The correlation in condition A was siginificant (p %{result:pearson.p1!!pval(var,0.001)})
The correlation in condition B was not siginificant (p = %{result:pearson.p2!!dround(var,2)})
The correlation in condition B was not siginificant (p %{result:pearson.p2!!pval(dround(var,2),0.001)})

Var B was not significant(t = %{table:C.2} (p %{table:C.3!!pval(var,0.001)}))
The row number starts with 1.
The column code starts with A.
Type as you see in Excel.
