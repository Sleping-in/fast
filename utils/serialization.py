"""
Utility functions for serializing FastF1 data to JSON-compatible formats.
Optimized for Swift app consumption.
"""
import pandas as pd
from datetime import datetime
from typing import Any, Dict, List, Optional
import numpy as np


def datetime_to_iso8601(dt: Any) -> Optional[str]:
    """Convert datetime to ISO 8601 format string (Swift-compatible)."""
    if pd.isna(dt) or dt is None:
        return None
    
    if isinstance(dt, pd.Timestamp):
        dt = dt.to_pydatetime()
    
    if isinstance(dt, datetime):
        return dt.isoformat()
    
    return str(dt)


def clean_numeric(value: Any) -> Optional[float]:
    """Convert numeric value, handling NaN and None."""
    if pd.isna(value) or value is None:
        return None
    
    if isinstance(value, (int, float)):
        if np.isnan(value):
            return None
        return float(value)
    
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def dataframe_to_dict_list(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Convert Pandas DataFrame to list of dictionaries.
    Handles datetime serialization and NaN values for Swift compatibility.
    """
    if df is None or df.empty:
        return []
    
    # Replace NaN with None for JSON serialization
    df = df.replace({np.nan: None})
    
    # Convert to dict records
    records = df.to_dict('records')
    
    # Process each record to handle datetime and numeric types
    result = []
    for record in records:
        processed = {}
        for key, value in record.items():
            # Handle datetime columns
            if isinstance(value, (pd.Timestamp, datetime)):
                processed[key] = datetime_to_iso8601(value)
            # Handle numeric columns
            elif isinstance(value, (int, float, np.number)):
                processed[key] = clean_numeric(value)
            # Handle other types
            else:
                processed[key] = value if value is not None else None
        
        result.append(processed)
    
    return result


def series_to_dict(series: pd.Series) -> Dict[str, Any]:
    """Convert Pandas Series to dictionary."""
    if series is None or series.empty:
        return {}
    
    result = {}
    for key, value in series.items():
        if isinstance(value, (pd.Timestamp, datetime)):
            result[key] = datetime_to_iso8601(value)
        elif isinstance(value, (int, float, np.number)):
            result[key] = clean_numeric(value)
        else:
            result[key] = value if not pd.isna(value) else None
    
    return result

