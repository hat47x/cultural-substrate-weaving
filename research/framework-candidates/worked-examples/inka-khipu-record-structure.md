# Inka khipu record-structure target-return example

Status: hypothetical / profile-readiness support

A team is digitizing a legacy maintenance board.

Each paper tag has:

- a handwritten quantity;
- a position under one of several rails;
- a colored edge;
- one or more smaller tags clipped beneath it;
- occasional blank positions left between groups.

The initial digitization plan stores only the handwritten text in a CSV.

A khipu-inspired pass does not claim the board is culturally equivalent to a khipu. It asks which information channels would disappear through flattening.

Target-return questions include:

- Does rail position classify the tag independently of its written value?
- Do clipped child tags belong to the parent tag or only happen to be nearby?
- Is color documented as a status code, or is its meaning unknown?
- Are blank positions meaningful separators, or merely unused space?
- Which relationships need explicit fields in the digital model before the physical layout is discarded?

If the team knows that color matters but no surviving documentation explains how, the correct result is to preserve the observed color value and mark its semantics unresolved rather than inventing a code.

The useful output is a loss-aware digitization model that separates known meaning, structural relation, and unresolved channel.
