from models import Universe, Character, Work, Relationship, Terminology


def get_universe_id_by_name(universe_name):
    """get universe id by using its name"""
    universe = Universe.query.filter_by(universe_title=universe_name).first()
    if universe:
        return universe.id
    else:
        raise ValueError(f"Universe with name '{universe_name}' not found, try again.")


def get_character_id_by_name(char_name):
    """get character id by using their name"""
    character = Character.query.filter_by(char_name=char_name).first()
    if character:
        return character.char_id
    else:
        raise ValueError(f"Character with name {char_name} not found, try again.")


def get_work_id_by_title(work_title):
    """gets work id by using its name"""
    work = Work.query.filter_by(work_title=work_title).first()
    if work:
        return work.work_id
    else:
        raise ValueError(f"Work with title '{work_title}' not found, try again.")


def get_term_id_by_name(term_name):
    """get character id by using their name"""
    terminology = Terminology.query.filter_by(term_name=term_name).first()
    if terminology:
        return terminology.term_id
    else:
        raise ValueError(f"'{term_name}' not found, try again.")


def create_a_universe(session, title, author):
    """creates a universe. uses a title and an author"""
    new_universe = Universe(universe_title=title, author=author)
    session.add(new_universe)
    session.commit()
    return f"Universe '{title}' created successfully."


def create_a_character(session, universe_id, char_name, gender, age, status, biography):
    """creates a character. add information about them."""
    new_character = Character(
        universe_id=universe_id,
        char_name=char_name,
        gender=gender,
        age=age,
        status=status,
        biography=biography
    )
    session.add(new_character)
    session.commit()
    return f"Character '{char_name}' created successfully."


def create_a_work(session, universe_id, title, ext_link):
    """creates a work. adds information about it."""
    new_work = Work(universe_id=universe_id, work_title=title, link=ext_link)
    session.add(new_work)
    session.commit()
    return f"Work '{title}' added successfully."


def create_a_relationship(session, universe_id, char_1, char_2, rel_type):
    """creates a relationship between two characters."""
    new_relationship = Relationship(universe_id=universe_id, character1_id=char_1, character2_id=char_2,
                                    relationship_type=rel_type)
    session.add(new_relationship)
    session.commit()
    return f"New relationship added successfully."


def create_terminology(session, universe_id, term_name, definition):
    """creates terminology. adds a name and a definition."""
    new_terminology = Terminology(universe_id=universe_id, term_name=term_name, definition=definition)
    session.add(new_terminology)
    session.commit()
    return f"{term_name} added successfully."


def delete_universe(session, universe_id):
    universe_to_delete = Universe.query.get(universe_id)
    if universe_to_delete:
        session.delete(universe_to_delete)
        session.commit()
        return f"Universe {universe_to_delete.universe_title} deleted successfully."
    else:
        print(f"Universe {universe_to_delete.universe_title} not found.")
    session.commit()


def delete_work(session, work_id):
    """deletes a work using its ID."""
    work_to_delete = Work.query.get(work_id)
    if work_to_delete:
        session.delete(work_to_delete)
        session.commit()
        return f"Work {work_to_delete.work_title} deleted successfully."
    else:
        print(f"Work {work_to_delete.work_title} with not found.")
    session.commit()


def delete_character(session, char_id):
    """deletes a character using their ID (and deletes their relationships so anomalies don't happen)"""
    char_to_delete = Character.query.get(char_id)
    if char_to_delete:
        relationships = session.query(Relationship).filter(
            (Relationship.character1_id == char_id) | (Relationship.character2_id == char_id)
        ).all()
        for relationship in relationships:
            session.delete(relationship)
        session.commit()
        session.delete(char_to_delete)
        session.commit()
        return f"Character {char_to_delete.char_name} and their relationships have been deleted."
    else:
        print(f"Character with ID {char_to_delete.char_name} not found.")
    session.commit()


def delete_terminology(session, term_id):
    """deletes terminology."""
    term_to_delete = Terminology.query.get(term_id)
    if term_to_delete:
        session.delete(term_to_delete)
        session.commit()
        return f"Terminology {term_to_delete.term_name} deleted successfully."
    else:
        print(f"Terminology {term_to_delete.term_name} not found.")
    session.commit()


def delete_relationship(session, char1_id, char2_id, rel_type):
    """deletes a relationship"""
    rel = session.query(Relationship).filter(
        (Relationship.character1_id == char1_id) &
        (Relationship.character2_id == char2_id) &
        (Relationship.relationship_type == rel_type)
    ).first()
    if rel:
        session.delete(rel)
        session.commit()
        return f"Relationship deleted successfully."
    else:
        print(f"Relationship not found.")
    session.commit()


def edit_data(session, table_to_edit, data_id, field_to_edit, new_value):
    """edits data"""
    data_to_edit = None
    if table_to_edit == "CHARACTERS":
        data_to_edit = session.query(Character).filter_by(char_id=data_id).first()
    elif table_to_edit == "WORKS":
        data_to_edit = session.query(Work).filter_by(work_id=data_id).first()
    elif table_to_edit == "TERMINOLOGY":
        data_to_edit = session.query(Terminology).filter_by(term_id=data_id).first()

    setattr(data_to_edit, field_to_edit, new_value)
    session.commit()
