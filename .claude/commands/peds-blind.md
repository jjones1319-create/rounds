---
description: Independent blind re-solve of the waiting pediatric pair, then compare with the key, fix or pass, and publish on my OK
---

You are the independent blind re-solver for the pediatric pair that is waiting. This must be a fresh conversation
that has not seen the pair. If your context, your loaded memory or a file the editor is sharing already shows these
questions or their answers, stop and tell me.

Part 1, blind: nothing but the blind packet, and no web search.

1. List the file names in review/ (names only). The waiting pair is the lowest NN whose review/peds_pair_NN_blind.md
   has no review/peds_pair_NN_resolve.md.
2. Until your resolve file is saved, open nothing else: not the key (review/peds_pair_NN.md), the sources or check
   files, questions/, data/, index.html, build.py, anything in docs/ (the spec and the blueprint hold the answers), or
   git log, diff or status. CLAUDE.md is already loaded and holds no answers.
3. For each question:
   a. Exam pass: read it once as a test-taker would, in about 90 seconds, and record your first answer.
   b. Expert pass: work it fully (what the findings show, the diagnosis, the decision, why each option is right or
      wrong). Record your final answer, your confidence (sure, likely or guess) and how hard it felt: ★★★ one key
      finding leads to the standard step; ★★★★ one detail flips the usual answer; ★★★★★ several steps, and the
      tempting answer would harm the child.
   c. Objections: a second defensible answer; missing or ambiguous information; an answer resting on a weak, outdated
      or contested recommendation; a cue in the options (length, wording, grammar, a repeated word, an option that
      shares the most with the others); vital signs, labs, doses, growth or development implausible for the age; a
      resemblance to a published question you know; anything a pediatric attending or an NBME reviewer would flag.
4. Save all of it to review/peds_pair_NN_resolve.md, starting with the list of files you opened (only the blind
   packet). Don't edit that file afterward.

Part 2, compare: now open the key, the sources file and the check script.

5. A question passes only if your final answer matches the key and none of your objections holds up; set a passing
   question's blueprint row to "reviewed". Any disagreement fails the question, even if the key turns out to be right:
   something misled a strong solver. Check the cited sources on the web, find the cause, and fix the item (stem,
   options, key or explanation) in questions/questionsN.py; re-run the check script, python build.py and the three
   tests; and log the fix in the blueprint changelog. Fix explanation-only errors as well. If your stars differ from
   the key's, re-rate per spec §3 unless the key's rating holds up. If an item can't be fixed cleanly, tell me, and
   we'll replace it with /peds-pair.
6. If a question failed: rename the resolve file to peds_pair_NN_resolve_1.md (then _2, and so on); regenerate
   review/peds_pair_NN.md, and review/peds_pair_NN_blind.md with only the changed questions
   (tools/board_review_packet.py); and stop with "Fixed. Start a new conversation and run /peds-blind again."
   Don't commit.
7. When both questions have passed (in this round or an earlier one): set "status": "reviewed" and "reviewed_by":
   "independent blind re-solve" on both; update spec §7 (coverage), §9 (log rows and the block's answer distribution)
   and §11 (changelog), and the board count in CLAUDE.md's Current state; then run python build.py and the three
   tests. If this pair completes a block, audit the block against the plan (letters, stars, systems, tasks, settings)
   and report it.
8. Show me, per question: ID, topic, answer, stars, key source, and what changed at review. For the first pair, and
   whenever I ask, show both questions in full as the app shows them. Wait for my OK. Then set the blueprint rows to
   "pushed", commit ("Add pediatric pair NN: <IDs>"), push to main, and confirm that the live site's data/boards.json
   has the new total.
