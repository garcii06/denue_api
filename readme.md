# DENUE API
Python client for the INEGI DENUE API. Provides structured access to identification, location, economic activity, and size data for over 5 million businesses nationwide.

Intended uses: 
- Enrich business data from ERP systems.
- Support market analysis and expansion planning for SMEs.

## Project Structure
inegi_py/
├── utils/
│   └── client.py       # DenueClient class
├── main.py             # Entry point
├── .env.example        # Environment variable template
└── README.md

## Endpoints
This API offers the following enpoints:
- Buscar
    - Search by keyword around a coordinate.
- Nombre
    - Seach by business name (razón social).
- BuscarEntidad
    - Keyword search scoped to a specific state.
- BuscarAreaAct
    - Filter by state, municipality, locality, economic sector, subsector, and business size.
- Cuantificar
    - Count establishments by sector, geography, and size tier.
- Ficha
    - Retrieve full profile for a single establishment by ID.

## Setup
1. Clone the repo
2. Install dependencies with uv:
   uv sync
3. Copy .env.example to .env and add your DENUE token:
   DENUE_TOKEN=your_token_here

## Usage
```python
from utils.client import DenueClient
client = DenueClient(token=os.getenv("DENUE_TOKEN"))
results = client.buscar("restaurantes", "21.85,-102.28", "500")
```