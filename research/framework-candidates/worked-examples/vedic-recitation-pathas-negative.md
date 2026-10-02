# Vedic recitation pathas negative example

Status: negative example / profile-readiness support

A metadata record contains an unordered set of independent tags:

- archived;
- public;
- imported;
- reviewed.

The target specification explicitly says tag order has no meaning.

Creating overlapping pairs such as:

- archived / public;
- public / imported;
- imported / reviewed;

would invent adjacency that the target does not possess.

The correct CSW result is to reject the Vedic-recitation-inspired pass.

If the actual requirement is only to detect file corruption during transport, use a checksum or signature rather than adding human-readable recitation views.

Sequence-preservation operations are useful only when the target itself gives order, boundary, or local transition semantic or operational importance.
