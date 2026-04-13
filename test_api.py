import flask
from app import app
import json

with app.test_client() as client:
    # First create a method
    client.post('/api/method', json={"name": "test_method"})
    
    # Send export request with memo
    res = client.post('/api/export-csv', json={
        "map_name": "mapA",
        "agent_count": "5",
        "memo": "MyComment"
    })
    
    # Check headers
    print("Export CSV headers:")
    print(res.headers.get("Content-Disposition"))
    
    res_all = client.post('/api/export-all', json={
        "params": {
            "map_name": "mapA",
            "agent_count": "5",
            "memo": "MyComment"
        }
    })
    print("Export All headers:")
    print(res_all.headers.get("Content-Disposition"))
    print("Export All status:", res_all.status_code)
