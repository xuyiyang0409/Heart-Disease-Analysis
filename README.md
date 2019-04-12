# Heart-Disease-Analysis
COMP9321 19T1 Assignment 3

## API Specification

**Get data to plot charts**

- GET data of two attributes (each for all values) from the database to plot a chart.

    ```
    GET /attr?name=<AttributeName>
    
    Sample Request
    GET /attr?name=cp
    
    Sample Response
    {
        "cp" : "[[63, 1, 1], [67, 1, 4] ...]"
    }
    ```
- If any attributes does not exist in database, return message and **404 Error**.

    ```
    Response
    {
        "message" : "<AttributeName> not found in database!"
    }
    ```
- If no attribute is given, return message and **400 Error**.

    ```
    Response
    {
        "message": "Please ensure you provide a coordinate!"
    }
    ```

**Get important factors**
 
- GET the potential important factors analyzed by machine learning algorithms.
- Note the number of important factors can be changed.

    ```
    GET /factors
    
    Sample Response
    {
        "importantFactor1": "sex",
        "importantFactor2": "age"
        ...
    }
    ```
- If the important factors are not yet determined (NOT happen when finished), return message and **404 Error**.

    ```
    Response
    {
        "message": "The important factors are not yet determined!"
    }
    ```

**Predict users' risks of suffering heart diseases**

- POST the important factors to backend from user input.
- Predict the result based on `PredictType`.
- If `PredictType` = 1, it means 0-1 classification
    ```
    POST /predict?type=<PredictType>
    
    POST Payload
    {
        "ca": "0",
        "oldpeak": "2.3"
        ...
    }
    
    Sample Response
    {
        "message": "No Disease"
        "level": "0"
    }
    ```
- If `PredictType` = 2, it means multiple classification

    ```
    POST /predict?type=<PredictType>
    
    POST Payload
    {
        "ca": "0",
        "oldpeak": "2.3"
        ...
    }
    
    Sample Response
    {
        "message": "No Disease"
        "level": "0"
    }
    ```
- If the `PredictType` is not either 1 or 2, return message and **400 Error**.

    ```
    Response
    {
        "message" : "Bad Request, please check your argument is either 1 or 2!"
    }
    ```

- If any attributes in POST payload are not **Important Factors**, return message and **404 Error**.

    ```
    Response
    {
        "message" : "<AttributeName> is not an important factor!"
    }
    ```
    
- If any attributes in POST payload is malformed (e.g. empty payload), return message and **400 Error**.

    ```
    Response
    {
        "message" : "Bad Request, please check your payload format!"
    }
    ```
