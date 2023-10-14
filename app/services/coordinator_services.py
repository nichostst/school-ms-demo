# Standard Library imports
from typing import List, Dict

# Core Flask imports

# Third-party imports

# App imports
from app import db_manager as db
from ..models import modules_lecturers, ModuleGradeStructure


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

def change_weights(new_weights: Dict[str, float]):
    try:
        assert sum(new_weights.values()) == 1
    except AssertionError:
        print('Weights do not sum to 100%, please check again')
        return 'weight_failure'
    
    try:
        assert min(new_weights.values()) >= 0.05
    except AssertionError:
        print('Minimum weight for a structure is 5%, please check again')
        return 'min_weight_failure'

    query = db.session.query(ModuleGradeStructure)

    sorted_new_weights = dict(sorted(new_weights.items()))
    for structure_id, structure_weight in sorted_new_weights.items():
        s = query.filter(ModuleGradeStructure.structure_id == structure_id).first()
        s.weightage = round(structure_weight, 2)
    
    db.session.commit()

    return 'success'

def create_structures(structures, types, weights, module_id):
    try:
        assert sum(weights) == 1
    except AssertionError:
        print('Weights do not sum to 100%, please check again')
        return 'weight_failure'
    
    try:
        assert min(weights) >= 0.05
    except AssertionError:
        print('Minimum weight for a structure is 5%, please check again')
        return 'min_weight_failure'

    for s, t, w in zip(structures, types, weights):
        mgs = ModuleGradeStructure(
            module_id=int(module_id),
            structure_name=s,
            structure_type=t,
            weightage=w
        )
        db.session.add(mgs)
        db.session.flush()

    db.session.commit()
    return 'success'