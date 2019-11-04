# FireBase-access
Python  Module and sample files to access FireBase to Create, Read, Update and Delete Nodes (CRUD Operations) in FireBase

## Setup

```
virtualenv env
source env/bin/activate
pip install requirements.txt

export GOOGLE_APPLICATION_CREDENTIALS=/path/to/firebase/credentials.json
```

## How to Use
```
Zeta
|__ components
|   |__ Node    : Class for Node
|   |__ Tx      : Class for Transaction
|
|__ zbase
    |__ create  : Creates a Node in FireBase
    |__ read    : returns a node in FireBase with a particular id
    |__ update  : Updates a Node in FireBase with a particular id
    |__ delete  : Deletes a Node in FireBase with a particular id
    |__ exists  : helper function that returns a boolean if an id exists in FireBase


```
