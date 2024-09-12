# Crawl Data from YouTube using YouTube API v3

This project uses YouTube API v3 to fetch data from YouTube, including videos and video comments from a specific channel.
## Clone Code

To copy the project's source code to your computer, you can use one of the following commands:
### 1. Using SSH
```bash
git clone git@github.com:lazyboytql/crawl_youtube_first.git
```

### 2. Using HTTP
```bash
https://github.com/lazyboytql/crawl_youtube_first.git
```
## Setting
### 1. Move to project folder
```bash
cd crawl_youtube_first
```
### 2. Create and activate virtual environment (optional)
```bash
python -m venv venv
source venv/bin/activate  # Trên Windows: venv\Scripts\activate
```
### 3. Install related library
```bash
pip install -r requirements.txt
```
## Config 
We can adjust the database information in the file config.py , dockerfile , docker-compose to make the project work.

## Create table 
### 1. Connect to PostgreSQL
First, you need to connect to PostgreSQL via psql, the PostgreSQL command line tool. Open a terminal or command prompt and run the command:
```bash
psql -h localhost -U username -d database_name
```
If you do not have a database, you can do the following:
```bash
CREATE DATABASE database_name;
```
After successfully creating the database, connect to the new database using the following command:
```bash
\c database_name
```
Or connect directly from the terminal:
```bash
psql -h localhost -U username -d database_name
```
### 2. Create table 
Once you're connected to the database, you can create tables by running SQL commands. For example, to create the ```bash youtube_comments ``` table:
```bash
CREATE TABLE youtube_comments (
    id SERIAL PRIMARY KEY,
    video_id VARCHAR(50) NOT NULL,
    author VARCHAR(100),
    comment_text TEXT,
    like_count INT DEFAULT 0,
    published_at TIMESTAMP
);
```
### 3. Check the created table
After successfully creating the table, check the table has been created in the database:
```bash
\dt
```
If you want to see the data in the table, use the command line:
```bash
SELECT * FROM youtube_comments;
```
And finally to exit you use the command:
```bash
\q
```
## Docker
If you want to run the project in a Docker environment, follow these steps:

### 1. Build docker image
```bash
docker-compose build
```
### 2. Run Docker compose
```bash 
docker-compose build
```
