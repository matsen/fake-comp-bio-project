Please read issue {{0}} using `gh`.
We are going to do the work described there.

**Before starting:**
- Think hard to brainstorm clarifying questions
- If you have any such questions, STOP and ask them
- Once everything is clear, pull main and create a new feature branch {{0}}-...

**During implementation:**
- Don't get creative with the implementation - copy code directly from the issue as a starting point
- Feel free to refine code as needed, but STOP if you start deviating from the issue significantly so we can discuss
- Follow CLAUDE.md guidelines (code quality, testing standards, documentation)
- Continue until the issue is done and all tests pass

**Before creating PR:**
- Run `pytest tests/ -v` to ensure all tests pass
- Verify the implementation matches all requirements from the issue

**When creating the PR:**
- Include "Closes #{{0}}" in the PR description to link the issue
- Provide clear summary of changes and design decisions
- Do NOT manually close the issue - GitHub will auto-close it when the PR merges
- Leave the issue open for tracking until the PR is reviewed and merged
