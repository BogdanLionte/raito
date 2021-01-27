import mysql.connector
from authentication import validate_access_token

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="raito"
)


def write_query(access_token, api, result):
    user_email = validate_access_token(access_token)
    stmt = "INSERT INTO userqueries(user_email, api, result) VALUES (%s, %s, %s)"
    params = (user_email, api, result)
    db.cursor().execute(stmt, params)
    db.commit()


def read_queries(access_token):
    user_email = validate_access_token(access_token)
    stmt = "SELECT * FROM userqueries WHERE user_email = %s"
    params = (user_email,)
    cursor = db.cursor()
    cursor.execute(stmt, params)
    return cursor.fetchall()


if __name__ == '__main__':
    access_token = "eyJ0eXAiOiAiSldUIiwgImFsZyI6ICJSUzI1NiJ9.eyJzdWIiOiAidGF0dS5hZGl0emFAZ21haWwuY29tIiwgImlhdCI6IDE2MTE2OTg0MTYsICJleHAiOiAxNjQwNzI4ODE2LCAibmJmIjogMTY0MDcyODgxNiwgImF1ZCI6ICJhY2Nlc3MifQ.DJpcD26b34UUekWIfsrDhRk7z2pwOrs8LkYc0kQnP5SdZ9dU7-ca-Fv-WcaDrAzgiCoKsM2inWU6URcB3kg6Rtm3j8UOQHPKZLmrSKXDlokRWiZywWSNyqyK-QxWaJDUF9Dd9j1kbfPYMqCALQ53ei3iPVUCSXxje5HAfBL-01UoS0iB2AI-vzpHSAoEWvcbVQWcXuEVlc_mqP-r86SFF_6mfhS_9iDYmhuhnO5rHydxFNSoJPCe1OS-6Td5R375i7GBD0hcdQj9gyvRlcwcXLWZ6rx7gu4W4dKPvdeoDfYq7JVmJ4PFfAYcAQ_d-8RDA6ubjUSa7q9RRVmttCdjTg"
    write_query(access_token, "api", "result")
    print(read_queries(access_token))
