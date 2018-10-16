Provides examples for running the upf workflow. The examples
illustrate both high throughput inferencing and uncertianty
quantification.


 1012  mkdir T29_UncertiantyQuantification
 1013  cd T29_UncertiantyQuantification/
 1014  git clone https://github.com/ECP-Candle/Supervisor
 1015  git clone https://github.com/ECP-Candle/Benchmarks
 1016  git clone https://github.com/ECP-Candle/Candle
 1017  git clone https://github.com/brettin/T29res

https://ecp-candle.github.io/Candle/html/index.html
https://ecp-candle.github.io/Candle/html/tutorials/workflow_upf.html

We will demonstrate the use of the dropout layer at inference time.
First, we must use the PermanentDropout class from the CANDLE library.


