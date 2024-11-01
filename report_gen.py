import pdfkit
from datetime import datetime
import os

def pdf_gen(data):
    # Prepare HTML content for the report
    timestamp = data['time_stamp'].strftime('%Y-%m-%d %H:%M:%S')
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{data['title']}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                color: #333;
            }}
            h1 {{
                color: #4CAF50;
            }}
            h2 {{
                border-bottom: 2px solid #4CAF50;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #4CAF50;
                color: white;
            }}
            tr:hover {{
                background-color: #f1f1f1;
            }}
            .summary {{
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <h1>{data['title']}</h1>
        <p><strong>Report generated on:</strong> {timestamp}</p>

        <h2>Summary</h2>
        <p>Total URLs Checked: <span class="summary">{len(data['urls_checked'])}</span></p>
        <p>Broken Links: <span class="summary">{len(data['broken_links'])}</span></p>
        <p>Validation Issues: <span class="summary">{len(data['validation_issues'])}</span></p>

        <h2>Detailed Report</h2>

        <h3>Checked URLs</h3>
        <table>
            <tr>
                <th>URL</th>
                <th>Status</th>
            </tr>
            {''.join(f"<tr><td>{url}</td><td>{status}</td></tr>" for url, status in data['urls_checked'].items())}
        </table>

        <h3>Broken Links</h3>
        <ul>
            {''.join(f"<li>{link}</li>" for link in data['broken_links'])}
        </ul>

        <h3>Validation Issues</h3>
        <ul>
            {''.join(f"<li>{issue}</li>" for issue in data['validation_issues'])}
        </ul>
    </body>
    </html>
    """
    
    # Create 'reports' directory if it doesn't exist
    os.makedirs('reports', exist_ok=True)

    # Generate PDF from the HTML content and save it in the 'reports' folder
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdfkit.from_string(html_content, f'reports/comprehensive_report_{timestamp_str}.pdf')
