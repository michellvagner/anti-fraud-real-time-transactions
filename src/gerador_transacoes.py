# %%
import random
import math
import time
from datetime import datetime
from faker import Faker
import requests
import pycountry
import gzip
import json

# %%
fake = Faker()

# %%
def generate_data():

    URL_COUNTRIES = "https://github.com/dr5hn/countries-states-cities-database/releases/latest/download/json-countries+states+cities.json.gz"

    r = requests.get(URL_COUNTRIES)

    return json.loads(gzip.decompress(r.content))

# %%
def generate_location():

    data = generate_data()

    if random.random() < 0.90:
        pais = next(p for p in data if p["iso2"] == "BR")
        estado = random.choice(pais["states"]) if pais["states"] else None
        cidade = random.choice(estado["cities"]) if estado and estado["cities"] else None

        if random.random() < 0.92:
            currency = "986"
        else:
            currency = random.choice([
                c.numeric
                for p in data
                if p["currency"] != "BRL"
                and (c := pycountry.currencies.get(alpha_3=p["currency"]))
            ])

    else:
        pais = random.choice([p for p in data if p["iso2"] != "BR"])
        estado = random.choice(pais["states"]) if pais["states"] else None
        cidade = random.choice(estado["cities"]) if estado and estado["cities"] else None

        if random.random() > 0.92:
            currency = random.choice([
                c.numeric
                for p in data
                if p["currency"] != "BRL"
                and (c := pycountry.currencies.get(alpha_3=p["currency"]))
            ])

        else:
            currency = "986"

    return {
            "country": pais["name"],
            "country_cd": pais["numeric_code"],
            "state": estado["name"] if estado else None,
            "state_code": estado["iso2"] if estado else None,
            "city": cidade["name"] if cidade else None,
            "currency": currency
        }

# %%
def criar_transacao():

    card_number = [
        f"{random.randint(0, 9999999999999999):016d}"
        for _ in range(600)
    ]

    amount = round(random.uniform(1, 100000), 2)
    limit = round(amount * 1.5, 0)
    limit = math.ceil(limit / 1000) * 1000
    card_limit_remaining = round(limit - amount, 2)

    estabelecimentos = [
    f"{random.randint(0, 99999999):08d}"
    for _ in range(300)
    ]
        
    merchant_id = random.choice(estabelecimentos)

    location = generate_location()

    card_brand = random.choice(["V", "M", "E"])

    if card_brand == "V":
        risk_score = f"{random.randint(1, 99):02d}"
    elif card_brand == "M":
        risk_score = f"{random.randint(1, 999):03d}"
    else:
        risk_score = None
    return {
        "transaction_id": fake.uuid4(),
        "bank": random.choice([
            "BANCO_A",
            "BANCO_B",
            "BANCO_C",
            "BANCO_D"
        ]),
        "card_number": random.choice(card_number),
        "trn_dt": datetime.now().isoformat() ,
        "transaction_type": "M" if random.random() < 0.92 else random.choice(["O", "P", "A"]),
        "amount": amount,
        "card_limit_total": limit,
        "card_limit_remaining": card_limit_remaining,
        "process_code": "00" if random.random() < 0.90 else f"{random.randint(1, 99):02d}",
        "num_reason": "000" if random.random() < 0.90 else f"{random.randint(1, 999):03d}",
        "pos_number": "81" if random.random() < 0.55 else random.choice(["01", "10", "05", "07", "90"]),
        "merchant_category_code": f'{random.randint(0, 9999):04d}',
        "currency_cd": location["currency"],
        "transaction_country_cd": location["country_cd"],
        "merchant_id": merchant_id,
        "merchant_name": fake.company(),
        "merchant_state": location["state"],
        "merchant_city": location["city"],
        "authorization_code": f'{random.randint(1, 999999):06d}',
        "acquirer_id": f'{random.randint(1, 99999999):08d}',
        "card_brand": card_brand,
        "risk_score": risk_score,
        "blck_ind": "" if random.random() < 0.92 else random.choice(["F", "P", "R"])
    } 

# %%
def iniciar_simulacao():

    try:
        while True:

            transacao = criar_transacao()

            print(transacao)

            delay = random.uniform(1, 5)

            time.sleep(delay)
    except KeyboardInterrupt:
        print("Simulação interrompida pelo usuário!")

    return transacao

# %%
if __name__ == "__main__":
    iniciar_simulacao()
