"""
CSV export utilities.

This module provides a reusable function that converts database query
results into a downloadable CSV file. It supports:
- SQLAlchemy ORM objects
- SQLAlchemy Row objects
- Tuples or lists

Keeping this logic in one place avoids duplication across API endpoints.
"""

import csv
from io import StringIO
from fastapi.responses import Response


def generate_csv_response(rows, headers, filename: str) -> Response:
    """
    Convert query results into a CSV file and return it as an HTTP response.

    Args:
        rows: Iterable of rows (ORM objects, Row objects, tuples, or lists)
        headers: List of column names for the CSV header
        filename: Name of the CSV file returned to the caller

    Returns:
        FastAPI Response containing CSV data
    """

    # Create an in-memory text buffer to hold CSV content
    buffer = StringIO()

    # Create a CSV writer using Python's standard library
    writer = csv.writer(buffer)

    # Write the header row
    writer.writerow(headers)

    # Write each row of data
    for row in rows:

        # Case 1: SQLAlchemy Row object (row._mapping)
        if hasattr(row, "_mapping"):
            writer.writerow([row._mapping[h] for h in headers])

        # Case 2: ORM object (attributes)
        elif hasattr(row, "__dict__"):
            writer.writerow([getattr(row, h) for h in headers])

        # Case 3: Tuple or list
        elif isinstance(row, (tuple, list)):
            writer.writerow(list(row))

        # Fallback: convert unknown types to string
        else:
            writer.writerow([str(row)])

    # Return the CSV as an HTTP response with download headers
    return Response(
        content=buffer.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
