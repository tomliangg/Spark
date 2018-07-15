import sys
from pyspark.sql import SparkSession, functions, types


spark = SparkSession.builder.appName('example').getOrCreate()

assert sys.version_info >= (3, 4) # make sure we have Python 3.4+
assert spark.version >= '2.1' # make sure we have Spark 2.1+

data = spark.read.csv('cities.csv', header=True, inferSchema=True)

data.show()
data.printSchema()
data.write.json('spark-output', mode='overwrite')