"""Teardown helper for cases where the service decides whether a record exists at teardown.

A declarative teardown step needs an id and exactly one expected status. When the create under
test is rejected there is no id, and when another delete may or may not have removed a record
there is no single expected status. This helper finds records by the run marker the case put
into them and deletes what it finds. Any answer other than success or "nothing there" raises,
so a real cleanup failure is still reported.
"""

_DIGITS_TO_LETTERS = str.maketrans("0123456789", "ghijklmnop")


def delete_marked(http, case, service, collection, field, prefix):
    """Delete every record of /api/<collection> whose <field> starts with <prefix>.

    In <prefix>, {run} stands for the run id and {run_letters} for the run id with its digits
    mapped to letters, the form cases use in names that must not contain digits.
    """
    marker = prefix.format(
        run=case.id_short, run_letters=case.id_short.translate(_DIGITS_TO_LETTERS)
    )
    response = http.get(service, f"/api/{collection}")
    if response.status_code == 404:  # this service answers 404 for an empty collection
        return
    response.raise_for_status()
    for record in response.json():
        if str(record.get(field, "")).startswith(marker):
            http.delete(service, f"/api/{collection}/{record['id']}").raise_for_status()
