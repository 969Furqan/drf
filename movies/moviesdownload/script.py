import csv
import requests
from datetime import datetime
from typing import Any
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# --- Base query with a year placeholder ---
BASE_QUERY = """
SELECT ?film ?filmLabel
(GROUP_CONCAT(DISTINCT ?genreLabel; separator = ", ") AS ?genres)
(GROUP_CONCAT(DISTINCT ?countryLabel; separator = ", ") AS ?countries)
(GROUP_CONCAT(DISTINCT ?directorLabel; separator = ", ") AS ?directors)
WHERE {{
  ?film wdt:P31 wd:Q11424;
        wdt:P577 ?releaseDate.
  FILTER(YEAR(?releaseDate) = {year})

  OPTIONAL {{
    ?film wdt:P136 ?genre.
    ?genre rdfs:label ?genreLabel.
    FILTER(LANG(?genreLabel) = "en")
  }}
  OPTIONAL {{
    ?film wdt:P495 ?country.
    ?country rdfs:label ?countryLabel.
    FILTER(LANG(?countryLabel) = "en")
  }}
  OPTIONAL {{
    ?film wdt:P57 ?director.
    ?director rdfs:label ?directorLabel.
    FILTER(LANG(?directorLabel) = "en")
  }}
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
}}
GROUP BY ?film ?filmLabel
LIMIT {limit} OFFSET {offset}
"""


# --- Setup session with retry ---
session = requests.Session()
retries = Retry(
    total=5, 
    backoff_factor=2, 
    status_forcelist=[429, 500, 502, 503, 504]
)
session.mount("https://", HTTPAdapter(max_retries=retries))

def fetch_by_year(year: int, limit: int = 500) -> list[dict[str, Any]]:
    data = []
    offset = 0

    while True:
        query = BASE_QUERY.format(year=year, limit=limit, offset=offset)
        url = "https://query.wikidata.org/sparql"

        try:
            response = session.get(
                url,
                headers={"Accept": "application/sparql-results+json", "User-Agent": "MoviesCollectorBot/1.0"},
                params={"query": query},
                timeout=30
            )
            response.raise_for_status()
            results = response.json().get("results", {}).get("bindings", [])
            if not results:
                break
            data.extend(results)
            offset += limit
        except requests.exceptions.ReadTimeout:
            print(f"Timeout fetching {year}, offset={offset}. Skipping batch.")
            break
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {year}, offset={offset}: {e}")
            break

    return data


def fetch_all_data() -> None:
    current_year = datetime.now().year
    all_data = []

    for year in tqdm(range(1888, current_year + 1), desc="Fetching movies by year"):
        yearly_data = fetch_by_year(year)
        if yearly_data:
            all_data.extend(yearly_data)

    csv_file_name = f"movies_data_1888_to_{current_year}.csv"
    with open(csv_file_name, mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["film", "title", "genres", "countries", "directors"])

        for item in all_data:
            writer.writerow([
                item.get("film", {}).get("value", ""),
                item.get("filmLabel", {}).get("value", ""),
                item.get("genres", {}).get("value", ""),
                item.get("countries", {}).get("value", ""),
                item.get("directors", {}).get("value", "")
            ])

    print(f"Saved all data to {csv_file_name}")


if __name__ == "__main__":
    fetch_all_data()
