This is readme file for demo dagshub repository

### Setup Commands : 

dvc remote add -f origin s3://dvc

dvc remote modify origin endpointurl https://dagshub.com/asadullahcreative/demo-dagshub.s3

dvc remote modify origin --local access_key_id YOUR_NEW_DAGSHUB_TOKEN

dvc remote modify origin --local secret_access_key YOUR_NEW_DAGSHUB_TOKEN

dvc remote list

dvc push -r origin