"""Tests for the user."""
from fm_database.models.user import User


def test_get_user(client, dbsession, user, admin_headers):
    """Test GET User."""
    # test 404
    rep = client.get("/api/v1/users/100000", headers=admin_headers)
    assert rep.status_code == 404

    dbsession.add(user)
    dbsession.commit()

    # test get_user
    rep = client.get("/api/v1/users/%d" % user.id, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()["user"]
    print(data)
    assert data["username"] == user.username
    assert data["email"] == user.email
    assert data["active"] == user.active


def test_put_user(client, dbsession, user, admin_headers):
    """Test PUT User."""
    # test 404
    rep = client.put("/api/v1/users/100000", headers=admin_headers)
    assert rep.status_code == 404

    dbsession.add(user)
    dbsession.commit()

    data = {"username": "updated"}

    # test update user
    rep = client.put("/api/v1/users/%d" % user.id, json=data, headers=admin_headers)
    assert rep.status_code == 200

    data = rep.get_json()["user"]
    assert data["username"] == "updated"
    assert data["email"] == user.email
    assert data["active"] == user.active


def test_delete_user(client, dbsession, user, admin_headers):
    """Test DELETE User."""
    # test 404
    rep = client.put("/api/v1/users/100000", headers=admin_headers)
    assert rep.status_code == 404

    dbsession.add(user)
    dbsession.commit()

    # test get_user
    user_id = user.id
    rep = client.delete("/api/v1/users/%d" % user_id, headers=admin_headers)
    assert rep.status_code == 200
    assert dbsession.query(User).filter_by(id=user_id).first() is None


def test_create_user(client, dbsession, admin_headers):
    """Test POST User."""
    # test bad data
    data = {"username": "created"}
    rep = client.post("/api/v1/users", json=data, headers=admin_headers)
    assert rep.status_code == 422

    data["password"] = "admin"
    data["email"] = "create@mail.com"

    rep = client.post("/api/v1/users", json=data, headers=admin_headers)
    assert rep.status_code == 201

    data = rep.get_json()
    user = dbsession.query(User).filter_by(id=data["user"]["id"]).first()

    assert user.username == "created"
    assert user.email == "create@mail.com"


def test_get_all_user(client, dbsession, user_factory, admin_headers):
    """Test GET all Users."""
    users = user_factory.create_batch(30)

    dbsession.add_all(users)
    dbsession.commit()

    rep = client.get("/api/v1/users", headers=admin_headers)
    assert rep.status_code == 200

    results = rep.get_json()
    for user in users:
        assert any(u["id"] == user.id for u in results["results"])
