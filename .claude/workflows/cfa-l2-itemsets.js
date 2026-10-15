export const meta = {
  name: 'cfa-l2-itemsets',
  description: 'Write CFA L2 bank item sets and Mock 3-6 item sets per learning module, then independently audit every answer',
  phases: [
    { title: 'Bank', detail: 'bank item sets per LM (3 or 4)' },
    { title: 'Mock', detail: 'fresh Mock 3-6 item sets per LM, distinct from bank' },
    { title: 'Audit', detail: 'independent re-solve and fix of every set for the LM' },
  ],
}

const SCRATCH = 'build/cfa_l2/agent-scratch'  // gitignored, under the repository root
const BANK = '17-CFA/CFA-L-2/20-Item-Set-Bank'
const FOUR = ['01', '03', '05', '06', '09', '10']
// mock -> topic code -> ordered LM list; the first LM listed per topic in each mock is written at difficulty 4
const MOCKS = {
  3: { '01': [1, 5], '02': [1], '03': [1, 2, 3], '04': [1, 3], '05': [2, 3, 5], '06': [1, 2, 3], '07': [1, 2], '08': [1], '09': [1, 2, 5], '10': [2, 3] },
  4: { '01': [2, 6], '02': [2], '03': [4, 5, 6], '04': [2, 4], '05': [1, 4, 6], '06': [3, 4, 5], '07': [1, 2], '08': [2], '09': [3, 4, 6], '10': [2, 3] },
  5: { '01': [3, 7], '02': [1], '03': [1, 3, 5], '04': [1, 4], '05': [2, 3, 4], '06': [1, 2, 4], '07': [1, 2], '08': [4], '09': [2, 4, 5], '10': [1, 2] },
  6: { '01': [4, 5], '02': [2], '03': [2, 4, 6], '04': [2, 3], '05': [3, 5, 6], '06': [2, 3, 5], '07': [1, 2], '08': [3], '09': [1, 3, 6], '10': [1, 3] },
}
const HARD = ['01', '03', '05', '06', '07', '09', '10']

const items = args.notes.map(n => {
  const [code, slug, lmStr] = [n.code, n.slug, n.lm]
  const lm = Number(lmStr)
  const nn = String(lm).padStart(2, '0')
  const mocks = []
  for (const m of [3, 4, 5, 6]) {
    const list = MOCKS[m][code]
    const idx = list.indexOf(lm)
    if (idx >= 0) mocks.push({ mock: m, difficulty: idx === 0 && HARD.includes(code) ? 4 : 3, file: `${BANK}/${slug}/IS-${slug}-LM${nn}-M0${m}.md` })
  }
  const bankN = FOUR.includes(code) ? 4 : 3
  const bankFiles = Array.from({ length: bankN }, (_, i) => `${BANK}/${slug}/IS-${slug}-LM${nn}-${i + 1}.md`)
  return { ...n, lm, nn, mocks, bankN, bankFiles, key: `${code}-${nn}` }
})

const WRITE_SCHEMA = {
  type: 'object',
  properties: {
    files: { type: 'array', items: { type: 'string' } },
    los_covered: { type: 'array', items: { type: 'string' } },
    verify_lines: { type: 'string' },
    notes: { type: 'string' },
  },
  required: ['files', 'verify_lines'],
}
const AUDIT_SCHEMA = {
  type: 'object',
  properties: {
    files_checked: { type: 'integer' },
    questions_checked: { type: 'integer' },
    fixes: { type: 'array', items: { type: 'object', properties: { file: { type: 'string' }, question: { type: 'string' }, problem: { type: 'string' }, fix: { type: 'string' } }, required: ['file', 'problem', 'fix'] } },
    unresolved: { type: 'array', items: { type: 'string' } },
  },
  required: ['files_checked', 'questions_checked', 'fixes', 'unresolved'],
}

const common = (it) => `Topic ${it.code} ${it.topic} (folder slug ${it.slug}), learning module ${it.lm}.
LM note: ${it.note}
Curriculum practice problems (style reference only, never copy): build/cfa_l2/${it.slug}/LM${it.nn}.json
Valid LOS IDs are the keys of build/cfa_l2/los_index.json starting with los-${it.code}-${it.nn}-; use only those.
Work from the repository root (the current working directory).
Put any Python scratch scripts under ${SCRATCH}/${it.key}/ (create it), never anywhere else in the repository.
Do not modify any file other than the item-set files named below; do not run git.
The tag for this topic is cfa/${it.slug.replace(/^\d+-/, '').toLowerCase()}.`

const results = await pipeline(
  items,
  (it) => agent(`You are writing original CFA Level II bank item sets.
Read 17-CFA/scripts/cfa_l2/ITEMSET_SPEC.md fully and follow it verbatim, then read the LM note fully.
${common(it)}

Write exactly ${it.bankN} files:
${it.bankFiles.join('\n')}
Frontmatter source: bank. Each set has 4 to 6 questions (minutes 18 for 6, 12 for 4); at least one set at difficulty 4.
Across the ${it.bankN} sets, cover every LOS of this module that is testable in an item set, and vary entity type, scenario (valuation, reporting, decision, compliance), and which LOS carry the calculations.
Recompute every number in Python before writing it into the answer key; distractors must come from named errors.
Then run python3 17-CFA/scripts/cfa_l2/verify_practice.py and python3 17-CFA/scripts/cfa_l2/verify_notes.py ${it.code}, and fix anything that concerns your files.
Return the files written, the LOS IDs covered, and the verify lines that mention ${it.key} or your file names.`, { label: `bank ${it.key}`, phase: 'Bank', schema: WRITE_SCHEMA }),
  (bank, it) => it.mocks.length === 0 ? bank : agent(`You are writing original CFA Level II item sets for fresh mock exams.
Read 17-CFA/scripts/cfa_l2/ITEMSET_SPEC.md and 17-CFA/scripts/cfa_l2/MOCK_SPEC.md fully, then read the LM note fully.
${common(it)}

The bank sets for this module already exist: ${it.bankFiles.join(', ')}.
Read them first; your mock sets must not reuse their scenarios, entity names, exhibits, or LOS-and-calculation mix, and must differ from each other.

Write exactly these files (one per mock slot):
${it.mocks.map(s => `${s.file}  (source: mock-0${s.mock}, difficulty: ${s.difficulty})`).join('\n')}
Each mock set uses the ITEMSET_SPEC frontmatter and body with these differences: source is mock-0<n> as listed, EXACTLY 4 questions, minutes: 12, the timer callout says 12 minutes for 4 questions, and the title line is the vignette title.
A difficulty-4 set must be genuinely harder than curriculum level: multi-step calculations, exhibits with decoys, questions that chain.
Recompute every number in Python before writing it into the answer key; distractors must come from named errors.
Then run python3 17-CFA/scripts/cfa_l2/verify_practice.py and python3 17-CFA/scripts/cfa_l2/verify_notes.py ${it.code}, and fix anything that concerns your files.
Return the files written, the LOS IDs covered, and the verify lines that mention ${it.key} or your file names.`, { label: `mock ${it.key}`, phase: 'Mock', schema: WRITE_SCHEMA }),
  (mock, it) => agent(`You are an independent auditor of CFA Level II item sets; assume the author made mistakes and find them.
${common(it)}
Audit rules are in 17-CFA/scripts/cfa_l2/ITEMSET_SPEC.md (and MOCK_SPEC.md for the M0n files); read them and the LM note.

Files to audit:
${[...it.bankFiles, ...it.mocks.map(s => s.file)].join('\n')}

For every question in every file:
1. Solve it yourself from the vignette alone, BEFORE reading the answer key, recomputing every number in Python (for Ethics, reason from the Standards text in the LM note).
2. Compare with the key: the keyed answer must be the single defensible correct choice, each wrong option must be wrong for the reason the key states, and the vignette must contain every input needed with no contradiction.
3. Check the curriculum conventions the LM note uses (formula variants, day counts, compounding, IFRS vs US GAAP treatment, sign conventions, which Standard applies).
4. Check structure: frontmatter keys and values per the spec (type, topic, topic_code as a quoted string, topic_slug, lm, title, los list of valid IDs for this module, difficulty, minutes, source, attempts: 0, tags), every question ends with (LOS: <valid id for this module>), 4 to 6 questions for bank sets and exactly 4 for M0n sets, Answer key inside a foldable success callout, Distractor design section, no emoji, no em dash character, one sentence per line in prose.
Fix every defect in place with minimal edits (a wrong key, a wrong number, an ambiguous stem, a second correct option, a missing input, a format error).
If an option letter changes, update the key, reasoning, and distractor line consistently.
Then run python3 17-CFA/scripts/cfa_l2/verify_practice.py and python3 17-CFA/scripts/cfa_l2/verify_notes.py ${it.code}.
Return counts, every fix you made, and anything you could not resolve.`, { label: `audit ${it.key}`, phase: 'Audit', schema: AUDIT_SCHEMA })
    .then(a => ({ key: it.key, mockFiles: it.mocks.map(s => s.file), audit: a })),
)

const done = results.filter(Boolean)
const fixes = done.reduce((s, r) => s + ((r.audit && r.audit.fixes) ? r.audit.fixes.length : 0), 0)
log(`${done.length}/${items.length} modules completed, ${fixes} audit fixes`)
return {
  completed: done.map(r => r.key),
  missing: items.filter(it => !done.find(r => r.key === it.key)).map(it => it.key),
  audits: done.map(r => ({ key: r.key, checked: r.audit ? r.audit.questions_checked : 0, fixes: r.audit ? r.audit.fixes : [], unresolved: r.audit ? r.audit.unresolved : ['audit missing'] })),
}
