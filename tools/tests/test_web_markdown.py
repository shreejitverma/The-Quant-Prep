"""Behaviour tests for the dashboard's note renderer (tools/qp/web/app.js), run in Node."""

from __future__ import annotations

import json
import shutil
import subprocess
import unittest
from pathlib import Path

APP_JS = Path(__file__).resolve().parents[1] / "qp" / "web" / "app.js"

# Loads app.js in a sandbox with stand-ins for the browser globals and the CDN libraries.
# marked and DOMPurify pass text through; katex records each maths span as [I:tex] or [D:tex].
HARNESS = r"""
const fs = require("fs");
const vm = require("vm");
const [appPath, input] = process.argv.slice(1);
const ctx = {
  document: { getElementById: () => null },
  addEventListener: () => {},
  marked: { parse: (s) => s, parseInline: (s) => s },
  DOMPurify: { sanitize: (s) => s },
  katex: { renderToString: (t, o) => `[${o.displayMode ? "D" : "I"}:${t}]` },
};
ctx.window = ctx;
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(appPath, "utf8"), ctx);
process.stdout.write(JSON.stringify(vm.runInContext("renderMarkdown", ctx)(JSON.parse(input))));
"""


@unittest.skipUnless(shutil.which("node"), "node not installed")
class InlineMathTest(unittest.TestCase):
    def render(self, src: str) -> str:
        out = subprocess.run(
            ["node", "-e", HARNESS, str(APP_JS), json.dumps(src)],
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(out.stdout)

    def test_escaped_dollar_inside_inline_maths_is_rendered_as_tex(self):
        # KaTeX (and Obsidian) treat \$ as a literal dollar sign inside maths.
        self.assertEqual(self.render(r"with $\$10{,}000$ DV01"), r"with [I:\$10{,}000] DV01")
        self.assertEqual(
            self.render(r"$a = \$1 - \$2 = +\$3$ and $V$."),
            r"[I:a = \$1 - \$2 = +\$3] and [I:V].",
        )
        self.assertEqual(self.render(r"> $\$4$. $V = 4$."), r"> [I:\$4]. [I:V = 4].")

    def test_escaped_dollar_outside_maths_stays_text(self):
        self.assertEqual(self.render(r"costs \$1. The value $V$ solves"), r"costs \$1. The value [I:V] solves")

    def test_escaped_dollar_does_not_close_inline_maths(self):
        self.assertEqual(self.render(r"$x\$ y$"), r"[I:x\$ y]")

    def test_display_maths_with_escaped_dollar(self):
        self.assertEqual(self.render(r"$$N = \frac{\$10}{\$2}$$"), r"[D:N = \frac{\$10}{\$2}]")

    def test_display_maths_with_delimiters_on_own_lines(self):
        # Obsidian renders a $$ block split over lines as one display equation.
        self.assertEqual(self.render("a\n\n$$\nE[X] = \\$1\n$$\n\nb"), "a\n\n[D:E[X] = \\$1]\n\nb")
        # An unclosed $$ leaves the following lines as ordinary text.
        self.assertEqual(self.render("$$\nx"), "$$\nx")

    def test_card_prompt_is_one_element_in_the_summary(self):
        # The summary is a flex row: the Q badge and the prompt must be its only two items.
        out = self.render("> [!question]- fi-x | Find $P_3$ given $s$\n> answer")
        self.assertIn("<summary><span>Find [I:P_3] given [I:s]</span></summary>", out)


if __name__ == "__main__":
    unittest.main()
