from app import create_app, db


def test_ticket_lifecycle(tmp_path):
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": f"sqlite:///{tmp_path / 'test.db'}"})
    client = app.test_client()
    assert client.get("/health").status_code == 200
    assert client.get("/api/tickets").json == []
    response = client.post("/api/tickets", json={"title": "Cannot log in", "priority": "high"})
    assert response.status_code == 201
    ticket_id = response.json["id"]
    assert client.get("/api/tickets").json[0]["title"] == "Cannot log in"
    response = client.patch(f"/api/tickets/{ticket_id}", json={"status": "resolved"})
    assert response.status_code == 200
    assert response.json["status"] == "resolved"
    assert client.post("/api/tickets", json={"title": ""}).status_code == 400
    with app.app_context():
        db.session.remove()
