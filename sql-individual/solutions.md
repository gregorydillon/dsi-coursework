## Basic Exploration

1. What are the tables in our database?

```
public | events    | table | postgres
public | meals     | table | postgres
public | referrals | table | postgres
public | users     | table | postgres
public | visits    | table | postgres
```

2. What columns?

```
readychef=# \d events
          Table "public.events"
 Column  |       Type        | Modifiers
---------+-------------------+-----------
 dt      | date              |
 userid  | integer           |
 meal_id | integer           |
 event   | character varying |

readychef=# \d meals
          Table "public.meals"
 Column  |       Type        | Modifiers
---------+-------------------+-----------
 meal_id | integer           |
 type    | character varying |
 dt      | date              |
 price   | integer           |

readychef=# \d referrals
     Table "public.referrals"
   Column    |  Type   | Modifiers
-------------+---------+-----------
 referred    | integer |
 referred_by | integer |

readychef=# \d users
            Table "public.users"
   Column    |       Type        | Modifiers
-------------+-------------------+-----------
 userid      | integer           |
 dt          | date              |
 campaign_id | character varying |

readychef=# \d visits
    Table "public.visits"
 Column |  Type   | Modifiers
--------+---------+-----------
 dt     | date    |
 userid | integer |

```

Select statements
===================

1. To get an understanding of the data, run a [SELECT](http://www.postgresqltutorial.com/postgresql-select/) statement on each table. Keep all the columns and limit the number of rows to 10.
  ```sql
  SELECT *
  FROM EVENTS
  LIMIT 10;
  ```

2. Write a `SELECT` statement that would get just the userids.

  ```sql
  select userid from users limit 10;
```

3. Maybe you're just interested in what the campaign ids are. Use 'SELECT DISTINCT' to figure out all the possible values of that column.

  ```sql
  select distinct campaign_id from users;
  ```

Where Clauses / Filtering
========================================

1. Using the `WHERE` clause, write a new `SELECT` statement that returns all rows where `Campaign_ID` is equal to `FB`.
  ```sql
  select * from users where campaign_id='FB';
  ```

2. We don't need the campaign id in the result since they are all the same, so only include the other two columns.
  ```sql
  select userid, dt from users where campaign_id='FB';
  ```

Aggregation Functions
=======================

1. Write a query to get the count of just the users who came from Facebook.
  ```sql
  select count(1) from users where campaign_id='FB';
  ```

2. Now, count the number of users coming from each service. Here you'll have to group by the column you're selecting with a [GROUP BY](http://www.postgresql.org/docs/8.0/static/sql-select.html#SQL-GROUPBY) clause.
  ```sql
  select campaign_id, count(1) from users
  group by campaign_id;
  ```

3. Use `COUNT (DISTINCT columnname)` to get the number of unique dates that appear in the `users` table.
  ```sql
  select count(distinct dt) from users;
  ```

4. There's also `MAX` and `MIN` functions, which do what you might expect. Write a query to get the first and last registration date from the `users` table.
  ```sql
  select min(dt) as min, max(dt) max from users;
  ```

5. Calculate the mean price for a meal (from the `meals` table). You can use the `AVG` function. Your result should look like this:

  ```sql
  select avg(price) from meals;
  ```

6. Now get the average price, the min price and the max price for each meal type. Don't forget the group by statement!

  ```sql
  select
    type,
    avg(price) as avg,
    min(price) as min,
    max(price) as max
  from meals
  group by type;
  ```

7. It's often helpful for us to give our own names to columns. We can always rename columns that we select by doing `AVG(price) AS avg_price`. This is called [aliasing](http://stackoverflow.com/questions/15413735/postgresql-help-me-figure-out-how-to-use-table-aliases). Alias all the above columns so that your table looks like this:
  ```sql
  select
    type,
    avg(price) as avg_price,
    min(price) as min_price,
    max(price) as max_price
  from meals
  group by type;
  ```

8. Maybe you only want to consider the meals which occur in the first quarter (January through March). Use `date_part` to get the month like this: `date_part('month', dt)`. Add a `WHERE` clause to the above query to consider only meals in the first quarter of 2013 (month<=3 and year=2013).
  ```sql
  select
    type,
    avg(price) as avg,
    min(price) as min,
    max(price) as max
  from meals
  where date_part('month', dt) < 3 and date_part('year', dt) = 2013
  group by type;
  ```

9. There are also scenarios where you'd want to group by two columns. Modify the above query so that we get the aggregate values for each month and type. You'll need to add the month to both the select statement and the group by statement.

  ```sql
  select
    type, date_part('month', dt) as month,
    avg(price) as avg,
    min(price) as min,
    max(price) as max
  from meals
  where date_part('year', dt) = 2013
  group by type, month;
  ```

10. From the `events` table, write a query that gets the total number of buys, likes and shares for each meal id.
_Extra_: To avoid having to do this as three separate queries you can do the count of the number of buys like this: `SUM(CASE WHEN event='bought' THEN 1 ELSE 0 END)`.

  ```sql
  select
    meal_id,
    sum(case when event='bought' then 1 else 0 end) as buys,
    sum(case when event='like' then 1 else 0 end) as likes,
    sum(case when event='share' then 1 else 0 end) as share
  from events
  group by meal_id
  order by likes desc;
  ```

Sorting
==========================================

1. Let's start with a query which gets the average price for each type. It will be helpful to alias the average price column as 'avg_price'.
  ```sql
  select
    type,
    avg(price) as avg_price
  from meals
  group by type;
  ```

2. To make it easier to read, sort the results by the `type` column. You can do this with an [ORDER BY](http://www.postgresqltutorial.com/postgresql-order-by/) clause.
  ```sql
  select
    type,
    avg(price) as avg_price
  from meals
  group by type
  order by type;
  ```

3. Now return the same table again, except this time order by the price in descending order (add the `DESC` keyword).
  ```sql
  select
    type,
    avg(price) as avg_price
  from meals
  group by type
  order by type desc;
  ```

3. Sometimes we want to sort by two columns. Write a query to get all the meals, but sort by the type and then by the price. You should have an order by clause that looks something like this: `ORDER BY col1, col2`.

  ```sql
  select
    type,
    price
  from meals
  order by type, price;
  ```

4. For shorthand, people sometimes use numbers to refer to the columns in their order by or group by clauses. The numbers refer to the order they are in the select statement. For instance `SELECT type, dt FROM meals ORDER BY 1;` would order the results by the `type` column.

  > I refuse to do this. From the zen of python: "explicit is better than implicit"


Joins
=========================

Now we are ready to do operations on multiple tables. A [JOIN](http://www.tutorialspoint.com/postgresql/postgresql_using_joins.htm) allows us to combine multiple tables.

1. Write a query to get one table that joins the `events` table with the `users` table (on `userid`) to create the following table.

  ```sql
  select
    u.userid,
    u.campaign_id,
    e.meal_id,
    e.event
  from users u
  join events e on u.userid=e.userid;
  ```

2. Also include information about the meal, like the `type` and the `price`. Only include the `bought` events. The result should look like this:

  ```sql
  select
    u.userid,
    u.campaign_id,
    e.meal_id,
    m.type,
    m.price
  from users u
  join events e on u.userid=e.userid and e.event='bought'
  join meals m on e.meal_id=m.meal_id;
  ```

3. Write a query to get how many of each type of meal were bought.

  ```sql
  select
    m.type,
    count(1) as meals_of_type_bought,
    avg(price) as avg_price_of_meal_type
  from events e
  join meals m on e.meal_id=m.meal_id
  group by m.type;
  ```

Extra Credit (pt. 1)
========================

Subqueries
================================
In a [subquery](http://www.postgresql.org/docs/8.1/static/functions-subquery.html), you have a select statement embedded in another select statement.

1. Write a query to get meals that are above the average meal price.

```sql
  select * from meals where price > (select avg(price) from meals)
```

2. Write a query to get the meals that are above the average meal price *for that type*.

    ```sql
    SELECT meals.*
    FROM meals
    JOIN (SELECT type, avg(price) as avg_price from meals group by type) average
    ON average.type=meals.type and meals.price > average.avg_price
    ```

3. Modify the above query to give a count of the number of meals per type that are above the average price.

    ```sql
    SELECT meals.type, count(1)
    FROM meals
    JOIN (SELECT type, avg(price) as avg_price from meals group by type) average
    ON average.type=meals.type and meals.price > average.avg_price
    group by meals.type;
    ```

4. Calculate the percentage of users which come from each service. This query will look similar to #2 from aggregation functions, except you have to divide by the total number of users.

    Like with many programming languages, dividing an int by an int yields an int, and you will get 0 instead of something like 0.54. You can deal with this by casting one of the values as a real like this: `CAST (value AS REAL)`

    You should get a result like this:

    ```
     campaign_id |      percent
    -------------+-------------------
     RE          | 0.156046343229544
     FB          | 0.396813902968863
     TW          | 0.340695148443157
     PI          | 0.106444605358436
    (4 rows)
    ```

Extra Credit (pt. 2)
========================
1. Answer the question, _"What user from each campaign bought the most items?"_

    It will be helpful to create a temporary table that contains the counts of the number of items each user bought. You can create a table like this: `CREATE TABLE mytable AS SELECT...`

2. For each day, get the total number of users who have registered as of that day. You should get a table that has a `dt` and a `cnt` column. This is a cumulative sum.

3. What day of the week gets meals with the most buys?

4. Which month had the highest percent of users who visited the site purchase a meal?

5. Find all the meals that are above the average price of the previous 7 days.

6. What percent of users have shared more meals than they have liked?

7. For every day, count the number of users who have visited the site and done no action.

8. Find all the dates with a greater than average number of meals.

9. Find all the users who bought a meal before liking or sharing a meal.



### !Challenge
* type: project
* id: sql_individual
* title: sql individual project

#### !Question
Submit the link to your work in github.

##### !end-question

#### !Placeholder
https://github.com/<your username>/...

##### !end-placeholder

#### !Explanation
Solutions will be available [here](solutions/individual/) once they are released.

##### !end-explanation
##### !end-challenge
