from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
from datetime import datetime

app = FastAPI(
    title="Japan Employment API",
    description="Japan employment data including unemployment rate, labor force participation, wages, part-time employment, and job openings. Powered by World Bank Open Data.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

WB_BASE_URL = "https://api.worldbank.org/v2/country/JP/indicator"

INDICATORS = {
    "unemployment":      {"id": "SL.UEM.TOTL.ZS",   "name": "Unemployment Rate",                  "unit": "% of Labor Force"},
    "youth_unemp":       {"id": "SL.UEM.1524.ZS",   "name": "Youth Unemployment Rate",             "unit": "% of Labor Force ages 15-24"},
    "labor_force":       {"id": "SL.TLF.TOTL.IN",   "name": "Total Labor Force",                   "unit": "Persons"},
    "participation":     {"id": "SL.TLF.CACT.ZS",   "name": "Labor Force Participation Rate",      "unit": "% of Population 15+"},
    "female_partici":    {"id": "SL.TLF.CACT.FE.ZS","name": "Female Labor Force Participation",    "unit": "% of Female Population 15+"},
    "wage_growth":       {"id": "SL.EMP.WORK.ZS",   "name": "Wage & Salaried Workers",             "unit": "% of Total Employment"},
    "employment_agri":   {"id": "SL.AGR.EMPL.ZS",   "name": "Employment in Agriculture",           "unit": "% of Total Employment"},
    "employment_industry":{"id": "SL.IND.EMPL.ZS",  "name": "Employment in Industry",              "unit": "% of Total Employment"},
    "employment_service":{"id": "SL.SRV.EMPL.ZS",   "name": "Employment in Services",              "unit": "% of Total Employment"},
    "self_employed":     {"id": "SL.EMP.SELF.ZS",   "name": "Self-Employed Workers",               "unit": "% of Total Employment"},
}


async def fetch_wb(indicator_id: str, limit: int = 10):
    url = f"{WB_BASE_URL}/{indicator_id}"
    params = {"format": "json", "mrv": limit, "per_page": limit}
    async with httpx.AsyncClient(timeout=15) as client:
        res = await client.get(url, params=params)
        data = res.json()
    if not data or len(data) < 2:
        return []
    records = data[1] or []
    return [
        {"year": str(r["date"]), "value": r["value"]}
        for r in records
        if r.get("value") is not None
    ]


@app.get("/")
def root():
    return {
        "api": "Japan Employment API",
        "version": "1.0.0",
        "provider": "GlobalData Store",
        "source": "World Bank Open Data",
        "country": "Japan (JP)",
        "endpoints": [
            "/summary", "/unemployment", "/youth-unemployment", "/labor-force",
            "/participation", "/female-participation", "/wages",
            "/by-sector", "/self-employed"
        ],
        "updated_at": datetime.utcnow().isoformat() + "Z",
    }


@app.get("/summary")
async def summary(limit: int = Query(default=5, ge=1, le=30)):
    """All Japan employment indicators snapshot"""
    results = {}
    for key, meta in INDICATORS.items():
        results[key] = await fetch_wb(meta["id"], limit)
    formatted = {
        key: {
            "name": INDICATORS[key]["name"],
            "unit": INDICATORS[key]["unit"],
            "data": results[key],
        }
        for key in INDICATORS
    }
    return {
        "country": "Japan",
        "country_code": "JP",
        "source": "World Bank Open Data",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "indicators": formatted,
    }


@app.get("/unemployment")
async def unemployment(limit: int = Query(default=10, ge=1, le=60)):
    """Japan unemployment rate (% of labor force)"""
    data = await fetch_wb("SL.UEM.TOTL.ZS", limit)
    return {"indicator": "Unemployment Rate", "series_id": "SL.UEM.TOTL.ZS", "unit": "% of Labor Force", "frequency": "Annual", "country": "Japan", "source": "World Bank", "updated_at": datetime.utcnow().isoformat() + "Z", "data": data}


@app.get("/youth-unemployment")
async def youth_unemployment(limit: int = Query(default=10, ge=1, le=60)):
    """Japan youth unemployment rate (ages 15-24)"""
    data = await fetch_wb("SL.UEM.1524.ZS", limit)
    return {"indicator": "Youth Unemployment Rate", "series_id": "SL.UEM.1524.ZS", "unit": "% of Labor Force ages 15-24", "frequency": "Annual", "country": "Japan", "source": "World Bank", "updated_at": datetime.utcnow().isoformat() + "Z", "data": data}


@app.get("/labor-force")
async def labor_force(limit: int = Query(default=10, ge=1, le=60)):
    """Japan total labor force (persons)"""
    data = await fetch_wb("SL.TLF.TOTL.IN", limit)
    return {"indicator": "Total Labor Force", "series_id": "SL.TLF.TOTL.IN", "unit": "Persons", "frequency": "Annual", "country": "Japan", "source": "World Bank", "updated_at": datetime.utcnow().isoformat() + "Z", "data": data}


@app.get("/participation")
async def participation(limit: int = Query(default=10, ge=1, le=60)):
    """Japan labor force participation rate (% of population 15+)"""
    data = await fetch_wb("SL.TLF.CACT.ZS", limit)
    return {"indicator": "Labor Force Participation Rate", "series_id": "SL.TLF.CACT.ZS", "unit": "% of Population 15+", "frequency": "Annual", "country": "Japan", "source": "World Bank", "updated_at": datetime.utcnow().isoformat() + "Z", "data": data}


@app.get("/female-participation")
async def female_participation(limit: int = Query(default=10, ge=1, le=60)):
    """Japan female labor force participation rate"""
    data = await fetch_wb("SL.TLF.CACT.FE.ZS", limit)
    return {"indicator": "Female Labor Force Participation", "series_id": "SL.TLF.CACT.FE.ZS", "unit": "% of Female Population 15+", "frequency": "Annual", "country": "Japan", "source": "World Bank", "updated_at": datetime.utcnow().isoformat() + "Z", "data": data}


@app.get("/wages")
async def wages(limit: int = Query(default=10, ge=1, le=60)):
    """Wage and salaried workers as % of total employment"""
    data = await fetch_wb("SL.EMP.WORK.ZS", limit)
    return {"indicator": "Wage & Salaried Workers", "series_id": "SL.EMP.WORK.ZS", "unit": "% of Total Employment", "frequency": "Annual", "country": "Japan", "source": "World Bank", "updated_at": datetime.utcnow().isoformat() + "Z", "data": data}


@app.get("/by-sector")
async def by_sector(limit: int = Query(default=10, ge=1, le=60)):
    """Japan employment by sector: agriculture, industry, services"""
    agri = await fetch_wb("SL.AGR.EMPL.ZS", limit)
    ind = await fetch_wb("SL.IND.EMPL.ZS", limit)
    serv = await fetch_wb("SL.SRV.EMPL.ZS", limit)
    return {
        "country": "Japan",
        "source": "World Bank",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "agriculture": {"series_id": "SL.AGR.EMPL.ZS", "unit": "% of Total Employment", "data": agri},
        "industry": {"series_id": "SL.IND.EMPL.ZS", "unit": "% of Total Employment", "data": ind},
        "services": {"series_id": "SL.SRV.EMPL.ZS", "unit": "% of Total Employment", "data": serv},
    }


@app.get("/self-employed")
async def self_employed(limit: int = Query(default=10, ge=1, le=60)):
    """Self-employed workers as % of total employment"""
    data = await fetch_wb("SL.EMP.SELF.ZS", limit)
    return {"indicator": "Self-Employed Workers", "series_id": "SL.EMP.SELF.ZS", "unit": "% of Total Employment", "frequency": "Annual", "country": "Japan", "source": "World Bank", "updated_at": datetime.utcnow().isoformat() + "Z", "data": data}
