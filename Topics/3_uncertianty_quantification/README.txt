Provides examples for running the upf workflow. The examples
illustrate both high throughput inferencing and uncertianty
quantification.

Make sure that Benchmarks/common is set (outside of CANDLE)
Make sure that the data is available
Make sure that the path to the data is fully specified


 1012  mkdir T29_UncertiantyQuantification
 1013  cd T29_UncertiantyQuantification/
 1014  git clone https://github.com/ECP-Candle/Supervisor

 1015  git clone https://github.com/ECP-Candle/Benchmarks
       cd Benchmarks ; git checkout release_01

 1016  git clone https://github.com/ECP-Candle/Candle
 1017  git clone https://github.com/brettin/T29res

https://ecp-candle.github.io/Candle/html/index.html
https://ecp-candle.github.io/Candle/html/tutorials/workflow_upf.html

We will demonstrate the use of the dropout layer at inference time.
First, we must use the PermanentDropout class from the CANDLE library.

1. set MODEL_NAME in upf-1.sh
2. set BENCHMARK_DIR in cfg-sys-1.sh
3. set MODEL_PYTHON_SCRIPT in cfg-sys-1.sh
4. set PROCS, QUEUE, WALLTIME in cfg-sys-1.sh

Need to modify the DNN infer to use PermenantDropout
 to have a parameterized output file.
 to hava a paramterized input file.
 to use PermenantDropout


So If I understand this correctly, all I have to do in my DNN is replace the Dropout layer with a PermanentDropout layer from keras_candle?

Yes, you’d need to call the register function only in the code that needs to load the network from checkpoint.






