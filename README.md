# Spark-CMPT353_e9
<h3>This repo is created for documentation purpose. The repo contains my personal work toward the SFU CMPT353 (Computational Data Science) course. You may use my solution as a reference. The .zip archive contains the original exercise files. For practice purpose, you can download the .zip archive and start working from there.</h3>

<p><a href="https://coursys.sfu.ca/2018su-cmpt-353-d1/pages/AcademicHonesty">Academic Honesty</a>: it's important, as always.</p>

<br/>
<p>The main goal of this exercise is to help you get familiar with running spark jobs locally and on clusters. You will be working with spark dataframe and sql funtions to process and output some big data.</p>
<br/>

<p>Below is the exercise description </p>
<hr>

<h2 id="h-aside-big-data-data-files">Aside: Big Data data files</h2>
<p>Distributing input data for this part of the course is challenging. I will distribute a few different input sets so you can test your programs at different scales. See some more detail on the <a href="BigDataSets">data sets instructions page</a>.</p>
<p>tl;dr: You'll get a toy-sized data set in the <code>.zip</code> file you're used to downloading. Bigger data sets can be found to do more serious <span>&ldquo;</span>big data<span>&rdquo;</span> testing.</p>
<p>For the exercises (and in general with big data), you should start with small data sets to get the basics working, then scale up as you work out performance problems.</p>
<h2 id="h-getting-started-with-spark">Getting Started with Spark</h2>
<p>For this question, see the program <code>first_spark.py</code> in this week's <code>.zip</code>. We want to get it running on your computer (or a CSIL Linux workstation): see the <a href="SparkLocal">Running Spark Jobs Locally</a> instructions for guidance. This is generally the right way to start working on Spark programs: locally with small data sets where you can test quickly.</p>
<p>This program takes the <code>xyz-*</code> data sets as input. These are randomly-generated values to give us something to work with. The program groups the values by their <code>id % 10</code> value, sums the <code>x</code> values, and outputs in CSV files. [Don't look for any meaning in these calculations: they are a random thing to calculate so we can see Spark do something.]</p>
<p>You should be able to run it with a command like:</p>
<pre class="highlight lang-bash">spark-submit first_spark.py xyz-1 output</pre>
<p>Assuming it runs correctly, you should be able to see its output (in CSV files) with a command like this:</p>
<pre class="highlight lang-bash">cat output/part-* | less</pre>
<p>To make sure you have to at least look at the code, <strong>add a column to the output</strong> which is the mean average of the <code>y</code> values in each group. (Hint: <a href="https://spark.apache.org/docs/2.3.1/api/python/pyspark.sql.html#pyspark.sql.functions.avg">avg</a>.)</p>
<h2 id="h-getting-started-with-our-cluster">Getting Started with our cluster</h2>
<p>Now let's get the program working on our <a href="Cluster">Cluster</a>. Assuming your code worked locally, it <em>should</em> work on the cluster.</p>
<p>See the <a href="Cluster">cluster instructions</a> for more detailed information, but you need to SSH to <code>gateway.sfucloud.ca</code> and always start your session with the command:</p>
<pre class="highlight lang-bash">module load 353</pre>
<p>Copy your program (by SCP/SFTP) to <code>gateway.sfucloud.ca</code> and you should be able to submit the job to the cluster:</p>
<pre class="highlight lang-bash">spark-submit first_spark.py /courses/353/xyz-2 output</pre>
<p>The output files will be stored on the cluster's HDFS. That means an extra step to view them. See the <a href="HDFS">HDFS instructions</a> for more details, but since the output is uncompressed and quite small, you can simply:</p>
<pre class="highlight lang-bash">hdfs dfs -cat output/*</pre>
<h3 id="h-yarn-web-frontend">YARN Web Frontend</h3>
<p>Running this job on the <code>xyz-3</code> data set should take a measurable amount of time, even on the cluster. While it's running, we can explore the information YARN (the thing responsible for doing compute work on the cluster) gives us about jobs. Visit <a href="http://localhost:8088">http://localhost:8088</a> (assuming you have done the port forwarding as described in the <a href="Cluster">Cluster</a> instructions. If not and you're on-campus, you can probably access at <a href="http://master.sfucloud.ca:8088">http://master.sfucloud.ca:8088</a>).</p>
<p>You should see a list of jobs that are running or have been run on the cluster. Find yours and make a note of its <span>&ldquo;</span>application ID<span>&rdquo;</span> in the first column of the table: you need to <strong>give it as an answer below</strong>. [Once you have that, feel free to the following tour of the frontend in small groups: there's not much utility to each of you hammering away at the cluster to each see the same screen.]</p>
<p>Click the application ID and the <span>&ldquo;</span>ApplicationMaster<span>&rdquo;</span> link. Have a look around and see the information given about your job and what's happening. The frontend will disappear when the task completes: either run it again if you want to explore more, or decide you're done your tour. (The YARN frontend in general is always there: just not for your job after it completes.)</p>
<p>If you feel like it, you can also explore the HDFS web frontend  at  <a href="http://localhost:50070">http://localhost:50070</a> or <a href="http://master.sfucloud.ca:50070">http://master.sfucloud.ca:50070</a>.</p>
<h2 id="h-extract-transform-load-ghcn-data">Extract-Transform-Load GHCN data</h2>
<p>We have worked several times with data from <a href="https://www.ncdc.noaa.gov/data-access/land-based-station-data/land-based-datasets/global-historical-climatology-network-ghcn">the GHCN</a>. I have always extracted the parts you needed: the full data set is &gt;160MB of gzipped CSV per year. It is cumbersome to deal with without big data tools. But now<span>&hellip;</span></p>
<p>When doing work with the maximum daily temperatures, it's not completely trivial to get that out of the original data files. This is very much an ETL task, but one where the big data tools become necessary.</p>
<p>Write a program <code>weather_etl.py</code> that takes two command-line arguments: the input and output directories, so it can be started like this:</p>
<pre class="highlight lang-bash">spark-submit weather_etl.py weather-1 output # locally
spark-submit weather_etl.py /courses/353/weather-1 output # cluster</pre>
<p>You'll find some code to get you started in <code>weather_etl_hint.py</code>. There is a directory of data files distributed as <code>weather-1</code> in the ZIP file. You'll also find (as described above) medium- and large-sized data sets <code>weather-2</code> and <code>weather-3</code>. These are partitioned subsets of the original GHCN data, but the exact same file format.</p>
<p>Things that need to be done to get the data into a more usable shape:</p>
<ol><li>Read the input directory of <code>.csv.gz</code> files.
</li><li>Keep only the records we care about:
<ol><li>field <code>qflag</code> (quality flag) is null; (<a href="https://spark.apache.org/docs/2.3.1/api/python/pyspark.sql.html#pyspark.sql.Column.isNull">Hint</a>)
</li><li>the <code>station</code> starts with <code>'CA'</code>; (<a href="https://spark.apache.org/docs/2.3.1/api/python/pyspark.sql.html#pyspark.sql.Column.startswith">Hint option 1</a>; <a href="https://spark.apache.org/docs/2.3.1/api/python/pyspark.sql.html#pyspark.sql.functions.substring">Hint option 2</a>)
</li><li>the <code>observation</code> is <code>'TMAX'</code>.
</li></ol></li><li>Divide the temperature by 10 so it's actually in <span>&deg;</span>C.
</li><li>Keep only the columns <code>station</code>, <code>date</code>, and <code>tmax</code> (which is the value after dividing by 10).
</li><li>Write the result as a directory of JSON files GZIP compressed (in the Spark one-JSON-object-per-line way).
</li></ol>
<p>Here are two lines of correct output (after uncompressing with <code>gunzip</code> or similar)</p>
<pre class="highlight lang-js">{"station":"CA001173242","date":"20161203","tmax":1.0}
{"station":"CA004038116","date":"20161203","tmax":4.0}</pre>
<p>Since the output here is compressed and a little larger, you'll need to uncompress and page the output to view it:</p>
<pre class="highlight lang-bash">cat output/* | gunzip | less # local
hdfs dfs -cat output/* | gunzip | less # cluster</pre>
<h2 id="h-reddit-average-scores">Reddit Average Scores</h2>
<p>I had originally put the <span>&ldquo;</span>Reddit Average Scores<span>&rdquo;</span> question on this exercise, but moved it to next week because of Quiz #2. You might want to start looking at that question and <span>&ldquo;</span>Spark Overhead<span>&rdquo;</span> from <a href="Exercise10">Exercise10</a> this week, but I won't force you to submit (until next week).</p>
<h2 id="h-questions">Questions</h2>
<p>Answer this question in a file <code>answers.txt</code>.</p>
<ol><li>What was the application ID you saw in the YARN frontend (<a href="http://localhost:8088">http://localhost:8088</a>) of the job where you actually ran the <code>first_spark.py</code> on the cluster? (It should be like <code>application_0000000000000_0000</code>. If you rand multiple time, pick any one.)
</li></ol>
