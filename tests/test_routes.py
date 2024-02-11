def test_route_invalid(client):
    response = client.get("/abcde")
    assert response.status_code == 404


def test_index_valid(client):
    response = client.get("/")
    assert response.status_code == 200


def test_about_valid(client):
    response = client.get("/about/")
    assert response.status_code == 200


def test_contact_valid(client):
    response = client.get("/contact/")
    assert response.status_code == 200


def test_help_valid(client):
    response = client.get("/help/")
    assert response.status_code == 200


def test_processing_valid(client):
    response = client.get("/analysis/job_submitted/")
    assert response.status_code == 200


def test_results_example_valid(client):
    response = client.get("/results/example/")
    assert response.status_code == 200
