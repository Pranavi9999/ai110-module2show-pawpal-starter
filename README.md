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

## Testing PawPal+

### Running the tests

```bash
python -m pytest tests/
```

Or to see each test name as it runs:

```bash
python -m pytest tests/ -v
```

### What the tests cover

| Area | Tests |
|---|---|
| **Sorting correctness** | Tasks return in chronological order (morning → afternoon → evening); unrecognized time slots default to midday; the original task list is never mutated; empty scheduler returns `[]` |
| **Recurrence logic** | Daily task creates a next-day task on completion; weekly task creates one 7 days later; non-recurring tasks return `None`; missing `due_date` falls back to today; `Scheduler.complete_task()` appends the new task and does not grow the list for one-off tasks |
| **Conflict detection** | Two tasks at the same hour are flagged; sequential tasks (no gap, no overlap) pass cleanly; partially overlapping tasks are caught; empty schedule returns no warnings |
| **Core behavior** | `mark_complete()` sets `is_complete = True`; `pet.add_task()` increases the task count |

### Confidence Level

**★★★★☆ (4 / 5)**

The core scheduling logic — sorting, recurrence, and conflict detection — is well-covered by the test suite and the implementations are straightforward. One star is held back because `build_schedule()`, `priority_value()`, and `get_species_defaults()` are still stubs, so end-to-end schedule generation and priority tie-breaking are not yet tested. Confidence will reach 5 / 5 once those methods are implemented and covered.

---

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
