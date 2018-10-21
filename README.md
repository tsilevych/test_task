# test_task

A small RestAPI app that provides only one method: **POST /address** 

**Input**  
A .csv file with geo points. Example of file format:    
*Point,Latitude,Longitude  
A,30.493407,50.655727  
B,30.12323, 51.123123*  

**Output**  
Json sctucture with human readable address names and distances between them. Example:     
*{
  "result": {
    "links": [
      {
        "distance": 60908.13, 
        "name": "BA"
      }
    ], 
    "points": [
      {
        "address": "Vyshgorodskiy rayon, Kyivska Oblast, UKR", 
        "name": "A"
      }, 
      {
        "address": "Ivankovskiy rayon, Kyivska Oblast, UKR", 
        "name": "B"
      }
    ]
  }, 
  "success": true
}*

**Building**  
Just clone that repo, then, run Flask app:  
`export FLASK_APP=run.py`  
`flask run`  

**Testing**   
Can be tested via cURL. Example:  
`curl -F 'file=@/home/user/Документы/test_file.csv' http://127.0.0.1:5000/address`
