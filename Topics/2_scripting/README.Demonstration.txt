# Clone a current copy of the Supervisor and checkout master.
  001  git clone https://github.com/ECP-Candle/Supervisor
  002  cd Supervisor
  003  git checkout master
  004  cd ..

# Clone a current copy of the Benchmarks and checkout frameworks.
  005  git clone https://github.com/ECP-Candle/Benchmarks
  006  cd Benchmarks/
  007  git checkout frameworks

# Stage the train and test data on the head node.
  008  cd Pilot1/NT3/
  009  source ~/python.env.from.supervisor
  010  python nt3_baseline_keras2.py

# Run a hyperparameter optimization.
 1001  cd ~/m2924/brettin/candle_workshop/Supervisor/workflows/nt3_mlrMBO/test/
 1002  ./test-1.sh cori
