import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine


if __name__ == '__main__':
    engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
    # local = /workspaces/de-zoomcamp-work/data/yellow_tripdata_2021-01.parquet
    parquet_file = pq.ParquetFile('/app/data/yellow_tripdata_2021-01.parquet')

    batch_size = 100000

    first_batch = True
    rows = 0

    for batch in parquet_file.iter_batches(batch_size=batch_size):
        df_batch = batch.to_pandas()

        if first_batch :
            df_batch.to_sql('ny_taxi_data', engine, if_exists='replace', index=False)
            first_batch = False
            print(f"Created table with first batch: {len(df_batch)} rows")
        else:
            df_batch.to_sql('ny_taxi_data', engine, if_exists='append', index=False)
            print(f"Inserted batch: {len(df_batch)} rows")

        rows += len(df_batch)

    print(f"Total rows inserted: {rows}")