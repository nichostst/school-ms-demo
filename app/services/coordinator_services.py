# Standard Library imports
from typing import List

# Core Flask imports

# Third-party imports

# App imports
from app import db_manager as db
from ..models import modules_lecturers


def assign_lecturer(module_id: int, lecturer_id: int, term_ids: List[int]):
    result = 'success'
    query = db.session.query(
        modules_lecturers.c.module_id,
        modules_lecturers.c.lecturer_id,
        modules_lecturers.c.term_id,
    ).filter(
        modules_lecturers.c.module_id == module_id,
    ).all()

    for term in term_ids:
        module_term = [q for q in query if q.term_id == term]
        assert len(module_term) <= 1, f"(Module ID: {module_id}, Term ID: {term}) has multiple lecturers."

        module_term_already_assigned = bool(len(module_term))
        # If module-term pair has a lecturer
        if module_term_already_assigned:
            print(f'(Module ID: {module_id}, Term ID: {term}) has already been assigned, skipping.')
            result = 'partial'
            continue

        # If module-term pair has no lecturer, assign
        ml = modules_lecturers.insert().values(
            module_id=module_id,
            lecturer_id=lecturer_id,
            term_id=term
        )
        db.session.execute(ml)

        # Clear all previous unassigned relations
        unassigned = modules_lecturers.delete().where(
            modules_lecturers.c.module_id == module_id,
            modules_lecturers.c.lecturer_id == lecturer_id,
            modules_lecturers.c.term_id == None
        )

        db.session.execute(unassigned)

        db.session.commit()

    return result