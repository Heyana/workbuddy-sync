---
name: improve-codebase-architecture
description: Scan a codebase for deepening opportunities (shallow modules, tight coupling, untested seams), present them as a visual HTML report, then grill through your chosen refactoring.
---

# Improve Codebase Architecture

Surface architectural friction and propose **deepening opportunities** — refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability.

## When to Use

Trigger this skill when the user asks to:
- Review codebase architecture or design quality
- Find refactoring opportunities
- Improve testability of existing code
- "Clean up" or "restructure" code
- Analyze module coupling or cohesion

**Auto-trigger keywords**: architecture review, codebase review, refactor, restructure, deepen modules, shallow modules, coupling, cohesion, testability

## Core Concepts

This skill uses a specific architectural vocabulary from John Ousterhout's "deep module" principle:

- **Module**: A unit of code with an interface and implementation
- **Interface**: What callers see and depend on — should be small
- **Implementation**: What the interface hides — should be large
- **Depth**: The ratio of implementation complexity to interface complexity. Deep modules have small interfaces hiding large implementations.
- **Seam**: A place where you can vary behavior without changing the module itself
- **Adapter**: Code that sits behind a seam; "one adapter = hypothetical seam, two = real"
- **Leverage**: How much work a module does for how little its caller needs to know
- **Locality**: How close together related code lives. High locality means you can understand a concern without jumping between files.

**The deletion test**: If you deleted this module, would complexity concentrate elsewhere (good), or just move (shallow)?

**Note**: This skill works best when the project has a `CONTEXT.md` file with domain terms and a `docs/adr/` directory with architecture decision records. Without these, it can still operate but domain naming will be generic.

## Process

### 1. Explore

Read the project's domain glossary (`CONTEXT.md`) and any ADRs in the area first if they exist.

Then walk the codebase organically. Don't follow rigid heuristics — explore and note where you experience friction:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow** — interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?

Apply the **deletion test** to anything you suspect is shallow: would deleting it concentrate complexity, or just move it?

### 2. Present candidates as an HTML report

Write a self-contained HTML file to the OS temp directory. Use `%TEMP%` on Windows, `/tmp` on Linux/macOS. Name: `architecture-review-<timestamp>.html`. Open it for the user immediately.

The report should use Tailwind CDN for styling and Mermaid CDN for diagrams. Each candidate card includes:

- **Files**: which files/modules are involved
- **Problem**: why the current architecture is causing friction
- **Solution**: plain English description of what would change
- **Benefits**: explained in terms of locality, leverage, and test improvements
- **Before/After diagram**: side-by-side visual comparison
- **Recommendation strength**: Strong / Worth exploring / Speculative

End with a **Top recommendation** section.

### 3. Grilling loop

Once the user picks a candidate, walk the design tree with them:
- Constraints and dependencies
- The shape of the deepened module
- What sits behind the seam
- What tests survive or should be added

Side effects as decisions crystallize:
- **New domain concept?** Add it to `CONTEXT.md` (create lazily if needed)
- **Sharpening a fuzzy term?** Update `CONTEXT.md` immediately
- **User rejects with a load-bearing reason?** Offer to record as an ADR
- **Want to explore alternative interfaces?** Generate multiple designs with parallel sub-agents and recommend the strongest approach
