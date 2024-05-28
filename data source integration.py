#!/usr/bin/env python
# coding: utf-8

# In[ ]:


pip install mindsdb


# In[ ]:


mkdir mindsdb_datasource_integration
cd mindsdb_datasource_integration
python -m venv venv
source venv/bin/activate 
pip install mindsdb


# In[ ]:


from mindsdb_datasources.datasources.base import SQLDataSource
from mindsdb_datasources import DataSource
from mindsdb_datasources.utilities.types import DSType

@DataSource(name='NewDataSource', ds_type=DSType.RELATIONAL)
class NewDataSource(SQLDataSource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connection = None  # This will be your connection object

    def connect(self):
        # Implement your connection logic here
        self.connection = "Your connection logic"

    def execute(self, query, *args, **kwargs):
        # Execute a query against your data source
        cursor = self.connection.cursor()
        cursor.execute(query, *args)
        return cursor.fetchall()

    def disconnect(self):
        # Close your connection
        self.connection.close()

    def get_schema(self):
        # Return the schema of your data source
        return {"tables": []}  # Modify this to return actual tables and schema

    def to_df(self, query, *args, **kwargs):
        # Convert the result of the query to a DataFrame
        import pandas as pd
        data = self.execute(query, *args)
        df = pd.DataFrame(data)
        return df


# In[ ]:


@DataSource(name='NewDataSource', ds_type=DSType.RELATIONAL)
class NewDataSource(SQLDataSource):
    def __init__(self, host, port, username, password, database, **kwargs):
        super().__init__(**kwargs)
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        # Implement your connection logic here
        import your_datasource_library as ds
        self.connection = ds.connect(
            host=self.host,
            port=self.port,
            user=self.username,
            password=self.password,
            database=self.database
        )


# In[ ]:


if __name__ == '__main__':
    ds = NewDataSource(
        host='localhost',
        port=3306,
        username='root',
        password='password',
        database='test_db'
    )
    ds.connect()
    result = ds.execute('SELECT * FROM your_table LIMIT 10')
    print(result)
    ds.disconnect()


# In[ ]:


from mindsdb_datasources import DataSourceRegistry
from mindsdb_datasources.datasources.new_datasource import NewDataSource

DataSourceRegistry().register(NewDataSource)


# In[ ]:


from mindsdb import Predictor

# Create a new predictor
predictor = Predictor(name='new_datasource_predictor')

# Train the predictor using the new data source
predictor.learn(
    from_data='new_datasource.table_name',
    to_predict='target_column'
)

