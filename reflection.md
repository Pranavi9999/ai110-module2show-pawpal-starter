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

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
