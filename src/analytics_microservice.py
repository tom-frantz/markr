import math
import statistics
from typing import TypeVar, List

from sqlalchemy.orm import Session

from src.models import Result
from src.schema import Analytics

T = TypeVar("T")


def percentile(data: List[T], percentile: int) -> T:
    return data[math.ceil(percentile / 100 * len(data)) - 1]


def calculate_analytics(test_id: str, db: Session) -> Analytics:
    results = db.query(Result).filter_by(test_id=test_id)

    count = results.count()

    results_as_percent = [result.obtained / result.available for result in results]

    try:
        stddev = statistics.stdev(results_as_percent)
    except statistics.StatisticsError as e:
        stddev = 0.0

    return Analytics(
        mean=statistics.mean(results_as_percent),
        count=count,

        stddev=stddev,
        min=min(results_as_percent),
        max=max(results_as_percent),

        # Calculate percentiles using nearest-rank method
        # https://en.wikipedia.org/wiki/Percentile#The_nearest-rank_method
        p25=percentile(results_as_percent, 25),
        p50=percentile(results_as_percent, 50),
        p75=percentile(results_as_percent, 75),
    )
