import csv
from sqlalchemy import create_engine, Table, Column, Integer, MetaData

engine = create_engine('sqlite:///data.db', echo=True)
insert_query = "INSERT INTO games (title,platform,score,genre,editors_choice) VALUES (:title, :platform,:score,:genre,:editors_choice)"

with open('dataset.csv', 'r', encoding="utf-8") as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    engine.execute(
        insert_query,
        [{"title": row[0], "platform": row[1],"score": row[2],"genre":row[3],"editors_choice":row[4]} 
            for row in csv_reader]
    )
