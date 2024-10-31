from fastapi import FastAPI
from google.cloud import bigquery

app = FastAPI()
client = bigquery.Client()

@app.get("/api/reddit")
async def get_reddit_data():
    query = "SELECT * FROM your_dataset.reddit_table LIMIT 100"
    results = [dict(row) for row in client.query(query)]
    return {"data": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
