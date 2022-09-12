from webapp.models.enums import Server


def test_server_enum():
    assert len(Server) == 2
    assert Server.to_dict(Server.luxplena) == {"value": 0, "name": "LuxPlena"}
    assert Server.to_dict(Server.bergruen) == {"value": 1, "name": "Bergruen"}
