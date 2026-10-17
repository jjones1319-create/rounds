---
description: Write the next block of 8 board questions (verified against current guidelines), add them to the app, and publish
---

Write the next question block: 8 new questions for the question bank, then publish them.
If arguments were given ($ARGUMENTS), treat them as topic or system preferences for this block.

1. Read CLAUDE.md and all of docs/board_question_generator_spec.md before doing anything.
   The new block number is one more than the highest block in questions/ (Block N), skipping any block
   reserved in docs/PEDS_BLUEPRINT.md (Blocks 4–8 belong to the pediatrics track and are written only with
   /peds-pair); so the next general block is Block 9 until the pediatric blocks are done. IDs are BN-Q01 to BN-Q08.
2. Pick 8 topics from the coverage gaps in spec §7. Don't repeat any topic in the §9 log.
   Show me the 8 topics with planned difficulty, answer letter, and the guideline you'll
   verify each against. Wait for my OK.
3. For each question, search the web for the current guideline and verify the answer
   before writing. Follow spec §2–§6 exactly: one defensible best answer, checked math,
   every distractor tied to a specific error, full explanation format, real citations.
   Never answer from memory alone.
4. Then review each question again as a skeptical reviewer, re-checking every factual
   claim against its source. Fix anything wrong. List anything you couldn't verify.
5. Save them as questions/questionsN.py with IDs BN-Q01 to BN-Q08, in the same format as
   the previous block's file. Import them in build.py and add each ID to SYS.
6. Update spec §7 (coverage), §9 (log), and §11 (changelog).
7. Run python build.py, python tests/smoke.py, and python tests/overflow.py. Fix any failures.
8. Show me a summary (topic, answer, difficulty, source for each) and wait for my OK.
9. Then commit with a clear message, push to main, and tell me when the live site shows
   the new question total.
