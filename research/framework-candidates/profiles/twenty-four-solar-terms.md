# Twenty-Four Solar Terms candidate profile

Status: profile-ready / research-only / regional-ecological-context-sensitive

## Identity

- names: 二十四節気, Twenty-Four Solar Terms, 二十四節氣
- current scope: the Chinese solar-term system as an annual set of 24 named solar-position markers and associated living temporal practices
- intended CSW use: fine-grained annual phase segmentation, recurring phase boundaries, and separation of inherited timing from observed target conditions
- not intended use: universal climate prediction, agricultural prescription, or transferring Chinese phenological meanings to unrelated targets

## Source basis

### Living-heritage institutional source

UNESCO Intangible Cultural Heritage, “The Twenty-Four Solar Terms”

https://ich.unesco.org/en/RL/the-twenty-four-solar-terms-knowledge-in-china-of-time-and-practices-developed-through-observation-of-the-sun-s-annual-motion-00647

UNESCO documents the system as knowledge and practices developed through observation of the Sun's annual motion and maintained through living cultural practice.

### Astronomical institutional source

Hong Kong Observatory, “The 24 Solar Terms”

https://www.hko.gov.hk/en/gts/time/24solarterms.htm

The HKO describes the ecliptic as 360 degrees and the 24 solar terms as positions separated by 15 degrees of solar longitude. This provides an astronomical phase anchor without treating the cultural names as universal climate states.

### Independent scholarly context

Scientific Reports, “Analysis of geographical origin of solar terms based on the STTMD method” (2024)

https://www.nature.com/articles/s41598-024-73740-x

The study examines geographical/climatic origin and regional adaptation. CSW uses it to keep the historical Yellow River-region context and later spatial variation visible.

## Structural core

The reusable structure is not “there are 24 seasons.”

It is:

- one recurring annual solar cycle;
- a fine-grained sequence of named phase markers;
- explicit boundaries between adjacent annual phases;
- practices that may be scheduled relative to recurring phase position;
- a distinction between inherited/calendar timing and actual local conditions.

The astronomical phase marker is more stable than any specific phenological meaning attached to it in one region.

## Native operation candidates

### annual-phase

Locate a target observation within a recurring annual cycle without reducing the year to four coarse seasons.

### fine-grained-cycle-segmentation

Ask whether a coarse quarter/season grouping hides repeatable transition structure.

### phase-boundary

Inspect observations just before, at, and just after a recurring marker.

### seasonal-transition

Ask whether change is concentrated around a phase boundary rather than spread uniformly across a whole season.

### practice-timing

Separate “we act at this inherited/nominal time” from “target conditions currently justify this action.”

### local-condition-return

After using a recurring marker, return to local target observations instead of treating the marker's traditional name as evidence.

## Target-return questions

- Is a four-season or quarterly view hiding a repeatable transition?
- Which variables change before, at, or after the recurring annual marker?
- Does the target respond to solar/annual phase, to local environmental conditions, or to an institutional calendar?
- Is an inherited timing rule still supported by current local observations?
- Does the same nominal phase behave differently across locations?
- If the Chinese solar-term name is removed, does the annual phase boundary remain useful?

## Near-neighbor differentiation

### Twenty-Four Solar Terms vs Maya calendars

Maya calendar systems in CSW emphasize coupled cycles, recurrence distance, and long-count coordinates.

Twenty-Four Solar Terms emphasize fine-grained position within one annual solar cycle and the relation between recurring marker and local practice.

### Twenty-Four Solar Terms vs generic 24-bin partition

The framework is not useful if it merely divides a year into 24 equal analysis bins. The target-return operation must involve recurring phase boundaries, timing, or local-condition mismatch.

### Twenty-Four Solar Terms vs Jo-Ha-Kyū

Jo-Ha-Kyū concerns tempo shape inside one process. Solar terms concern position and transition in a repeating annual cycle.

## Regional / ecological boundary

- Do not treat traditional names such as “Great Heat” or “White Dew” as universal weather observations.
- Do not assume the same ecological signal occurs at the same marker in all regions.
- Do not convert heritage practice into agronomic or climate-science authority.
- Keep modern astronomical longitude definitions distinct from historical evolution of calendrical computation.
- Do not force a target to have exactly 24 meaningful phases after de-binding.

## De-binding route

1. remove Chinese term names and traditional phenological claims from the target-facing result;
2. retain only recurring annual phase markers and observed target changes;
3. mark any proposed phase boundary as `framework_generated`;
4. compare inherited timing with local measurements or records;
5. preserve spatial variation;
6. reject the framework when the target has no meaningful annual recurrence.

## Profile-ready decision

The candidate now has living-heritage, astronomical, and scholarly source classes; explicit regional boundaries; native operations; target-return questions; de-binding; and positive/negative examples.

It remains outside runtime until repeated target use shows that 24-term-inspired phase probing adds enough beyond generic annual seasonality analysis.

Worked examples:

- `research/framework-candidates/worked-examples/twenty-four-solar-terms.md`
- `research/framework-candidates/worked-examples/twenty-four-solar-terms-negative.md`
