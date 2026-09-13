# Anti-Fraud Real-Time Transactions

Gerador de transações financeiras para simular eventos de pagamento e movimentações em diferentes localidades, servindo como fonte de dados para uma plataforma de prevenção a fraudes em tempo real.

O projeto gera transações sintéticas com informações de localização, moeda e data/hora, permitindo alimentar testes, pipelines de dados e componentes de detecção de fraude.

## Objetivo

Este projeto foi criado para gerar dados sintéticos de transações de forma simples e reproduzível, evitando a necessidade de utilizar dados reais de clientes.

A geração de localização utiliza a base pública **Countries, States and Cities Database**, mantendo a hierarquia:

```text
País
 └── Estado
      └── Cidade
```

## Funcionamento

Para cada transação, o gerador:

1. Seleciona aleatoriamente um país.
2. Seleciona um estado desse país, quando disponível.
3. Seleciona uma cidade desse estado, quando disponível.
4. Define a moeda da transação.
5. Registra o timestamp utilizando o fuso horário `America/Sao_Paulo`.
6. Retorna os dados da localização para composição da transação.

A maior parte das transações utiliza **BRL**, simulando um cenário predominantemente brasileiro, enquanto uma parcela menor utiliza moedas internacionais reconhecidas.

## Exemplo de localização gerada

```json
{
  "country": "Brazil",
  "country_cd": "076",
  "state": "São Paulo",
  "state_code": "SP",
  "city": "Carapicuíba",
  "currency": "BRL"
}
```

Os valores acima são apenas um exemplo. Os dados reais são escolhidos aleatoriamente durante a execução.

## Estrutura do projeto

```text
anti-fraud-real-time-transactions/
├── src/
│   ├── __init__.py
│   └── gerador_transacoes.py
├── tests/
│   └── test_location.py
├── scripts/
│   ├── api.ipynb
│   └── gerador_transacoes.ipynb
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── relock-release.yml
├── Dockerfile
├── pyproject.toml
└── uv.lock
```

## Tecnologias

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- Faker
- PyCountry
- Requests
- Pytest
- Ruff
- Docker
- GitHub Actions
- GitHub Container Registry (GHCR)

## Executando localmente

### Pré-requisitos

Tenha instalado:

- Python 3.11 ou superior
- `uv`
- Docker (opcional)

### Instalar dependências

Na raiz do projeto:

```bash
uv sync
```

### Executar o gerador

```bash
uv run python src/gerador_transacoes.py
```

## Testes

Para executar os testes:

```bash
uv run python -m pytest
```

## Qualidade de código

O projeto utiliza **Ruff** para lint e formatação.

Verificar lint:

```bash
uv run ruff check .
```

Verificar formatação:

```bash
uv run ruff format --check .
```

## Docker

A aplicação também pode ser executada em um container.

### Build

```bash
docker build -t anti-fraud-real-time-transactions .
```

### Executar

```bash
docker run --rm anti-fraud-real-time-transactions
```

## CI/CD

O projeto utiliza GitHub Actions para automatizar o ciclo de integração e entrega.

O pipeline executa:

```text
Push / Pull Request
        │
        ▼
      CI
        │
        ├── Ruff
        ├── Pytest
        └── Docker Build
                │
                ▼
               GHCR
```

As imagens Docker são publicadas no GitHub Container Registry com:

- `latest`
- SHA do commit
- versão da release, por exemplo `v1.2.0`

O versionamento das releases é gerenciado automaticamente pelo **Release Please**.

## Imagem Docker

A imagem publicada está disponível no GitHub Container Registry:

```text
ghcr.io/michellvagner/anti-fraud-real-time-transactions
```

Exemplo:

```bash
docker pull ghcr.io/michellvagner/anti-fraud-real-time-transactions:v1.2.0
```

## Fonte dos dados de localização

A base de países, estados e cidades utilizada pelo gerador é disponibilizada pelo projeto:

**Dr5hn Countries, States and Cities Database**

Arquivo utilizado:

```text
json-countries+states+cities.json.gz
```

URL utilizada pelo projeto:

```text
https://github.com/dr5hn/countries-states-cities-database/releases/latest/download/json-countries+states+cities.json.gz
```

## Próximos passos

O gerador foi desenvolvido como uma fonte de dados para uma arquitetura maior de prevenção a fraudes.

A evolução natural do projeto é utilizar as transações geradas para alimentar componentes de processamento e detecção de fraude, incluindo execução em ambiente cloud.

---

**Projeto:** Anti-Fraud Real-Time Transactions  
**Autor:** Vagner Michell
