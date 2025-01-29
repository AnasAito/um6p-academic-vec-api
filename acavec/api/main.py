from fastapi import FastAPI, Query
from typing import Optional, List
from pydantic import BaseModel
import time
import lancedb
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    global table
    # Initialize LanceDB
    uri = "./data/acavec-lancedb"
    db = lancedb.connect(uri)
    table = db.open_table("works")
    # first cold run
    table.search("ocp").to_polars().select([
        "id", "title", "abstract", "publication_year", "language", "type",
        "countries_distinct_count", "institutions_distinct_count", "cited_by_count",
        "locations_count", "_distance"
    ]).to_dicts()

# Define response model


class QueryResult(BaseModel):
    id: str
    title: str
    abstract: Optional[str]
    publication_year: Optional[int]
    language: Optional[str]
    type: Optional[str]
    countries_distinct_count: Optional[int]
    institutions_distinct_count: Optional[int]
    cited_by_count: Optional[int]
    locations_count: Optional[int]
    referenced_works_count: Optional[int]
    # authorships_author_display_name: Optional[List[str]]
    # authorships_countries: Optional[List[str]]
    # topics_display_name: Optional[List[str]]
    # keywords_display_name: Optional[List[str]]
    # concepts_display_name: Optional[List[str]]
    _distance: float


@app.get("/search", response_model=List[QueryResult])
async def search(
    query: str = Query(..., description="Search query"),
    items_count: int = Query(20, description="Number of items to retrieve"),
    # sort_key: Optional[str] = Query(None, description="Sort key"),
    # is_ascending: Optional[bool] = Query(True, description="Sort order")
):
    """Search the database with the provided query."""
    cols_to_select = [
        "id", "title", "abstract", "publication_year", "language", "type",
        "countries_distinct_count", "institutions_distinct_count", "cited_by_count",
        "locations_count", "referenced_works_count", "_distance"
    ]

    # Execute the query
    time_start = time.time()
    df = (
        table.search(query)
        .limit(items_count)
        .to_polars().select(cols_to_select)
    )
    time_end = time.time()

    # Prepare the results
    results = df.to_dicts()
    formatted_results = [
        {
            "id": item["id"],
            "title": item["title"],
            "abstract": item["abstract"],
            "publication_year": item["publication_year"],
            "language": item["language"],
            "type": item["type"],
            "countries_distinct_count": item["countries_distinct_count"],
            "institutions_distinct_count": item["institutions_distinct_count"],
            "cited_by_count": item["cited_by_count"],
            "locations_count": item["locations_count"],
            "referenced_works_count": item["referenced_works_count"],
            # "authorships_author_display_name": item["authorships_author_display_name"],
            # "authorships_countries": item["authorships_countries"],
            # "topics_display_name": item["topics_display_name"],
            # "keywords_display_name": item["keywords_display_name"],
            # "concepts_display_name": item["concepts_display_name"],
            "_distance": item["_distance"],
        }
        for item in results
    ]

    print(f"Query executed in {time_end - time_start:.2f} seconds")
    return formatted_results
