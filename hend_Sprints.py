# Databricks notebook source
display(dbutils.fs.ls("/databricks-datasets/samples/docs/"))

# COMMAND ----------

textFile = spark.read.text("/databricks-datasets/samples/docs/README.md")                                                                                                                                                                                                                         

# COMMAND ----------

textFile.count()

# COMMAND ----------

# MAGIC %scala
# MAGIC val lines = sc.textFile("/databricks-datasets/samples/docs/README.md")
# MAGIC val counts = lines.flatMap(line => line.split(" ")).map(word => (word, 1)).reduceByKey(_+_)

# COMMAND ----------

# MAGIC %scala
# MAGIC counts.collect

# COMMAND ----------

#python
#use the Spark csv file datasource with options specifying:
# first line of file is a header
#automatically infer the schema of the data
#in otherwords, reuse the already exist schema and generate the datatypes
data = spark.read.format("csv") \
.option("header", "true") \
.option("inferschema", "true") \
.load("/databricks-datasets/samples/population-vs-price/data_geo.csv")

# COMMAND ----------

data.count()

# COMMAND ----------

#command cache() cache data for faster reuse
#command dropna drops rows with missing values
data.cache()
data = data.dropna()
data.count()

# COMMAND ----------

data.take(10)

# COMMAND ----------

data.take(5)

# COMMAND ----------

display(data)

# COMMAND ----------

data.createOrReplaceTempView("data_geo")

# COMMAND ----------

# MAGIC %sql
# MAGIC select City, State from data_geo

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from data_geo where State = 'Alabama'

# COMMAND ----------

# MAGIC %scala
# MAGIC val range100 = spark.range(100)
# MAGIC range100.collect()

# COMMAND ----------

# MAGIC %scala 
# MAGIC val df = spark.read.json("/databricks-datasets/samples/people/people.json")

# COMMAND ----------

# MAGIC  %scala
# MAGIC case class Person (name: String, age: Long) 
# MAGIC val ds = spark.read.json("/databricks-datasets/samples/people/people.json").as[Person]

# COMMAND ----------

# MAGIC %scala
# MAGIC case class DeviceIoTData (
# MAGIC battery_level: Long,
# MAGIC c02_level: Long, 
# MAGIC cca2: String, 
# MAGIC cn: String,
# MAGIC device_id: Long, 
# MAGIC device_name: String, 
# MAGIC humidity: Long, 
# MAGIC ip: String, 
# MAGIC latitude: Double, 
# MAGIC longitude: Double, 
# MAGIC scale: String,
# MAGIC temp: Long,
# MAGIC timestamp: Long
# MAGIC )
# MAGIC val ds = spark.read.json("/databricks-datasets/iot/iot_devices.json").as[DeviceIoTData]

# COMMAND ----------

# MAGIC %scala
# MAGIC display(ds)

# COMMAND ----------

# MAGIC %scala
# MAGIC ds.take(10).foreach(println(_))

# COMMAND ----------

# MAGIC %scala
# MAGIC val sorted_device = ds.select($"battery_level", $"c02_level", $"device_name").where($"battery_level" >= 6).sort($"c02_level")
# MAGIC display(sorted_device)

# COMMAND ----------

# MAGIC %scala
# MAGIC ds.createOrReplaceTempView("iot_device_data")

# COMMAND ----------

# MAGIC %sql
# MAGIC select cca3, count (distinct device_id) as device_id from iot_device_data group by cca3 order by device_id desc limit 100

# COMMAND ----------

# MAGIC %scala
# MAGIC ds.write.saveAsTable("iot_device_data2")

# COMMAND ----------

# MAGIC %scala
# MAGIC ds.write.mode("overwrite").parquet("/tmp/testParquet")

# COMMAND ----------

display(dbutils.fs.ls("/tmp/testParquet"))

# COMMAND ----------

parquet_directory = spark.read.parquet("/tmp/testParquet/")
display(parquet_directory)

# COMMAND ----------

# MAGIC %scala
# MAGIC spark.sql("show tables").show()

# COMMAND ----------



# COMMAND ----------


