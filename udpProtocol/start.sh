nc -ulp 8000 |tee >(nc -u 192.168.137.60 8000) &
python3 ./gorev.py