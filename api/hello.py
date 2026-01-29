"""
Absolute minimal test - no FastAPI, just pure function
"""

def handler(event, context):
    """Minimal lambda handler - no dependencies"""
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': '{"status":"ok","message":"Pure lambda working"}'
    }
