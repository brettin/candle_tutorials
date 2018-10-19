# Provides examples for running the upf workflow. The examples illustrate
# both high throughput inferencing and uncertianty quantification.

# Docuementation can be found here.
https://ecp-candle.github.io/Candle/html/index.html
https://ecp-candle.github.io/Candle/html/tutorials/workflow_upf.html

# First, we need to modify the DNN to use the PermanentDropout class. This
# is a wrapper around the keras Dropout class that allows us to use the
# dropout layers during inferencing.

# We also need to modify the inference script to use recognize the
# PermanentDropout layer.

# The PermenantDropout class can be imported from the candle_keras
# library.

# Make sure that Benchmarks/common is set (outside of CANDLE). Make sure
# that the data is available. Make sure that the path to the data is fully
# specified.

# We will setup a clean CANDLE environment by cloning the Supervisor and
# Benchmarks repositories.

git clone https://github.com/ECP-Candle/Supervisor
git clone https://github.com/ECP-Candle/Benchmarks 

cd Benchmarks
git checkout release_01

# For the tutorial, we can use the t29res model.

git clone https://github.com/brettin/T29res

# To get the data to run the t29 example, you can download it from an
# ANL ftp server.

cd T29res
curl -o rip.it.test.csv ftp://ftp.mcs.anl.gov/pub/candle/public/tutorials/t29res/rip.it.test.csv
curl -o rip.it.train.csv ftp://ftp.mcs.anl.gov/pub/candle/public/tutorials/t29res/rip.it.train.csv
curl -o t29res.model.h5  ftp://ftp.mcs.anl.gov/pub/candle/public/tutorials/t29res/ori-t29res.model.h5

# We will demonstrate the use of the dropout layer at inference time.
# First, we must use the PermanentDropout class from the CANDLE library.

1. add path to Benchmarks/common in t29res
2. change Dropout to PermenantDropout in t29res
3. train and save model

1. add path to Benchmarks/commom in infer
2. register PermanentDropout in infer
3. add argument and loop for number of predictions

# Now we are ready to proceed to setting up the run using the CANDLE upf
# workflow. 


cd ../Supervisor/workflows/upf/test
1. set MODEL_NAME in upf-1.sh 
2. set BENCHMARK_DIR in cfg-sys-1.sh 
3. set MODEL_PYTHON_SCRIPT in cfg-sys-1.sh 
4. set PROCS, QUEUE, WALLTIME in cfg-sys-1.sh
5. create upf-1.txt
