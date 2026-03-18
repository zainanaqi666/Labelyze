import requests

DAILYMED_SEARCH_URL = "https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json"
DAILYMED_LABEL_URL  = "https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/{}.json"


def search_drug(drug_name):
    """
    Search DailyMed for a drug by name.
    Returns the first matching label's set ID, or None if not found.
    """
    try:
        response = requests.get(
            DAILYMED_SEARCH_URL,
            params={"drug_name": drug_name, "pagesize": 1},
            timeout=10
        )
        data = response.json()
        results = data.get("data", [])
        if results:
            return results[0].get("setid")
        return None
    except Exception as e:
        print(f"DailyMed search error: {e}")
        return None


def fetch_label_text(set_id):
    """
    Fetches the full label text for a given set ID.
    Returns extracted section text as a plain string.
    """
    try:
        response = requests.get(
            DAILYMED_LABEL_URL.format(set_id),
            timeout=10
        )
        data = response.json()
        sections = data.get("data", {}).get("spl_medguide", "")
        if not sections:
            sections_raw = data.get("data", {}).get("spl_product_data_elements", "")
            sections = sections_raw if sections_raw else ""
        return sections
    except Exception as e:
        print(f"DailyMed fetch error: {e}")
        return ""


def get_reference_label(drug_name):
    """
    Main entry point for FDA mode.
    Pass a drug name, get back reference label text.
    """
    print(f"Searching DailyMed for: {drug_name}...")
    set_id = search_drug(drug_name)
    if not set_id:
        print("Drug not found on DailyMed.")
        return None
    print(f"Found label ID: {set_id}. Fetching label...")
    return fetch_label_text(set_id)
