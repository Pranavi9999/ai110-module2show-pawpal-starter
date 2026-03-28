# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design:
The 3 core actions a user should be able to perform are:
    - Seeing the daily schedule
    - Adding one or multiple pets
    - Being able to schedule a task

- What classes did you include, and what responsibilities did you assign to each?

I am planning on adding a pet, owner, task, and scheduler class.

- The pet class will have the following responsibilities: name, species, age
- The owner class will have the following responsibilities: name, available_start, available_end, pets, add_pet
- The task class will have the following responsibilities: title, duration_time, priority, is_recurring
- The scheduler class will have the following responsibilities: owner, tasks, add_task, build_schedule()

**b. Design changes**

- Did your design change during implementation? Yes, AI helped me notice that there was no time slot tracking, the explain_schedule method had no shared state with build_schedule, and Task was not linked to Pet.

- If yes, describe at least one change and why you made it. Originally build_schedule() and explain_schedule() were fully independent. I added self._schedule: list[tuple[Task, int]] so build_schedule() stores each task with its assigned start hour, and explain_schedule() reads from it. Without shared state, explain_schedule() had no way to know when or why tasks were placed.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

Owner availability window: tasks only get placed between available_start and available_end (e.g., 8am–8pm). Any task that would push past available_end is dropped entirely.

Preferred time slot: each task declares morning, afternoon, or evening. The scheduler maps these to anchor hours (8, 13, 17) and won't start a task earlier than its slot's anchor.

Priority: within the same time slot, high priority tasks are sorted before medium and low, so they get placed first and are least likely to be crowded out.

Task duration: the running clock advances by duration_minutes / 60 after each task, preventing tasks from stacking on top of each other.

How I decided which mattered most:

Time availability comes first because it's a hard limit. No amount of priority overrides the fact that the owner simply isn't available. Preferred time slot comes second because pet care tasks are often biologically driven (a morning walk, a bedtime feeding), so respecting the slot keeps the schedule realistic. Priority acts as a tiebreaker within a slot rather than a global override, because bumping a low-priority task from morning to evening is less disruptive than ignoring time preferences entirely.
**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler uses a single running clock that advances tasks one after another, so it cannot place two tasks in parallel, even if one is for Buddy and one is for Mochi.

Why it's reasonable: A solo pet owner can only actively do one thing at a time. They can't walk Buddy while simultaneously cleaning Mochi's litter box. Modeling the schedule as a linear queue reflects how a real owner experiences their day. Allowing parallel tracks would suggest the owner can be in two places at once, which isn't practical for daily planning. The tradeoff favors simplicity and real-world accuracy over scheduling efficiency.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

I used AI to help with the mermaid code, the logic, and test cases. 

- What kinds of prompts or questions were most helpful?

The more information I gave provided the best outputs. It's important to make sure you give the most amount of relevant information to receive an output tailored to the question.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

Sometimes when I would ask a question to help me with brainstorming it would automatically provide the code when I just wanted ideas. I would have to decline the code and emphasize that I didn't want code.

- How did you evaluate or verify what the AI suggested?

I would run the code to see that the output is as expected.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

Some behaviors that I tested were a task with missing/unknown time. This is important to test to make sure it doesn't crash. Test what happens when 2 tasks are in the same time slot. Test what happens when there's an empty task list and make sure it does not raise an error. 

**b. Confidence**

- How confident are you that your scheduler works correctly?
About 4/5 for the parts that are built — sorting, recurrence, filtering, and conflict detection all have passing tests. Confidence drops for the full pipeline since build_schedule() and priority_value() are still stubs and untested end-to-end.

- What edge cases would you test next if you had more time?
- Tasks that overflow past available_end
- Priority tie-breaking within the same time slot
- filter_tasks() with both filters active at once (AND logic)
- Zero-duration tasks in conflict detection

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am satisfied that the project runs successfully and does what is intended. It handles the edge cases successfully and does not crash.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would work on making the UI better. Currently it looks very simple, and making more enhancements would make it more user friendly.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

We can't accept every output that AI gives. We have to make sure that the output it gives is a plausible fix. Also, make sure to push to github often in case AI accidentally writes over existing code that you need. 