queries = {
    "validate": "SELECT 1",
    "schema_condition": """AND UPPER(T.TABLE_SCHEMA) = UPPER('<schema_name>')""",
    "schema_by_database": """SELECT DISTINCT TABLE_SCHEMA AS [SCHEMA] FROM INFORMATION_SCHEMA.TABLES   
                                WHERE UPPER(TABLE_CATALOG) = UPPER('<database_name>')""",
    "attributes": """
        SELECT T.COLUMN_NAME, T.DATA_TYPE AS DATATYPE, '' AS DESCRIPTION
        ,T.TABLE_SCHEMA AS [SCHEMA]
        FROM INFORMATION_SCHEMA.COLUMNS T
        WHERE UPPER(T.TABLE_NAME) = UPPER('<table_name>') <schema_condition>
    """,
    "primary_key": """ SELECT T.COLUMN_NAME
                    FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE T
                    WHERE OBJECTPROPERTY(OBJECT_ID(T.CONSTRAINT_SCHEMA + '.' + QUOTENAME(T.CONSTRAINT_NAME)), 'IsPrimaryKey') = 1
                    AND UPPER(T.TABLE_NAME) = UPPER('<table_name>')  <schema_condition> """,
    "tables": """
        ;with tablelist as
        (
            Select T.TABLE_SCHEMA,T.TABLE_NAME,T.TABLE_TYPE ,Count(Distinct COLUMN_NAME) as ColumnCnt
            ,ISNULL(STRING_AGG( 
                CASE WHEN UPPER(C.DATA_TYPE)
                    IN ('DATE','DATETIME','DATETIME2','TIME','DATETIMEOFFSET','SMALLDATETIME')
                    THEN C.COLUMN_NAME END, ', '),'') as WATERMARK_COLUMNS
            FROM INFORMATION_SCHEMA.COLUMNS C
            INNER JOIN INFORMATION_SCHEMA.TABLES T ON T.TABLE_CATALOG=C.TABLE_CATALOG
            AND C.TABLE_SCHEMA=T.TABLE_SCHEMA
            AND C.TABLE_NAME=T.TABLE_NAME
            GROUP BY T.TABLE_SCHEMA,T.TABLE_NAME,T.TABLE_TYPE
        )
        , TableRecCnt as
        (
        SELECT SCHEMA_NAME(obj.schema_id) as Table_Schema, obj.name AS [TableName]
            , SUM(p.Rows) AS RecordCount
        FROM sys.objects AS obj
        INNER JOIN sys.partitions AS p ON obj.object_id = p.object_id
        WHERE obj.is_ms_shipped = 0x0
            AND p.index_id < 2
        GROUP BY obj.schema_id , obj.name
        ),
        viewList as (
            SELECT 
                s.Name AS [SCHEMA],
                v.NAME AS [NAME],
                ASSET_TYPE = 'VIEW',
                0 AS ROW_COUNT,
                COLUMN_COUNT = (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS c WHERE c.TABLE_NAME=v.NAME),
                WATERMARK_COLUMNS = STUFF((SELECT ',' + c.COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS c
                WHERE c.TABLE_NAME = v.NAME and c.DATETIME_PRECISION IS NOT NULL
                FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 1, '')
            FROM 
                sys.views v
            INNER JOIN 
                sys.schemas s ON s.schema_id = v.schema_id
                <view_schema_condition>
        )
        Select t.TABLE_SCHEMA AS [SCHEMA]
        ,t.TABLE_NAME as NAME
        ,T.TABLE_TYPE as ASSET_TYPE
        ,r.RecordCount as ROW_COUNT
        ,t.ColumnCnt AS COLUMN_COUNT
        , t.WATERMARK_COLUMNS
        FROM tablelist t
        INNER JOIN TableRecCnt r on t.TABLE_SCHEMA=r.Table_Schema
        AND t.TABLE_NAME=r.TableName
        WHERE 1=1 <schema_condition>
        UNION  
        Select [SCHEMA]
        ,NAME
        ,ASSET_TYPE
        ,ROW_COUNT
        ,COLUMN_COUNT
        ,WATERMARK_COLUMNS
        FROM viewList 
        ORDER BY NAME ASC
    """,
    "dq_datatypes": {
        "Integer": [
            "INT",
            "BIGINT",
            "SMALLINT",
            "TINYINT",
            "LONG",
        ],
        "Numeric": [
            "DECIMAL",
            "FLOAT",
            "MONEY",
            "SMALLMONEY",
            "NUMERIC",
            "DOUBLE PRECISION",
            "REAL",
        ],
        "Text": ["string", "CHAR", "NVARCHAR", "NCHAR"],
        "Bit": ["BIT"],
        "Date": ["DATE"],
        "DateTime": ["DATETIME", "DATETIME2", "SMALLDATETIME"],
        "Time": ["TIME"],
        "DateTimeOffset": ["DATETIMEOFFSET"],
    },
    "metadata": {
        "table": """
             with tablelist as
            (
                Select T.TABLE_SCHEMA,T.TABLE_NAME,T.TABLE_TYPE ,Count(Distinct COLUMN_NAME) as ColumnCnt
                FROM INFORMATION_SCHEMA.COLUMNS C
                INNER JOIN INFORMATION_SCHEMA.TABLES T ON T.TABLE_CATALOG=C.TABLE_CATALOG
                AND C.TABLE_SCHEMA=T.TABLE_SCHEMA
                AND C.TABLE_NAME=T.TABLE_NAME
                WHERE UPPER(T.TABLE_NAME)=UPPER('<table_name>')
                AND UPPER(T.TABLE_SCHEMA)=UPPER('<schema_name>')
                GROUP BY T.TABLE_SCHEMA,T.TABLE_NAME,T.TABLE_TYPE
            )
            , TableRecCnt as
            (
            SELECT SCHEMA_NAME(obj.schema_id) as Table_Schema, obj.name AS [TableName]
                , SUM(p.Rows) AS RecordCount
				,SUM(a.total_pages) * 8*1024 as TABLE_SIZE
            FROM sys.objects AS obj
            INNER JOIN sys.partitions AS p ON obj.object_id = p.object_id
			INNER JOIN sys.allocation_units a ON p.partition_id = a.container_id
            WHERE UPPER(SCHEMA_NAME(obj.schema_id))=UPPER('<schema_name>')
            AND UPPER(obj.name)=UPPER('<table_name>')
            AND p.index_id < 2
            GROUP BY obj.schema_id , obj.name
            )
            Select
            r.RecordCount as ROW_COUNT
            ,t.ColumnCnt AS COLUMN_COUNT
			,r.TABLE_SIZE AS TABLE_SIZE
            ,DATEDIFF(second, getdate(), o.modify_date) AS FRESHNESS
            FROM tablelist t
            INNER JOIN TableRecCnt r on t.TABLE_SCHEMA=r.Table_Schema
            AND t.TABLE_NAME=r.TableName
            INNER JOIN sys.tables o on o.name=t.TABLE_NAME
			and schema_name(o.schema_id)=t.TABLE_SCHEMA
			WHERE o.[type] = 'U'
        """,
        "view": """ 
            SELECT  COUNT(DISTINCT COL.COLUMN_NAME) AS COLUMN_COUNT
            ,null AS FRESHNESS
            FROM INFORMATION_SCHEMA.TABLES  AS T
            JOIN INFORMATION_SCHEMA.COLUMNS AS COL 
                ON COL.TABLE_NAME = T.TABLE_NAME 
                AND COL.TABLE_SCHEMA = T.TABLE_SCHEMA
            LEFT JOIN sys.dm_db_index_usage_stats S ON S.database_id=db_id()
                AND object_id = object_id('<schema_name>.<table_name>') 
            WHERE UPPER(T.TABLE_NAME) = UPPER('<table_name>') AND UPPER(T.TABLE_SCHEMA) = UPPER('<schema_name>')
            AND T.TABLE_TYPE='VIEW'
            GROUP BY T.TABLE_NAME, T.TABLE_SCHEMA, S.last_user_update
        """,
        "attributes": """
            Select C.COLUMN_NAME as [name]
            ,CASE WHEN c.IS_NULLABLE='YES' THEN 1 ELSE 0 END as is_null
            ,C.DATA_TYPE as datatype
            ,'' as [description]
            FROM INFORMATION_SCHEMA.COLUMNS C
            WHERE UPPER(C.TABLE_NAME) = UPPER('<table_name>')
            AND UPPER(C.TABLE_SCHEMA)=UPPER('<schema_name>')
        """,
        "duplicate": """
            WITH duplicate_table as (
                SELECT <attribute>, ROW_NUMBER() OVER(PARTITION BY <attribute> ORDER BY <attribute>) as [row_number]
                FROM [<schema_name>].[<table_name>]
            ) SELECT COUNT(*) AS DUPLICATE_COUNT FROM duplicate_table
            where [row_number] > 1
        """,
        "total_rows": """ SELECT COUNT(*) AS total_rows FROM [<schema_name>].[<table_name>]""",
        "primary_key": """ SELECT T.COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE T
                            WHERE OBJECTPROPERTY(OBJECT_ID(T.CONSTRAINT_SCHEMA + '.' + QUOTENAME(T.CONSTRAINT_NAME)), 'IsPrimaryKey') = 1
                            AND UPPER(T.TABLE_NAME) = UPPER('<table_name>')  <schema_condition> """,
        "freshness": """SELECT DATEDIFF(second, getdate(), MAX([<attribute>])) AS FRESHNESS  
                        FROM [<schema_name>].[<table_name>] with(nolock)
                        WHERE [<attribute>] IS NOT NULL """,
        "total_queries": """
                Select Count(*) AS QUERY_COUNT 
                    FROM sys.dm_exec_query_stats  s
                    CROSS APPLY sys.dm_exec_sql_text(s.[sql_handle]) as st
                    WHERE st.text like '%<schema_name>.<table_name>%'
                    AND s.creation_time>=DateAdd(DD,-7,getdate())
        """,
    },
    "health": {
        "common": {
            "null_count": """COUNT(CASE WHEN [<attribute>] IS NULL THEN 1 END)""",
            "distinct_count": """COUNT(DISTINCT [<attribute>])""",
            "duplicate": """(COUNT(*) - COUNT(DISTINCT [<attribute>]))""",
            "min_length": """MIN(LEN([<attribute>]))""",
            "max_length": """MAX(LEN([<attribute>]))""",
            "min_value": """MIN([<attribute>])""",
            "max_value": """MAX([<attribute>])""",
        },
        "text": {
            "blank_count": """COUNT(CASE WHEN TRIM([<attribute>])='' THEN 1 END)""",
        },
        "numeric": {
            "zero_values": """COUNT(CASE WHEN [<attribute>]=0 THEN 1 END)""",
            "min_value": """MIN([<attribute>])""",
            "max_value": """MAX([<attribute>])""",
            "range": """MAX([<attribute>])-MIN([<attribute>])""",
        },
        "date": {
            "min_value": """MIN([<attribute>])""",
            "max_value": """MAX([<attribute>])""",
        },
        "bit": {
            "min_value": """MIN(CAST([<attribute>] AS INT))""",
            "max_value": """MAX(CAST([<attribute>] AS INT))""",
        },
    },
    "advanced": {
        "text": {
            "whitespace_count": """SUM(CASE WHEN [<attribute>] LIKE  '%[ ]%' THEN 1 ELSE 0 END) """,
            "special_char_count": """SUM(CASE WHEN [<attribute>] LIKE  '%[^A-Za-z0-9 ]%' THEN 1 ELSE 0 END)""",
            "characters_count": """SUM(CASE  WHEN [<attribute>] LIKE  '%[A-Za-z]%' THEN 1 ELSE 0 END)""",
            "digits_count": """SUM(CASE WHEN [<attribute>] LIKE  '%[0-9]%' THEN 1 ELSE 0 END)""",
        },
        "numeric": {
            "negative_count": """SUM(CASE WHEN [<attribute>] < 0 THEN 1 ELSE 0 END) """,
            "positive_count": """SUM(CASE WHEN [<attribute>] >= 0 THEN 1 ELSE 0 END)""",
            "sum": """ROUND(SUM([<attribute>]), 4)""",
            "mean": """ROUND(AVG([<attribute>]), 4)""",
            "median": {
                "query": """Select top 50 Percent [<attribute>]
                            INTO #Temp
                            FROM  <table_name> with(nolock)
                            where [<attribute>] IS NOT NULL
                            Order by [<attribute>]
                            Select max([<attribute>]) as  <attribute_label> FROM #Temp
                            DROP TABLE #Temp"""
            },
            "variance": """ROUND(VAR([<attribute>]), 4)""",
            "standard_deviation": """ROUND(STDEV([<attribute>]), 4)""",
            "q1": {
                "query": """Select top 25 Percent [<attribute>]
                            INTO #Temp
                            FROM  <table_name> with(nolock)
                            where [<attribute>] IS NOT NULL
                            Order by [<attribute>]
                            Select max([<attribute>]) as  <attribute_label> FROM #Temp
                            DROP TABLE #Temp"""
            },

            "q3": {
                "query": """Select top 75 Percent [<attribute>]
                            INTO #Temp
                            FROM  <table_name> with(nolock)
                            where [<attribute>] IS NOT NULL
                            Order by [<attribute>]
                            Select max([<attribute>]) as  <attribute_label> FROM #Temp
                            DROP TABLE #Temp"""
            },
            "skewness": {
                "query": """;WITH cte AS
                        (
                        SELECT AVG([<attribute>]*1.0) as mean, STDEV([<attribute>])as stddev
                        ,CASE when COUNT(*)>2 THEN COUNT(*)*1.0 / (COUNT(*)-1) / (COUNT(*)-2) ELSE 0 END as corrfact
                        FROM <table_name> with(nolock)
                        )
                        SELECT case when sum(c.stddev)>0 then
                        ROUND(SUM((([<attribute>]*1.0 - c.mean)/c.stddev)*(([<attribute>]*1.0 - c.mean)/c.stddev)*(([<attribute>]*1.0 - c.mean)/c.stddev))
                        * MIN(c.corrfact),4) 
                        ELSE 0 END as  <attribute_label>
                        FROM  <table_name>  p with(nolock)
                        CROSS JOIN cte c """
            },
            "nan_count": """SUM(CASE WHEN ISNUMERIC([<attribute>])=0 THEN 1 ELSE 0 END)""",
        },
    },
    "frequency": {
        "length": """
            SELECT COUNT(*) AS COUNT,strlen as [LENGTH] FROM (
                    SELECT LEN(ISNULL(cast([<attribute>] as nvarchar),'')) strlen
                    FROM  <table_name>  with(nolock) ) t
            GRoup by strlen
        """,
        "pattern": """
            SUM(CASE WHEN (<pattern_condition>) THEN 1 ELSE 0 END) AS <attribute_label>
        """,
        "enum": """
            SELECT COUNT([<attribute>]) AS COUNT, [<attribute>] AS ENUM_VALUE, 'True' AS IS_VALID
            FROM <table_name>
            WHERE [<attribute>] IS NOT NULL AND TRIM(ISNULL(cast([<attribute>] as nvarchar), '')) != ''
            GROUP BY [<attribute>]
        """,
    },
    "range": {
        "length": """
            SELECT COUNT(*) AS range_count FROM <table_name>  with(nolock)
            WHERE LEN(ISNULL(cast([<attribute>] as nvarchar),'')) NOT BETWEEN <value1> AND <value2>
        """,
        "value": """
            SELECT COUNT(*) AS range_count FROM <table_name>  with(nolock)
            WHERE [<attribute>] NOT BETWEEN <value1> AND <value2>
        """
    },
    "default_query": """SELECT <query> FROM <table_name>  with(nolock)""",
    "limit_query": """ order by (select 1)
                    OFFSET 0 ROWS
                    FETCH NEXT <count> ROWS ONLY """,
    "incremental": {
        "with_date": """
            SELECT <query> FROM <table_name>  with(nolock)
            WHERE DATEDIFF(second,  <watermark_column> , '<date>') >  0
            AND <watermark_column> IS NOT NULL
        """,
        "days": """
            SELECT <query> FROM <table_name>  with(nolock)
            WHERE <watermark_column> > cast(DATEADD(Day ,-<interval>, cast(getdate() as date))as datetime)
            AND <watermark_column> IS NOT NULL
        """,
        "percentage": """
            SELECT TOP <limit> PERCENT <query> FROM <table_name> with(nolock)
            WHERE <watermark_column> IS NOT NULL
            ORDER BY <watermark_column>
        """,
    },
    "behavioral": {
        "format_date": """CONVERT(datetime,<date_colum>)""",
        "default_filter": """ CONVERT(datetime,<date_colum>) >= cast(DATEADD(Day ,-<day_interval>, cast(getdate() as date))as datetime)""",
        "date_filter": """ CONVERT(datetime,<date_colum>) > CONVERT(datetime, '<max_date_value>') """,
        "slice_query": {
            "minute": """with DateColCTE as
                        (
                            Select <columns>
                            FROM <table_name>
                            WHERE <date_colum> IS NOT NULL <date_filter>
                        ),
                        FormattedDateCTE as
                        (
                            SELECT * , <formatted_date_colum> as new_date
                            FROM DateColCTE
                        )
                        ,
                        TimeSlicedDataCTE as
                        (
                            SELECT * 
                            ,CONVERT(string(16),DateAdd(MINUTE, -DatePart(MINUTE,new_date)%<slice_interval>,new_date),121)+':00.000' as slice_start
                            ,CONVERT(string(16),DateAdd(MINUTE, <slice_interval>-DatePart(MINUTE,new_date)%<slice_interval>-1,new_date),121)+':59.999' as slice_end
                            FROM FormattedDateCTE
                        )
                        SELECT <limit_condition> slice_start,slice_end <categorical_column> <aggregate_expression>
                        FROM TimeSlicedDataCTE
                        GROUP BY slice_start,slice_end <group_by_column>
                        ORDER BY slice_start,slice_end <group_by_column>
                    """,
            "hour": """with DateColCTE as
                        (
                            Select <columns>
                            FROM <table_name>
                            WHERE <date_colum> IS NOT NULL <date_filter>
                        ),
                        FormattedDateCTE as
                        (
                            SELECT * , <formatted_date_colum> as new_date
                            FROM DateColCTE
                        )
                        ,
                        TimeSlicedDataCTE as
                        (
                            SELECT * 
                            ,CONVERT(string(13), DateAdd(Hour, -DatePart(Hour,new_date)%<slice_interval>,new_date),121)+':00:00.000' as slice_start
                            ,CONVERT(string(13), DateAdd(Hour, <slice_interval>-DatePart(Hour,new_date)%<slice_interval>-1,new_date),121)+':59:59.999' as slice_end
                            FROM FormattedDateCTE
                        )
                        SELECT <limit_condition> slice_start,slice_end <categorical_column> <aggregate_expression>
                        FROM TimeSlicedDataCTE
                        GROUP BY slice_start,slice_end <group_by_column>
                        ORDER BY slice_start,slice_end <group_by_column>
                    """,
            "day": """with DataCTE as
                        (
                            Select <columns>
                            FROM <table_name>
                            WHERE <date_colum> IS NOT NULL <date_filter>
                        ),
                        FormattedDateCTE as
                        (
                            SELECT * , <formatted_date_colum> as new_date
                            FROM DataCTE
                        )
                        ,DateRangeCTE AS
                        (
                            Select Min(new_date) as DateCol_Min
                            ,Max(new_date) as DateCol_Max
                            FROM FormattedDateCTE
                        ),
                        GenerateTimeSliceCTE as (
                            SELECT CAST(CAST(DateCol_Min as DATE) as DATETIME) as slice_start
                            ,CONVERT(string(10),DATEADD(DD, <slice_interval>-1, DateCol_Min) , 121)  + ' 23:59:59.999' as slice_end
                            FROM DateRangeCTE
                            union all
                            select CAST(CAST(DATEADD(SS,1,slice_end) as DATE) as DATETIME) as slice_start
                            ,CONVERT(string(10),DATEADD(DD, <slice_interval>-1, slice_end) , 121)  + ' 23:59:59.999' as slice_end
                            from GenerateTimeSliceCTE
                            where slice_end<=(SELECT DateCol_Max FROM DateRangeCTE)
                        )
                        Select <limit_condition> slice_start, slice_end <categorical_column> <aggregate_expression>
                        FROM GenerateTimeSliceCTE G
                        INNER JOIN FormattedDateCTE D on D.new_date >= G.slice_start AND D.new_date <= G.slice_end
                        group by slice_start, slice_end <group_by_column>
                        ORDER BY slice_start,slice_end <group_by_column>
                        option (maxrecursion 0)
                    """,
            "week": """with DataCTE as
                        (
                            Select <columns>
                            FROM <table_name>
                            WHERE <date_colum> IS NOT NULL <date_filter>
                        ),
                        FormattedDateCTE as
                        (
                            SELECT * , <formatted_date_colum> as new_date
                            FROM DataCTE
                        )
                        ,DateRangeCTE AS
                        (
                            Select Min(new_date) as DateCol_Min
                            ,Max(new_date) as DateCol_Max
                            FROM FormattedDateCTE
                        ),
                        GenerateTimeSliceCTE as (
                            SELECT CONVERT(string(10),DATEADD(week, DATEDIFF(week, -1, DateCol_Min), -1), 121) + ' 00:00:00.000' as slice_start
                            ,CONVERT(string10),DATEADD(DAY,7*<slice_interval>-1,DATEADD(week, DATEDIFF(week, -1, DateCol_Min), -1)), 121) + ' 23:59:59.999' as slice_end
                            FROM DateRangeCTE
                            union all
                            select	CONVERT(string(10),CAST(DATEADD(SS,1,slice_end) as DATE) ,121)+ ' 00:00:00.000' as slice_start
                            ,CONVERT(string(10),DATEADD(DAY,7*<slice_interval>-1, slice_end), 121) + ' 23:59:59.999'  as slice_end
                            from GenerateTimeSliceCTE
                            where slice_end<=(SELECT DateCol_Max FROM DateRangeCTE)
                        )
                        Select <limit_condition> slice_start, slice_end <categorical_column> <aggregate_expression>
                        FROM GenerateTimeSliceCTE G
                        INNER JOIN FormattedDateCTE D on D.new_date >= G.slice_start AND D.new_date <= G.slice_end
                        group by slice_start, slice_end <group_by_column>
                        ORDER BY slice_start,slice_end <group_by_column>
                        option (maxrecursion 0)
                    """,
            "month": """with DataCTE as
                        (
                            Select <columns>
                            FROM <table_name>
                            WHERE <date_colum> IS NOT NULL <date_filter>
                        ),
                        FormattedDateCTE as
                        (
                            SELECT * , <formatted_date_colum> as new_date
                            FROM DataCTE
                        )
                        ,DateRangeCTE AS
                        (
                            Select Min(new_date) as DateCol_Min
                            ,Max(new_date) as DateCol_Max
                            FROM FormattedDateCTE
                        ),
                        GenerateTimeSliceCTE as (
                            SELECT CONVERT(string(10),DATEADD(MONTH, DATEDIFF(MONTH, 0, DateCol_Min), 0), 121) + ' 00:00:00.000' as slice_start
                            ,CONVERT(string(10),CAST(EOMONTH(DATEADD(MONTH, <slice_interval>, DateCol_Min)) as DateTIME), 121)  + ' 23:59:59.999' as slice_end
                            FROM DateRangeCTE
                            union all
                            select CONVERT(string(10),CAST(DATEADD(SS,1,slice_end) as DATE) ,121)+ ' 00:00:00.000' as slice_start
                            ,CONVERT(string(10),CAST(EOMONTH(DATEADD(MONTH, <slice_interval>, slice_end)) as DateTIME), 121)  + ' 23:59:59.999'  as slice_end
                            from GenerateTimeSliceCTE
                            where slice_end<=(SELECT DateCol_Max FROM DateRangeCTE)
                        )
                        Select <limit_condition> slice_start, slice_end <categorical_column> <aggregate_expression>
                        FROM GenerateTimeSliceCTE G
                        INNER JOIN FormattedDateCTE D on D.new_date >= G.slice_start AND D.new_date <= G.slice_end
                        group by slice_start, slice_end <group_by_column>
                        ORDER BY slice_start,slice_end <group_by_column>
                        option (maxrecursion 0)
                    """,
            "year": """with DataCTE as
                        (
                            Select <columns>
                            FROM <table_name>
                            WHERE <date_colum> IS NOT NULL <date_filter>
                        ),
                        FormattedDateCTE as
                        (
                            SELECT * , <formatted_date_colum> as new_date
                            FROM DataCTE
                        )
                        ,DateRangeCTE AS
                        (
                            Select Min(new_date) as DateCol_Min
                            ,Max(new_date) as DateCol_Max
                            FROM FormattedDateCTE
                        ),
                        GenerateTimeSliceCTE as (
                            SELECT CONVERT(string(10),DATEADD(YEAR, DATEDIFF(YEAR, 0, DateCol_Min), 0), 121) + ' 00:00:00.000' as slice_start
                            ,CONVERT(string(10),DATEADD(YEAR, <slice_interval>, DATEADD(YEAR, DATEDIFF(YEAR, 0, DateCol_Min), 0))-1, 121)  + ' 23:59:59.999' as slice_end
                            FROM DateRangeCTE
                            union all
                            select CONVERT(string(10),CAST(DATEADD(SS,1,slice_end) as DATE) ,121)+ ' 00:00:00.000' as slice_start
                            ,CONVERT(string(10),DATEADD(YEAR,<slice_interval>, DATEADD(YEAR, DATEDIFF(YEAR, 0, slice_end), 0))-1, 121)  + ' 23:59:59.999'   as slice_end
                            from GenerateTimeSliceCTE
                            where slice_end<=(SELECT DateCol_Max FROM DateRangeCTE)
                        )
                        Select <limit_condition> slice_start, slice_end <categorical_column> <aggregate_expression>
                        FROM GenerateTimeSliceCTE G
                        INNER JOIN FormattedDateCTE D on D.new_date >= G.slice_start AND D.new_date <= G.slice_end
                        group by slice_start, slice_end <group_by_column>
                        ORDER BY slice_start,slice_end <group_by_column>
                        option (maxrecursion 0)
                    """,
        },
        "aggregation": {
            "avg": "AVG",
            "sum": "SUM",
            "min": "MIN",
            "max": "MAX",
            "count": "COUNT",
            "value": ""
        },
        # do not add [] below in date_column it will appended by get_attribute_names function in airflow
        "max_query": """
            SELECT MAX(<date_colum>) as max_date FROM <table_name> with(nolock) 
        """
    },
    "query_mode": {
        "drop_view": """ IF EXISTS (Select 1 from INFORMATION_SCHEMA.TABLES
                            WHERE TABLE_TYPE='VIEW'
                            AND TABLE_NAME='<table_name>'
                            AND TABLE_SCHEMA='<schema_name>') DROP VIEW <schema_name>.<table_name> """,
        "create_view": """ CREATE OR ALTER VIEW <schema_name>.<table_name> AS <query_string> """
    },
    "custom_rule_query": {
        "and": """and""",
        "or": """or""",
        "not": """not""",
        "match": """cast([<attribute>] as nvarchar) like '<value1>'""",
        "notMatch": """cast([<attribute>] as nvarchar) not like '<value1>'""",
    },
    "failed_rows": {
        "schema": """
             SELECT Count(DISTINCT [TABLE_SCHEMA]) as schema_count FROM [<db_name>].[INFORMATION_SCHEMA].[TABLES] with(nolock)
                WHERE LOWER([TABLE_SCHEMA])=LOWER('<schema_name>')
        """,
        "asset": {
            "duplicate_count": """
                WITH duplicate_table as (
                    SELECT <attributes>, ROW_NUMBER() OVER(PARTITION BY <partition_by> ORDER BY <partition_by>) as [row_number]
                    FROM <table_name>
                ) select <limit_condition> <failed_attributes> from duplicate_table
                where <not_condition> [row_number] > 1
            """,
        },
        "attribute": {
            "distinct_count": """
                WITH distinct_table as (
                    SELECT <attributes>, ROW_NUMBER() OVER(PARTITION BY [<attribute>] ORDER BY [<attribute>]) as [row_number]
                    FROM <table_name>
                ) select <limit_condition> <failed_attributes> from distinct_table where <not_condition> [row_number] = 1
            """,
            "duplicate": """
                WITH duplicate_table as (
                    SELECT <attributes>, ROW_NUMBER() OVER(PARTITION BY [<attribute>] ORDER BY [<attribute>]) as row_number
                    FROM <table_name>

                ) select <limit_condition> <failed_attributes> from duplicate_table where <not_condition> [row_number] > 1
            """,
            "null_count": """SELECT <limit_condition> <failed_attributes> FROM <table_name> WHERE [<attribute>] IS <not_condition> NULL """,
            "blank_count": """SELECT <limit_condition> <failed_attributes> FROM <table_name> WHERE <not_condition> [<attribute>] = '' """,
            "space_count": """SELECT <limit_condition> <failed_attributes> FROM <table_name> WHERE <not_condition> (NOT [FirstName] LIKE  '%[^ ]%') """,
            "non_empty": """SELECT <limit_condition> <failed_attributes> FROM <table_name> WHERE <not_condition> ([<attribute>] IS NOT NULL AND [<attribute>] != '' AND [FirstName] LIKE  '%[^ ]%') """,
            "zero_values": """SELECT <limit_condition> <failed_attributes> FROM <table_name> WHERE <not_condition> [<attribute>] = 0 <negate_condition>""",
            "zero_values_negate_condition": """ OR [<attribute>] IS NULL """,
            "pattern": """SELECT <limit_condition> <failed_attributes> FROM <table_name> WHERE <not_condition> (<value1>) """,
            "pattern_condition": """ [<attribute>] LIKE '%<value1>%' """,
            "null_pattern_condition": """ [<attribute>] IS <not_condition> NULL """,
            "empty_pattern_condition": """ <not_condition> [<attribute>] = '' """,
            "space_pattern_condition": """ <not_condition> [<attribute>] = '' """,
            "length": """SELECT <limit_condition> <failed_attributes> FROM <table_name> WHERE LEN(ISNULL(cast([<attribute>] as nvarchar),'')) <not_condition> BETWEEN <value1> and <value2> """,
            "enum": """SELECT <limit_condition> <failed_attributes> FROM <table_name> WHERE (ISNULL(convert(string, [<attribute>], 121),'DQ_NULL') <not_condition> IN <value1>) """,
            "whitespace_count": """SELECT <limit_condition> <failed_attributes> FROM <table_name> WHERE <not_condition> [<attribute>] LIKE  '%[ ]%'  """,
            "special_char_count": """SELECT <limit_condition> <failed_attributes> FROM <table_name> WHERE <not_condition> [<attribute>] LIKE  '%[^A-Za-z0-9 ]%' """,
            "characters_count": """SELECT <limit_condition> <failed_attributes> FROM <table_name> WHERE <not_condition> [<attribute>] LIKE  '%[A-Za-z]%' """,
            "digits_count": """SELECT <limit_condition> <failed_attributes> FROM <table_name> WHERE <not_condition> [<attribute>] LIKE  '%[0-9]%' """,
            "negative_count": """SELECT <limit_condition> <failed_attributes> FROM <table_name> WHERE <not_condition> [<attribute>] < 0  """,
            "positive_count": """SELECT <limit_condition> <failed_attributes> FROM <table_name> WHERE <not_condition> [<attribute>] >= 0 """,
            "length_range": """
                SELECT <limit_condition> <failed_attributes> FROM <table_name>  with(nolock)
                WHERE <not_condition> (LEN(ISNULL(cast([<attribute>] as nvarchar),'')) NOT BETWEEN <value1> AND <value2>)
            """,
            "value_range": """
                SELECT <limit_condition> <failed_attributes> FROM <table_name>  with(nolock)
                WHERE <not_condition> ([<attribute>] NOT BETWEEN <value1> AND <value2>)
            """
        },
        "negative_query": """
            SELECT <limit_condition> <failed_attributes> FROM <table_name>
            WHERE <hash_key> NOT IN (
                SELECT <hash_key> FROM (<query_string>) as failed_records
            )
        """,
        "hash_key": "CONCAT(<attributes>)",
        "concat_ws": """CONCAT_WS('<delimiter>', <attributes>)""",
        "invalid_preview": """
            SELECT <limit_condition> * FROM <table_name> WHERE <hash_key> IN (
                SELECT DISTINCT IDENTIFIER_KEY FROM <database_name>.[<schema_name>].[<failed_rows_table>]
                WHERE <key_constrains>
            )
        """,
        "create_invalid_table": """ IF NOT EXISTS (SELECT TOP 1 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='<failed_rows_table>' AND TABLE_SCHEMA='<schema_name>' AND TABLE_TYPE='BASE TABLE')
            CREATE TABLE <database_name>.[<schema_name>].[<failed_rows_table>] (
                CONNECTION_NAME NVARCHAR(1000),
                ASSET_NAME NVARCHAR(1000),
                ATTRIBUTE_NAME NVARCHAR(1000),
                MEASURE_NAME NVARCHAR(1000),
                IDENTIFIER_KEY NVARCHAR(1000),
                IDENTIFIER_VALUE NVARCHAR(1000),
                VALUE NVARCHAR(1000),
                CONNECTION_ID NVARCHAR(50),
                ASSET_ID NVARCHAR(50),
                RUN_ID NVARCHAR(50),
                ATTRIBUTE_ID NVARCHAR(50),
                MEASURE_ID NVARCHAR(50),
                CREATED_DATE DATETIME
            )
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ‘\t’
            LINES TERMINATED BY ‘\n’
        """,
        "insert_invalid_data": """
            INSERT INTO <database_name>.[<schema_name>].[<failed_rows_table>] (
               CONNECTION_NAME, ASSET_NAME, ATTRIBUTE_NAME, MEASURE_NAME,
               CONNECTION_ID, ASSET_ID, RUN_ID, ATTRIBUTE_ID, MEASURE_ID,
               IDENTIFIER_KEY, IDENTIFIER_VALUE, VALUE, CREATED_DATE 
            ) 
        """,
        "current_date": """ GETDATE() AS [CURRENT_TIMESTAMP] """,
        "delete": """
            DELETE FROM <database_name>.[<schema_name>].[<failed_rows_table>] WHERE RUN_ID='<run_id>'
        """,
        "delete_history": """
            DELETE FROM <database_name>.[<schema_name>].[<failed_rows_table>] WHERE RUN_ID NOT IN (<run_ids>)
        """,
        "distinct_run": """
            WITH RANKED_DATA AS (
                SELECT DISTINCT ATTRIBUTE_ID, RUN_ID, CREATED_DATE,
                RANK() OVER (PARTITION BY ATTRIBUTE_ID ORDER BY CREATED_DATE DESC) AS ranking
                FROM <database_name>.[<schema_name>].[<failed_rows_table>]
                GROUP BY ATTRIBUTE_ID, CREATED_DATE, RUN_ID
            ) SELECT * FROM RANKED_DATA WHERE ranking = 1
        """,
        "asset_invalid_count": """
            SELECT COUNT(DISTINCT IDENTIFIER_VALUE) AS INVALID_ROWS
            FROM <database_name>.[<schema_name>].[<failed_rows_table>] WHERE <where_condition>
        """,
        "attribute_invalid_count": """
            SELECT DISTINCT ATTRIBUTE_ID, COUNT(DISTINCT IDENTIFIER_VALUE) AS INVALID_ROWS
            FROM <database_name>.[<schema_name>].[<failed_rows_table>]
            WHERE (ATTRIBUTE_ID IS NOT NULL AND ATTRIBUTE_ID != '') <where_condition>
            GROUP BY ATTRIBUTE_ID
        """,
        "drop_table": """ DROP TABLE IF EXISTS <table_name> """
    },
    "profile": {
        "value_distribution": """
            SELECT CASE WHEN ISDATE(cast([<attribute>] as nvarchar))=1 THEN convert(string, [<attribute>],121) ELSE CAST([<attribute>] as string) END AS ENUM_VALUE
            , COUNT(*) AS VALUE_COUNT
            FROM <table_name> GROUP BY [<attribute>]
        """,
        "length_distribution": """
            SELECT LEN(CASE WHEN ISDATE(cast([<attribute>] as nvarchar))=1 THEN convert(string, [<attribute>],121) ELSE CAST([<attribute>] as string) END) AS LENGTH_VALUE
            , COUNT(*) AS VALUE_COUNT
            , MAX(CASE WHEN ISDATE(cast([<attribute>] as nvarchar))=1 THEN convert(string, [<attribute>],121) ELSE CAST([<attribute>] as string) END) AS ENUM_VALUE
            FROM <table_name>
            GROUP BY LEN(CASE WHEN ISDATE(cast([<attribute>] as nvarchar))=1 THEN convert(string, [<attribute>],121) ELSE CAST([<attribute>] as string) END)
        """,
        "pattern_distribution": """
            WITH DISTINCT_DATA AS (
            SELECT CASE WHEN ISDATE(cast([<attribute>] as nvarchar))=1 THEN convert(string, [<attribute>],121) ELSE CAST([<attribute>] as string) END AS ENUM_VALUE
            , COUNT(*) AS VALUE_COUNT
            , MAX(CASE WHEN ISDATE(cast([<attribute>] as nvarchar))=1 THEN convert(string, [<attribute>],121) ELSE CAST([<attribute>] as string) END) AS SAMPLE_VALUE
            FROM <table_name>  
            GROUP BY CASE WHEN ISDATE(cast([<attribute>] as nvarchar))=1 THEN convert(string, [<attribute>],121) ELSE CAST([<attribute>] as string) END
            )
            , TEXT_FORMATTING AS (
            SELECT dqlabs.dqlabs_deep_profile_pattern(ENUM_VALUE,1) AS ENUM_VALUE, VALUE_COUNT, SAMPLE_VALUE
            FROM DISTINCT_DATA
            )
            SELECT DISTINCT ENUM_VALUE, SUM(VALUE_COUNT) AS VALUE_COUNT, MAX(SAMPLE_VALUE) AS SAMPLE_VALUE
            FROM TEXT_FORMATTING GROUP BY ENUM_VALUE
        """,
        "short_pattern_distribution": """
             WITH DISTINCT_DATA AS (
            SELECT CASE WHEN ISDATE(cast([<attribute>] as nvarchar))=1 THEN convert(string, [<attribute>],121) ELSE CAST([<attribute>] as string) END AS ENUM_VALUE
            , COUNT(*) AS VALUE_COUNT
            , MAX(CASE WHEN ISDATE(cast([<attribute>] as nvarchar))=1 THEN convert(string, [<attribute>],121) ELSE CAST([<attribute>] as string) END) AS SAMPLE_VALUE
            FROM <table_name>  
            GROUP BY CASE WHEN ISDATE(cast([<attribute>] as nvarchar))=1 THEN convert(string, [<attribute>],121) ELSE CAST([<attribute>] as string) END
            )
            , TEXT_FORMATTING AS (
            SELECT dqlabs.dqlabs_deep_profile_pattern(ENUM_VALUE,0) AS ENUM_VALUE, VALUE_COUNT, SAMPLE_VALUE
            FROM DISTINCT_DATA
            )
            SELECT DISTINCT ENUM_VALUE, SUM(VALUE_COUNT) AS VALUE_COUNT, MAX(SAMPLE_VALUE) AS SAMPLE_VALUE
            FROM TEXT_FORMATTING GROUP BY ENUM_VALUE
        """,
        "value_range": """
            SELECT COUNT(*) AS range_count FROM <table_name>
            WHERE [<attribute>] NOT BETWEEN <value1> AND <value2>
        """,
        "zero_values": """
            SELECT count(*) AS zero_values_count FROM <table_name>
            WHERE 1=(
                CASE WHEN TRY_CAST([<attribute>] AS NUMERIC(18,2))=0.00  THEN 1
                WHEN TRY_CAST([<attribute>]  AS NUMERIC(18,2)) IS NULL 
                    AND (
                        TRIM(CAST([<attribute>]   AS NVARCHAR(2000))) LIKE '[+-]0[.]0%'
                        OR TRIM(CAST([<attribute>]   AS NVARCHAR(2000))) LIKE '[-+]?[0]+([-.]?[0])%' 
                    ) THEN 1
                ELSE 0
                END
                )
        """
    }
}
