## Task:

You are given piece of DASH manifest which represents one Period, please write a test that confirm/disprove validity of the period. Explain why this period is valid or invalid.


## Explanation:

I assume that this period is invalid as SegmentTemplate should be nested within Representation element:

**Representation**: A Representation describes an audio, video, or captions track. There are one or more Representations in each AdaptationSet. Each representation is a track.

**SegmentTemplate**: A SegmentTemplate defines properties of the representation, such as the timescale and access URLs for media and initialization segments. There is one SegmentTemplate for each Representation.

**Source:** https://docs.aws.amazon.com/mediapackage/latest/ug/dash-trtmts.html

**Autotest:**

```pytest test_manifest.py```