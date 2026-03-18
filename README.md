# Japan Employment API

Japan employment data including unemployment rate, youth unemployment, labor force size, participation rates, female labor participation, employment by sector, wages, and self-employment. Powered by World Bank Open Data.

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | API info and available endpoints |
| `GET /summary` | All employment indicators snapshot |
| `GET /unemployment` | Unemployment rate |
| `GET /youth-unemployment` | Youth unemployment (ages 15-24) |
| `GET /labor-force` | Total labor force |
| `GET /participation` | Labor force participation rate |
| `GET /female-participation` | Female labor participation rate |
| `GET /wages` | Wage & salaried workers |
| `GET /by-sector` | Employment by sector (agri/industry/services) |
| `GET /self-employed` | Self-employed workers |

## Data Source

World Bank Open Data
https://data.worldbank.org/country/JP

## Authentication

Requires `X-RapidAPI-Key` header via RapidAPI.
