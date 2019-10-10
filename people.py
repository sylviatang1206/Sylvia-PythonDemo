from flask import make_response, abort, jsonify
from config import db
from models import Person, PersonSchema

def read_all():
    print("read all - before query")
    
    # Create the list of people from our data
    people = Person.query.order_by(Person.lname).all()
    print(f"read all - after query people = {people}")


    # Serialize the data for the response
    person_schema = PersonSchema(many=True)
    print(person_schema.dump(people))
    data = person_schema.dump(people)
    print(f"read all- data = {data}")
    return data


def read_one(person_id):
    # Get the person requested
    person = Person.query.filter(Person.person_id == person_id).one_or_none()

    if person is not None:

        person_schema = PersonSchema()
        data = person_schema.dump(person)
        return data

    else:
        abort(
            404,
            "Person not found for Id: {person_id}".format(person_id=person_id),
        )


def create(person):
    
    fname = person.get("fname")
    lname = person.get("lname")

    existing_person = (
        Person.query.filter(Person.fname == fname)
        .filter(Person.lname == lname)
        .one_or_none()
    )

    if existing_person is None:

        # Create a person instance using the schema and the passed in person
        schema = PersonSchema()
        new_person = schema.load(person, session=db.session)

        # Add the person to the database
        db.session.add(new_person)
        db.session.commit()

        # Serialize and return the newly created person in the response
        data = schema.dump(new_person)

        return data, 201

    # Otherwise, person exists already
    else:
        abort(
            409,
            "Person {fname} {lname} exists already".format(
                fname=fname, lname=lname
            ),
        )


def update(person_id, person):
    # Get the person requested from the db into session
    update_person = Person.query.filter(
        Person.person_id == person_id
    ).one_or_none()

    # Try to find an existing person with the same name as the update
    fname = person.get("fname")
    lname = person.get("lname")

    existing_person = (
        Person.query.filter(Person.fname == fname)
        .filter(Person.lname == lname)
        .one_or_none()
    )

    if update_person is None:
        abort(
            404,
            "Person not found for Id: {person_id}".format(person_id=person_id),
        )

    elif (
        existing_person is not None and existing_person.person_id != person_id
    ):
        abort(
            409,
            "Person {fname} {lname} exists already".format(
                fname=fname, lname=lname
            ),
        )

    else:
        schema = PersonSchema()
        update = schema.load(person, session=db.session)

        update.person_id = update_person.person_id


        db.session.merge(update)
        db.session.commit()

        data = schema.dump(update_person)

        return data, 200


def delete(lname):
    # Get the person requested
    print("at delete first")
    person = Person.query.filter(Person.lname == lname).one_or_none()
    print("at delete second")

    if person is not None:
        db.session.delete(person)
        db.session.commit()
        return make_response(
            "Person {lname} deleted".format(lname=lname), 200
        )

    else:
        abort(
            404,
            "Person not found for Id: {lname}".format(lname=lname),
        )