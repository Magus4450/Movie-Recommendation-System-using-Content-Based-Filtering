# Movie Recommendation API using Content Based Filtering



## Technologies Used
- **Elastic Search**
- **FastAPI**
- **SBERT**
- **NLTK**

---

## Steps to run
1. Make a virtual environment with python 3.10.2
    ```bash
    python3.10.2 -m venv {env_name}
    ```

2. Run virtual env and install dependencies
    ```bash
    ./{env_name}/Scripts/activate // for windows
    source {env_name}/bin/activate // for linux

    pip install -r requirements.txt
    ```

3. Create a .env file to store environment variables. Add following variables 
    ```bash
    ELASTICSEARCH_USERNAME = {username}
    ELASTICSEARCH_PASSWORD = {password}
    ```

4. Create docker containers for elastic search and kibana.
    ```bash
    docker-compose up
    ```

5. Index data in elastic search. Run all the cells of *elastic_indexing.ipnyb*

6. Run FastAPI server
    ```bash
    uvicorn app:app
    ```

7. Go to http://localhost:8000/docs to test the API.


