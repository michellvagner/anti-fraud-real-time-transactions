from src.gerador_transacoes import generate_location


def test_generate_location():
    location = generate_location()

    assert location["country"] is None 
    assert location["country_cd"] is not None 
    assert location["currency"] is not None