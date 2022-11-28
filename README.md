# Movie Recommendation API using Content Based Filtering



## Technologies Used
- **Docker**
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

3. Create a .secrets.toml file to store environment variables. Add following variables 
    ```bash
    elastic_username = "{username}"
    elastic_password = "{password}"
    ```

4. Create docker containers for elastic search and kibana.
    ```bash
    docker-compose up
    ```

5. Index data in elastic search. 
    ```bash
    python ElasticIndexer.py
    ```

6. Run FastAPI server
    ```bash
    uvicorn app:app
    ```

7. Go to http://localhost:8000/docs to test the API.



---

## How It Works


**Content Based Filtering** is a type of recommendation generation system that used metadata of an item to find other similar items. The metadata for a movie would be its title, plot, cast, directors, genre, and so on. The metadata is then used to create a single document by combing them. The document in then encoded to a vector which represents that movie in the latent space. To generate recommendations for user that has liked a particular movie, the similarity is computed between that movie vector with all other movie vector. Most similar movie vectors can then be recommended to the users.

## Outputs

- Input: *The Lion King*

![The Lion King](/Screenshots/the_lion_king.png)

- Input: *Space Aliens*

![Space Aliens](/Screenshots/space_aliens.png)

