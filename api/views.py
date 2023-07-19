import sqlite3
from django.http import JsonResponse
from rest_framework.views import APIView

class GetData(APIView):
    def get(self, request):
        conn = sqlite3.connect('BD_New.sqlite3')
        cursor = conn.cursor()

        # Выполнение SQL-запроса с объединением таблиц
        cursor.execute("SELECT Stock.date, Stock.product_id, Stock.value as value, Warehouse.name as warehouse_name, "
                       "Company.name as company_name, Product.name as product_name, Sales.sales_sum, "
                       "(SELECT SUM(Sales.amount) FROM Sales WHERE Product.id = Sales.product_id) as amount, "
                       "GROUP_CONCAT(DISTINCT ProductSegmentation.segment_name) as segment_names, "
                       "ProductMovement.in_value, ProductMovement.out_value, COALESCE(ProductMovement.type, 0) as movement_type "
                       "FROM Stock "
                       "INNER JOIN Warehouse ON Stock.warehouse_id = Warehouse.id "
                       "INNER JOIN Company ON Stock.company_id = Company.id "
                       "INNER JOIN Product ON Stock.product_id = Product.id "
                       "INNER JOIN Sales ON Product.id = Sales.product_id "
                       "LEFT JOIN ProductSegmentation ON Product.id = ProductSegmentation.product_id "
                       "INNER JOIN ProductMovement ON Product.id = ProductMovement.product_id "
                       "GROUP BY Stock.date, Stock.product_id")

        result = cursor.fetchall()

        # Преобразование результатов в список словарей
        response_data = []
        for row in result:
            transformed_record = {
                'date': str(row[0]),
                'product_id': str(row[1]),
                'value': str(row[2]),
                'warehouse_name': str(row[3]),
                'company_name': str(row[4]),
                'product_name': str(row[5]),
                'sales_sum': str(row[6]),
                'amount': str(row[7]),
                'segment_names': str(row[8]),
                'in_value': str(row[9]),
                'out_value': str(row[10]),
                'movement_type': str(bool(row[11]))
            }
            response_data.append(transformed_record)

        return JsonResponse(response_data, safe=False)
