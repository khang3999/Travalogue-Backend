def avg_rating(rating_summary):
    """
    Tính toán điểm rating trung bình từ ratingSummary.
    """
    total_value = rating_summary.get("totalRatingValue", 0.0)
    total_counter = rating_summary.get("totalRatingCounter", 0.0)
    return total_value / total_counter if total_counter > 0 else 0.0