# UAS spk_web
## Install, create and activate virtualenv
https://medium.com/analytics-vidhya/virtual-environment-6ad5d9b6af59

## Install requirements

    pip install -r requirements.txt

## Run the app
to run the web app simply  use

    python main.py

## Usage
Install postman 
https://www.postman.com/downloads/

get data_toko list
<img src='img/get tas.png' alt='data_tas list'/>

get recommendations saw
<img src='img/get saw.png' alt='recommendations saw'/>

get recommendations wp
<img src='img/get wp.png' alt='recommendations wp'/>

post recommendations saw
<img src='img/saw post.png' alt='recommendations saw'/>


post recommendations wp
<img src='img/post wp.png' alt='recommendations wp'/>

ref:
https://en.wikipedia.org/wiki/Pearson_correlation_coefficient

### TUGAS UAS
Implementasikan model yang sudah anda buat ke dalam web api dengan http method `POST`

INPUT {'harga': 5, 'warna': 5, 'ukuran': 5, 'jenis': 3,'kualitas':3}

OUTPUT (diurutkan/sort dari yang terbesar ke yang terkecil)

contoh body request (bobot) :

    { 
    	"kriteria_1": 3,
    	 "kriteria_2": 5, 
    	 "kriteria_3": 7
    	 }

contoh output (diurutkan / sort dari yang terbesar ke yang terkecil):

    {
    	"alternatif_1": 40.0,
    	"alternatif_2": 37.5,
    	"alternatif_3": 35.5,
    	"alternatif_4": 30.0
    	}

