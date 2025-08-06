from typing import List


def extract_city_ids(locations: dict) -> List[str]:
    """
    Chuyển thành danh sach city_ids từ locations.
    """
    city_ids = []
    for country in locations.values():
        city_ids.extend(country.keys())
    return city_ids