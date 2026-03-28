# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

Beyond basic task ordering, PawPal+ includes four algorithmic improvements to make the daily plan more reliable:

- **Time-slot sorting** — `sort_by_time()` orders tasks chronologically across morning, afternoon, and evening slots. Tasks with no preferred time default to midday so they never disrupt the morning or evening anchors.

- **Flexible filtering** — `filter_tasks()` accepts an optional completion status and/or pet name, making it easy to answer questions like "what does Buddy still have left today?" without looping manually.

- **Recurring task scheduling** — marking a `"daily"` or `"weekly"` task complete via `complete_task()` automatically creates the next occurrence with the correct due date calculated using Python's `timedelta`. One-off tasks are unaffected.

- **Conflict detection** — `detect_conflicts()` scans the built schedule for overlapping time windows using the interval overlap condition (`A.start < B.end and B.start < A.end`) and returns plain-English warning messages without crashing the program.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
