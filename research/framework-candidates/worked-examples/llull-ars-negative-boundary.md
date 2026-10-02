# Llull Ars negative boundary example

Status: negative example / runtime adoption support

Suppose a target contains three labels that are not independent dimensions:

- "administrator";
- "administrator-only action";
- "anonymous user".

A blind combinatorial pass can generate "anonymous user × administrator-only action" and then present its absence as a gap.

That is not a valid CSW result.

The target definition already makes the combination impossible. The correct sequence is:

1. generate the combination as `framework_generated`;
2. return it to target constraints;
3. reject it as structurally impossible;
4. do not turn the empty cell into evidence of a missing case.

This negative case is important because the value of the Ars is systematic crossing, not maximization of the number of combinations.
