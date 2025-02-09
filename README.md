# Sepolia ETH Faucet

A Django REST API application that serves as a faucet for distributing Sepolia ETH to users.

## Features

- Distribute Sepolia ETH to specified wallet addresses
- Rate limiting by IP address and wallet address
- Transaction statistics
- Dockerized deployment
- Comprehensive test coverage
- Code quality tools (Black, isort, flake8)

## Prerequisites

- Docker and Docker Compose
- Sepolia ETH in the source wallet
- Environment variables configured (see .env.example)

## Quick Start
0.
   * Generate ETH private key
   ```bash
   python -c "from web3 import Web3; w3 = Web3(); acc = w3.eth.account.create(); print(f'private key={w3.to_hex(acc.key)}, account={acc.address}')"
   ```
   Default ETH address in env file is 0x666510995bDA5091218D6cb121C07EFea4F42515
   * Request Sepolia tokens
   https://cloud.google.com/application/web3/faucet/ethereum/sepolia

1. Copy `.env.example` to `.env` and fill in your configuration:
   ```bash
   cp .env.example .env
   ```

2. Build and run the application:
   ```bash
   docker compose up --build
   ```

3. Run migrations:
   ```bash
   docker compose exec web make setup
   ```

4. The API will be available at http://localhost:8000

## Configuration

Environment variables:
- `SECRET_KEY`: Django secret key
- `SOURCE_WALLET_PRIVATE_KEY`: Private key of the source wallet
- `WEB3_PROVIDER_URL`: Ethereum node URL (e.g., Infura endpoint)
- `RATE_LIMIT_MINUTES`: Minutes between allowed requests (default: 1)
- `ETH_AMOUNT`: Amount of ETH to send (default: 0.0001)

## API Endpoints

### POST /faucet/fund

Request funds from the faucet.

Request body:
```json
{
    "wallet_address": "0x..."
}
```

Response (success):
```json
{
    "transaction_id": "0x...",
    "message": "Successfully sent 0.0001 Sepolia ETH"
}
```

Response (error):
```json
{
    "error": "Rate limit exceeded. Please try again in X seconds"
}
```

### GET /faucet/stats

Get faucet statistics for the last 24 hours.

Response:
```json
{
    "successful_transactions": 42,
    "failed_transactions": 5
}
```

## Code Quality Tools
### Linters
Run all linting tools (flake8, black --check, isort --check)
```bash
docker compose exec web make lint
```

### Formatters
Format code using black and isort
```bash
docker compose exec web make format
```

## Tests
### Running the tests
Application is covered with unit tests. To run the tests:
```bash
docker compose exec web make test
```

### Generating the coverage
Generate coverage report:
```bash
docker compose exec web make coverage
```