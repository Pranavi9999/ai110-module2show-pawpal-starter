import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Pet, Task


def test_mark_complete_changes_status():
    task = Task(title="Morning walk", duration_minutes=30, priority="high")
    assert task.is_complete == False
    task.mark_complete()
    assert task.is_complete == True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", species="dog", age=3)
    assert len(pet.tasks) == 0
    pet.add_task(Task(title="Evening walk", duration_minutes=20, priority="medium"))
    assert len(pet.tasks) == 1


if __name__ == "__main__":
    test_mark_complete_changes_status()
    print("PASS: mark_complete changes status")

    test_add_task_increases_pet_task_count()
    print("PASS: add_task increases pet task count")
