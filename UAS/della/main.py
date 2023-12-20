from http import HTTPStatus
from flask import Flask, request, abort
from flask_restful import Resource, Api 
from models import tabeltas as tabeltasModel
from engine import engine
from sqlalchemy import select
from sqlalchemy.orm import Session

session = Session(engine)

app = Flask(__name__)
api = Api(app)        

class BaseMethod():

    def __init__(self):
        self.raw_weight = {'harga': 5, 'warna': 5, 'ukuran': 5, 'jenis': 3,'kualitas':3}

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {k: round(v/total_weight, 2) for k, v in self.raw_weight.items()}

    @property
    def data(self):
        query = select(tabeltasModel.nama_tas,  tabeltasModel.harga, tabeltasModel.warna, tabeltasModel.ukuran, tabeltasModel.jenis, tabeltasModel.kualitas)
        result = session.execute(query).fetchall()
        print(result)
        return [{'nama_tas': tabeltas.nama_tas, 'harga': tabeltas.harga, 'warna': tabeltas.warna, 'ukuran': tabeltas.ukuran, 'jenis': tabeltas.jenis, 'kualitas': tabeltas.kualitas} for tabeltas in result]

    @property
    def normalized_data(self):
        
        harga_values = []
        warna_values = []
        ukuran_values = []
        jenis_values = []
        kualitas_values = []
        
        for data in self.data:

            harga_values.append(data['harga'])
            warna_values.append(data['warna'])
            ukuran_values.append(data['ukuran'])
            jenis_values.append(data['jenis'])
            kualitas_values.append(data['kualitas'])

        return [
            {'nama_tas': data['nama_tas'],
             
             'harga': data['harga'] / max(harga_values),
             'warna': data['warna'] / max(warna_values),
             'ukuran': data['ukuran'] / max(ukuran_values),
             'jenis': data['jenis'] / max(jenis_values),
             'kualitas': data['kualitas'] / max(kualitas_values)
             }
            for data in self.data
        ]

    def update_weights(self, new_weights):
        self.raw_weight = new_weights

class WeightedProductCalculator(BaseMethod):
    def update_weights(self, new_weights):
        self.raw_weight = new_weights

    @property
    def calculate(self):
        normalized_data = self.normalized_data
        produk = []

        for row in normalized_data:
            product_score = (
               
                row['harga'] ** self.raw_weight['harga'] *
                row['warna'] ** self.raw_weight['warna'] *
                row['ukuran'] ** self.raw_weight['ukuran'] *
                row['jenis'] ** self.raw_weight['jenis']*
                row['kualitas'] ** self.raw_weight['kualitas']
            )

            produk.append({
                'nama_tas': row['nama_tas'],
                'produk': product_score
            })

        sorted_produk = sorted(produk, key=lambda x: x['produk'], reverse=True)

        sorted_data = []

        for product in sorted_produk:
            sorted_data.append({
                'nama_tas': product['nama_tas'],
                'score': product['produk']
            })

        return sorted_data


class WeightedProduct(Resource):
    def get(self):
        calculator = WeightedProductCalculator()
        result = calculator.calculate
        return result, HTTPStatus.OK.value
    
    def post(self):
        new_weights = request.get_json()
        calculator = WeightedProductCalculator()
        calculator.update_weights(new_weights)
        result = calculator.calculate
        return {'data': result}, HTTPStatus.OK.value
    

class SimpleAdditiveWeightingCalculator(BaseMethod):
    @property
    def calculate(self):
        weight = self.weight
        result = {row['nama_tas']:
                  round(
                        row['harga'] * weight['harga'] +
                        row['warna'] * weight['warna'] +
                        row['ukuran'] * weight['ukuran'] +
                        row['jenis'] * weight['jenis']+
                        row['kualitas'] * weight['kualitas'], 2)
                  for row in self.normalized_data
                  }
        sorted_result = dict(
            sorted(result.items(), key=lambda x: x[1], reverse=True))
        return sorted_result

    def update_weights(self, new_weights):
        self.raw_weight = new_weights

class SimpleAdditiveWeighting(Resource):
    def get(self):
        saw = SimpleAdditiveWeightingCalculator()
        result = saw.calculate
        return result, HTTPStatus.OK.value

    def post(self):
        new_weights = request.get_json()
        saw = SimpleAdditiveWeightingCalculator()
        saw.update_weights(new_weights)
        result = saw.calculate
        return {'data': result}, HTTPStatus.OK.value


class tabeltas(Resource):
    def get_paginated_result(self, url, list, args):
        page_size = int(args.get('page_size', 10))
        page = int(args.get('page', 1))
        page_count = int((len(list) + page_size - 1) / page_size)
        start = (page - 1) * page_size
        end = min(start + page_size, len(list))

        if page < page_count:
            next_page = f'{url}?page={page+1}&page_size={page_size}'
        else:
            next_page = None
        if page > 1:
            prev_page = f'{url}?page={page-1}&page_size={page_size}'
        else:
            prev_page = None
        
        if page > page_count or page < 1:
            abort(404, description=f'Halaman {page} tidak ditemukan.') 
        return {
            'page': page, 
            'page_size': page_size,
            'next': next_page, 
            'prev': prev_page,
            'Results': list[start:end]
        }

    def get(self):
        query = select(tabeltasModel)
        data = [{'nama_tas': tabeltas.nama_tas, 'harga': tabeltas.harga, 'warna': tabeltas.warna, 'ukuran': tabeltas.ukuran, 'jenis': tabeltas.jenis} for tabeltas in session.scalars(query)]
        return self.get_paginated_result('tabeltas/', data, request.args), HTTPStatus.OK.value


api.add_resource(tabeltas, '/tabeltas')
api.add_resource(WeightedProduct, '/wp')
api.add_resource(SimpleAdditiveWeighting, '/saw')

if __name__ == '__main__':
    app.run(port='5005', debug=True)