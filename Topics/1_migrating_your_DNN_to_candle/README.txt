

# To download the data for t29res.py, run these in the same directory as the 
# t29res.py code.

wget http://ftp.mcs.anl.gov/pub/candle/public/tutorials/t29res/rip.it.test.csv.gz
wget http://ftp.mcs.anl.gov/pub/candle/public/tutorials/t29res/rip.it.train.csv.gz

# Then uncompress them
gunzip rip.it.test.csv.gz
gunzip rip.it.train.csv.gz

# Then run the code
python ./t29res.py
