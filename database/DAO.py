from database.DB_connect import DBConnect
from model.order import Order
from model.store import Store


class DAO():

    @staticmethod
    def getAllStores():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT *
        FROM stores"""
        cursor.execute(query)
        listobj = []
        for dct in cursor:
            listobj.append(Store(**dct))
        cursor.close()
        conn.close()
        return listobj

    @staticmethod
    def getAllNodes(s):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT *
        FROM orders
        WHERE store_id = %s
        """
        cursor.execute(query, (s,))
        listobj = []
        for dct in cursor:
            listobj.append(Order(**dct))
        cursor.close()
        conn.close()
        return listobj

    @staticmethod
    def getAllEdges(s, k):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT DISTINCT o1.order_id AS source, o2.order_id AS target,
               COUNT(oi.quantity + oi2.quantity) AS weight
        FROM orders o1, orders o2, order_items oi, order_items oi2 
        WHERE o1.store_id = %s
          AND o1.store_id = o2.store_id 
          AND o1.order_date > o2.order_date
          AND oi.order_id = o1.order_id
          AND oi2.order_id = o2.order_id
          AND DATEDIFF(o1.order_date, o2.order_date) < %s
        GROUP BY o1.order_id, o2.order_id
        """
        cursor.execute(query, (s, k))
        listobj = []
        for dct in cursor:
            listobj.append((dct['source'], dct['target'], dct['weight']))
        cursor.close()
        conn.close()
        return listobj

    if __name__ == '__main__':
        print(getAllNodes(1))
        print(getAllEdges(1, 5))




