1. SELECT * FROM data;

   ```python
   df
   ```

2. SELECT * FROM data LIMIT 10;

   ```python
   df.head(10)
   ```

3. SELECT id FROM data;  //id 是 data 表的特定一列

   ```python
   df['id']
   ```

4. SELECT COUNT(id) FROM data;

   ```python
   df['id'].count()
   ```

5. SELECT * FROM data WHERE id<1000 AND age>30;

   ```python
   df[ (df['id'] < 1000) & (df['age'] > 30) ] 
   ```

6. SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;

   ```python
   df[['id', 'order_id']].drop_duplicates(subset='order_id').groupby('id').count()
   ```

7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;

   ```python
   pd.merge(table1, table2, on='id', how='inner')
   ```

8. SELECT * FROM table1 UNION SELECT * FROM table2;

   ```python
   pd.concat([table1, table2])
   ```

9. DELETE FROM table1 WHERE id=10;

   ```python
   table1[table1['id'] != 10]
   ```

10. ALTER TABLE table1 DROP COLUMN column_name;

    ```python
    table1.drop('column_name', axis=1)
    ```

    