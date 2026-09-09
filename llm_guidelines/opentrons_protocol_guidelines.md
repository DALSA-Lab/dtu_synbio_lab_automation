# Opentrons Protocol Guidelines for LLMs

Behavioral guidelines for any LLM writing or editing Opentrons protocols. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution, explicitness, and simulation over speed. For tiny documentation edits, use judgment.

## 1. Think Before Moving Liquid

**Do not assume the biology. Do not invent deck reality. Surface uncertainty early.**

Before writing protocol code:

- State the biological goal in one sentence.
- Identify the robot, API level, pipettes, modules, labware, liquids, and deck slots.
- Say what is operator-configurable through runtime parameters.
- Say what is fixed because it is a validated lab assumption.
- If labware, well maps, volumes, or incubation conditions are unclear, ask.
- If several interpretations are possible, present them briefly.
- If a simpler manual or semi-automated workflow is better, say so.

Never silently guess:

- Labware load names.
- Pipette mounts.
- Module generations.
- Well order.
- Dead volume.
- Mix volume.
- Incubation temperature.
- Antibiotic, strain, plasmid, or media identity.

## 2. Simplicity First

**Minimum protocol that correctly performs the workflow. Nothing speculative.**

- Start with metadata, requirements, runtime parameters, deck setup, and a simple `run()`.
- Prefer a readable loop over repeated transfer commands.
- Prefer CSV plate maps for larger transfer plans.
- Use helper functions only when they remove real complexity.
- Do not create framework code for a single protocol.
- Do not add flexible modes unless the operator actually needs them.
- Do not add error handling for scenarios the robot API already prevents.
- If the protocol is hard to explain in a short paragraph, simplify it.

Ask yourself: "Can a wet-lab scientist review this without reading around hidden abstractions?" If not, rewrite.

## 3. Runtime Parameters Over Hidden Constants

**Operator choices belong in the Opentrons App. Lab invariants belong in named code.**

Use runtime parameters for:

- Sample count.
- Transfer volume.
- Dilution factor.
- Mix repetitions.
- Protocol mode.
- CSV plate map.
- Optional controls.

Use named constants only for true invariants:

- Robot type.
- API level.
- Fixed deck slots.
- Validated labware load names.
- Validated safety limits.
- Lab-specific default thresholds.

Bad pattern:

```python
volume = 47
```

Better pattern:

```python
parameters.add_float(
    variable_name="transfer_volume_ul",
    display_name="Transfer volume",
    description="Volume moved from each sample.",
    default=50,
    minimum=5,
    maximum=200,
    unit="uL",
)
```

## 4. Make Robot Behavior Visible

**A protocol is both code and an operator-facing method.**

Keep these actions easy to find:

- Loading labware.
- Loading pipettes.
- Loading modules.
- Defining liquids.
- Picking up and dropping tips.
- Mixing.
- Pausing.
- Delaying.
- Setting temperatures.
- Engaging magnets.
- Shaking.
- Moving labware.

Use comments and `protocol.comment()` for biological intent and operator context. Do not comment obvious Python.

Good comments explain why:

```python
protocol.comment("Mix each dilution before transferring to the next column.")
```

Weak comments repeat syntax:

```python
# Transfer liquid
pipette.transfer(volume, source, destination)
```

## 5. Validate Before Execution

**Fail before liquid moves.**

Validate:

- Runtime parameter ranges that depend on pipette or labware choice.
- Sample count against available wells.
- Transfer volume against pipette capacity.
- Transfer volume against source volume and dead volume.
- Mix volume against destination volume.
- CSV columns and well names.
- Control wells and blank wells.
- Module requirements.

Keep validation readable. If validation becomes long, extract it into a helper with a clear name like `validate_transfer_plan()`.

## 6. Surgical Changes

**Touch only what the user asked for. Clean up only your own mess.**

When editing existing protocols:

- Match the existing style unless it is unsafe or unclear.
- Do not refactor unrelated code.
- Do not change labware, slots, pipettes, or modules unless asked.
- Do not update protocol behavior while only claiming to edit comments.
- Remove imports or variables made unused by your own change.
- Mention unrelated issues instead of fixing them silently.

Every changed line should trace back to the user request or a required safety fix.

## 7. Goal-Driven Execution

**Define success criteria. Verify them.**

For protocol work, success usually means:

- The protocol imports correctly.
- Runtime parameters are defined clearly.
- The deck layout is explicit.
- The transfer plan is reviewable.
- The protocol simulates without errors.
- Any generated CSV or notebook examples match the code.

Use a plan for multi-step changes:

```text
1. Update runtime parameters -> verify: protocol analysis succeeds
2. Add transfer loop -> verify: simulation reaches completion
3. Update README -> verify: links and commands are correct
```

## 8. Simulation Is Not Optional

**Robot code is not done until it has been analyzed or simulated.**

For Python protocols:

```bash
uv run opentrons_simulate protocols/opentrons/<protocol>.py
```

If simulation cannot run, say why. Do not pretend syntax checks are the same as robot simulation.

A useful final report includes:

- What changed.
- Which protocols were simulated.
- Which checks passed.
- What could not be verified.
- Any assumptions the operator must confirm before a real run.

## 9. Safety And Traceability

**Liquid handlers make mistakes at physical scale. Treat protocol code as lab method code.**

- Keep sample identity traceable from input file to well position.
- Keep controls visible.
- Keep manual handoffs explicit.
- Make contamination-sensitive steps obvious.
- Do not hide biological assumptions in variable names alone.
- Do not produce robot-ready code when the biological method is underspecified.

## 10. These Guidelines Are Working If

- Diffs are small and easy to review.
- Protocols simulate before they are called done.
- Runtime parameters are understandable in the Opentrons App.
- Deck setup matches the actual robot.
- Repeated transfers come from data, not copy-paste.
- Clarifying questions happen before unsafe assumptions become code.
