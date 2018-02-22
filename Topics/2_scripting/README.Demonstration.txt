# This is a short recipe on how to run your first hyperparameter optimization
# run on the cori supercomputer at NERSC.

# Clone a current copy of the Supervisor and checkout master.
git clone https://github.com/ECP-Candle/Supervisor
cd Supervisor
git checkout master
cd ..

# Clone a current copy of the Benchmarks and checkout frameworks.
git clone https://github.com/ECP-Candle/Benchmarks
cd Benchmarks/
git checkout frameworks

# Stage the train and test data on the head node.
cd Pilot1/NT3/
source ~/python.env.from.supervisor
python nt3_baseline_keras2.py

# Run a hyperparameter optimization.
cd ../../../Supervisor/workflows/nt3_mlrMBO/test/
./test-1.sh cori
