"""
Note: Make sure the server is running when running these tests. 

"""

from flask import request, jsonify, abort
import requests     
import unittest

user1 = {"email": "user1@tester.com", "fname": "User", "lname": "One"}
user2_bad = {"ema": "user.numberTwo@tester2.com", "fname": "User", "lname": "Two"}

url = 'http://127.0.0.1:5000/'

initial_dataDict = {"casper@casper.se": ["Casper", "casp"],
                    "somedude@hello.com": ["Some", "dude"]}     # Tuple converts to list for JSON. 

class TestAPI(unittest.TestCase):

    def test1Get(self):
        #Test the GET-request. 
        resp = requests.get(url)
        
        assert resp.status_code == 200
        self.assertEqual(resp.json(), initial_dataDict)
    
    def test2Put(self):
        #Test the PUT-request. 
        resp = requests.put(url, json=user1)       

        assert resp.status_code == 200
        self.assertEqual(resp.json(), {'user1@tester.com': ['User', 'One']})
        
    def test3PutAgain(self):
        #Make sure that another attempt on adding the same email adress, fails. 
        resp = requests.put(url, json=user1)
              
        assert resp.status_code == 409
        
    def test4Delete(self):
        #Test the DELETE-request
        resp = requests.delete(url, json=user1)

        assert resp.status_code == 200
        self.assertEqual(resp.json(), {'user1@tester.com': ['User', 'One']})

        #Make sure that the user is removed from the database. 
        resp = requests.get(url)

        assert resp.status_code == 200
        self.assertEqual(resp.json(), initial_dataDict)

        #Make sure that correct error code is sent when trying to delete a user that does not exist in the database. 
        resp = requests.delete(url, json=user1)
        assert resp.status_code == 404
    
    def test5BadKey(self):
        #Test and make sure that bad keys in the requests send correct error code. 
        resp = requests.put(url, json=user2_bad)
        assert resp.status_code == 400

        resp = requests.delete(url, json=user2_bad)
        assert resp.status_code == 400


if __name__ == '__main__':
    unittest.main()