import pandas as pd
from django.http import HttpResponse

def export_to_excel(queryset, filename='export.xlsx', columns=None):
    """
    Export a queryset to an Excel file.

    Args:
        queryset: The Django queryset to be exported.
        filename (str): The name of the resulting Excel file.
        columns (dict): A dictionary where keys are model field names and values are the column names in the Excel file.
    """
    # Convert queryset to a list of dictionaries
    data = list(queryset.values(*columns.keys())) if columns else list(queryset.values())

    # Rename columns if specified
    if columns:
        data = [{columns.get(k, k): v for k, v in item.items()} for item in data]
    
    # Create DataFrame
    df = pd.DataFrame(data)

    # Create HTTP response with Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={filename}'

    # Write DataFrame to Excel file in the response
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    return response
