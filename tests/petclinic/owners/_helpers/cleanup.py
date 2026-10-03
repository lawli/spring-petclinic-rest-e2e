"""Teardown helpers for owner cases where the service decides what still exists at teardown.

A declarative teardown step needs an id and exactly one expected status. These cases cannot give
either: a create that the service may reject returns no id, and an owner delete may or may not
have removed the pet type with it. Both helpers find records by the run marker the cases put into
them and delete what they find. Any answer other than success or "nothing there" raises, so a
real cleanup failure is still reported.
"""


def _listed(http, service, path):
    response = http.get(service, path)
    if response.status_code == 404:  # this service answers 404 for an empty collection
        return []
    response.raise_for_status()
    return response.json()


def delete_owners_of_run(http, case, service):
    """Delete every owner whose address starts with this run's marker."""
    marker = f"apitest-{case.id_short} "
    for owner in _listed(http, service, "/api/owners"):
        if owner["address"].startswith(marker):
            http.delete(service, f"/api/owners/{owner['id']}").raise_for_status()


def delete_pet_type_of_run(http, case, service):
    """Delete the pet type named after this run, if the service still has it."""
    name = f"apitest-type-{case.id_short}"
    for pet_type in _listed(http, service, "/api/pettypes"):
        if pet_type["name"] == name:
            http.delete(service, f"/api/pettypes/{pet_type['id']}").raise_for_status()
