from database.DB_connect import DBConnect
from model.actor import Actor


class DAO():

    @staticmethod
    def getAllRatings():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct r.avg_rating 
                from ratings r
                order by r.avg_rating ASC
                """

        cursor.execute(query)

        for row in cursor:
            results.append(row["avg_rating"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(r1, r2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct n.*
                from names n, role_mapping rm, movie m, ratings r 
                where n.id = rm.name_id and rm.movie_id = m.id and m.id = r.movie_id 
                and r.avg_rating between %s and %s
                and n.date_of_birth is not null
                """

        cursor.execute(query, (r1, r2))

        for row in cursor:
            results.append(Actor(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(r1, r2, idMap):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select t1.a1, t2.a2, SUM(CAST(REPLACE(REPLACE(m.worlwide_gross_income,'$',''),',','') AS UNSIGNED)) AS Weight
                from (select distinct n.id as a1, m.id m1
                from names n, role_mapping rm, movie m, ratings r 
                where n.id = rm.name_id and rm.movie_id = m.id and m.id = r.movie_id 
                and r.avg_rating between %s and %s
                and n.date_of_birth is not null) as t1,
                (select distinct n.id as a2, m.id as m2
                from names n, role_mapping rm, movie m, ratings r 
                where n.id = rm.name_id and rm.movie_id = m.id and m.id = r.movie_id 
                and r.avg_rating between %s and %s
                and n.date_of_birth is not null) as t2, movie m 
                where t1.a1 < t2.a2 and t1.m1 = t2.m2 and t1.m1 = m.id
                and m.worlwide_gross_income is not null
                group by t1.a1, t2.a2
                """

        cursor.execute(query, (r1, r2, r1, r2))

        for row in cursor:
            results.append([idMap[row["a1"]], idMap[row["a2"]], row["Weight"] ])

        cursor.close()
        conn.close()
        return results

