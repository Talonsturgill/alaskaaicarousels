# Review record, run 2026-08-12 (carousel No.31)

Round 1 covered slides 01-08 in four parallel pixel-critics. Slide 09 was
reviewed in the same round but its report was consumed inline while the slide
was being rebuilt and was never written to disk. That gap is recorded here
rather than papered over: its two hard fails were the absent scale rail and the
absent August 11 rail, and its verdict was revise at 5.0.

Round 2 re-reviewed all nine after the rebuild, in three critics plus a flow
critic on the sequence. A third fix pass landed AFTER those round-2 numbers
were written, so several defects they score are no longer on the frame.

| file | covers | scores |
| --- | --- | --- |
| r1-pixel-01-02.json | round 1, slides 01 and 02 | 6.0, 5.0 |
| r1-pixel-03-04.json | round 1, slides 03 and 04 | 5.5, 6.0 |
| r1-pixel-05-06.json | round 1, slides 05 and 06 | 5.0, 6.5 |
| r1-pixel-07-08.json | round 1, slides 07 and 08 | 5.5, 2.5 |
| (slide 09, round 1)  | not persisted, see above | 5.0 |
| r2-pixel-01-02.json | round 2, slides 01 and 02 | 5.5, 6.0 |
| r2-pixel-03-04.json | round 2, slides 03 and 04 | 5.0, 4.5 |
| r2-pixel-05-06.json | round 2, slides 05 and 06 | 6.0, 5.0 |
| r2-pixel-07-08-09.json | round 2, slides 07, 08 and 09 | 7.0, 6.5, 7.5 |
| flow-critic.json | the deck as a sequence | 6.0 |
| scorer.json | the finished package against the rubric | 8.42 |
