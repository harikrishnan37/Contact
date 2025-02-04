import uuid

from sanic import Sanic
from sanic.response import json, empty

print('Enter the details of the person')

_contacts = [
    {'Id': str(uuid.uuid4()), 'firstName': input(), 'lastName': input(), 'phoneNumber': input(), 'email' : input()}
]

app = Sanic("contacts")


@app.post('/')
async def create_contact(request):
    """Creates a contact"""
    try:
        try:
            contact = request.json
        except:
            raise ValueError
        if contact is None:
            raise ValueError

        id = str(uuid.uuid4())
        contact['Id'] = id

        _contacts.append(contact)

        return empty(201, {'Location': f"/{id}"})
    except ValueError:
        return empty(400)


@app.get('/')
async def get_all_contacts(request):
    """Gets all contacts"""
    return json(_contacts)


@app.get('/<id>')
async def get_contact(request, id):
    """Gets a specific contact"""
    _, contact = find_contact(id)
    if not contact:
        return empty(404)

    return json(contact)


@app.put('/<id>')
async def update_contact(request, id):
    """Updates a contact"""
    i, _ = find_contact(id)
    if i == -1:
        return empty(404)

    try:
        try:
            contact = request.json
        except:
            raise ValueError
        if contact is None:
            raise ValueError

        _contacts[i] = contact
        return empty(204)
    except ValueError:
        return empty(400)


@app.delete('/<id>')
async def delete_contact(request, id):
    """Deletes a contact"""
    i, contact = find_contact(id)
    if not contact:
        return empty(404)

    del _contacts[i]
    return empty(204)


def find_contact(id):
    for i in range(len(_contacts)):
        if _contacts[i]['Id'] == id:
            return i, _contacts[i]
    return -1, None


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8010)
