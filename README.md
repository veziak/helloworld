

[Hello world REST API implemented with GoLang](/app)

[Integration tests implemented with Python](/tests)

[Kubernetes deployment scripts](/k8s)

[Terraform scripts](/terraform)

## Hello world application
To build:
```bash
go get
go build
```
To run unit tests:
```bash
go test
```
To build a docker image for gcp docker registry:
```bash
docker build -t eu.gcr.io/{gcp.project.id}/helloworld-go:{image.tag} .
```
To push an image to gcp docker registry:
```bash
docker push eu.gcr.io/{gcp.project.id}/helloworld-go:{image.tag}
```
To run it locally postgres should be configured using environment variables:
```bash
export POSTGRES_DB_HOST="localhost:5432"
export POSTGRES_DB_USER="hello"
export POSTGRES_DB_PASSWORD="password"
```

and schema should be created manually

```sql
CREATE TABLE public.users
(
    username text COLLATE pg_catalog."default" NOT NULL,
    dateofbirth date NOT NULL,
    CONSTRAINT "User_pkey" PRIMARY KEY (username)
)
WITH (
    OIDS = FALSE
)
```

## Intergration tests
Intergation tests are written in Python and should be executed against Hello world application running in some test environment.
Hello world application url is configured in [config.py](/tests/config.py) file
To run tests:
```bash
pytest api_tests.py
```
## Deployment to Kubernetes
First step is to configure Service (Load Balancer):
```bash
kubectl apply -f service.yaml
```
Next step is to deploy hello world docker container :
```bash
export APP_VERSION="%app.version%"
export DOCKER_TAG="%docker.tag%"
envsubst < deploy.yaml | kubectl apply -f -
```
*envsubst* command is replacing parameters in deploy.yaml with environment variable values.

## Terraform
Terraform script will create a new Kubernetes cluster hosted on GCP with Google SQL Cloud Postgres instance accessible from Kubernetes pods. Database schema and postgres credentials should be created separately. Credentials stored to Kubernetes Secrets.

![](https://lh3.googleusercontent.com/MHdhLdUw5FZvNtRTcVxRdgM8-Paw6PPsauEpGKuvnMyUgeNb_3RUbS2InmgQaayOnmXe-jd1Ip09Suvp0sHoHsCDY58XRl202ENiVMOSrsuGDchxbt2uc7rJGCidFpj5RytP-wbz)


## No down time deployment example
We are running 1.1.0 version of hello world app based on helloworld-go:1.1.0 docker container and we would like to deploy 1.2.0 version based on helloworld-go:1.2.0 image.  
Let's check cluster status:

![](https://lh5.googleusercontent.com/Dkj_LONt0RUkStnG3Gg0nG_5EkV_9GtYf8EwUhKa7xKgyQUEduJNb6V4Vrx6dgKaZWEaCkOPzDP6zKVsn42PUqZyhJskfln67mDHIuSrDU2Nkl4_tlPLDoLrd8YKLKMT-R5XJfvZ)
To avoid any down time we can deploy and run a new version in parallel with an old version. We just need to make sure that application is backward compatible.
Let's run following command:
 ```bash
export APP_VERSION="1.2.0"
export DOCKER_TAG="1.2.0"
envsubst < deploy.yaml | kubectl apply -f -
```
and check cluster status after that:
![](https://lh4.googleusercontent.com/61wBaz2BoUVAx0naaT5tRUMgrSywYx_dEgiLgCZ9e0JRquwNHArUy1-b04TJymXcDuFV96HEhiP6a1e3BOH-N1lVTPtZLMaU7QWoeKa0vgxcpay9E77U3Fzb1GYs5NPHs-oDF-A5)
Both versions are running in parallel and load balancer randomly choose which pod should serve a request. If we are happy with a new version and logs and monitoring are looking good we can destroy 1.1.0 version. 
```bash
kubectl delete deploy helloworld-go-1.1.0
```
Cluster should look like this after that:

![](https://lh6.googleusercontent.com/Ea3nUI2_zwYdtbGgdIy-1TSn-C4dbpk6prXx4KKcfKoR8fR9N4cuHHOEko2Qhh76C5rBr6XwO3sbI5rikuxERbKNT0IDkWS07ttd1vaZqEuNm8BsaXB_TAD5t8_uVxGpsQ4dHQcM)

So a new version has been deployed successfully and without any downtime.
