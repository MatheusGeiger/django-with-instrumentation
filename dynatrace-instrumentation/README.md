# A simple django app to test dynatrace with oneagent on kubernetes instrumentation

## Configuration services

On the docker-compose file we have three services related with dynatrace instrumentation:
- **app-production**: Django web application (using gunicorn) with code to instrument
- **app-pubsub**: Simple django consumer using [django-stomp](https://github.com/juntossomosmais/django-stomp) library using stomp protocol
- **app-pubsub-pika**: Simple django consumer using [pika](https://pika.readthedocs.io/en/stable/) protocol

Flow: Django + autodynatrace instrumentation > dynatrace sdk > one agent (at the kubernetes) > process and parse > dynatrace ingest api > dynatrace UI

To run the instrumented application with services you can run `docker-compose up app-production`

## How to test ? 

After the up `app-production` you can use the `api/v1/users/attributes` endpoint to test traces. This endpoint will create database item, request to external service, log information, request to redis service and publish a message to rabbit (using pika and stomp protocol).

## Testing using curl
```curl
curl --request POST \
  --url http://127.0.0.1:8080/api/v1/users/attributes \
  --header 'Content-Type: application/json' \
  --data '{
	"full_name": "Carl Edward Sagan",
	"given_name": "Carl",
	"family_name": "Sagan",
	"user_metadata": {
		"city": "santo andré",
		"state": "SP",
		"birthday": "1989-10-10",
		"gender": "male"
	}
}'
```

## Creating local cluster and install one-agent dynatrace

Creates a trial account at [dynatrace](https://www.dynatrace.com/signup/) to generate PAAS token to download one-agent code and install locally.


Creating cluster local and up the django app:
   
    kind create cluster --config ./cluster-and-oneagent-installation/kind-config.yaml 
    kubectl create namespace dynatrace-test
    kubectl config set-context --current --namespace=dynatrace-test

    docker build -t dynatrace-instrumentation-app:latest . --platform linux/amd64
    kind load docker-image dynatrace-instrumentation-app:latest

    kubectl apply -f ./cluster-and-oneagent-installation/k8s-manifests/0-database-and-broker.yaml
    kubectl apply -f ./cluster-and-oneagent-installation/k8s-manifests/1-secrets-and-configmap.yaml
    kubectl apply -f ./cluster-and-oneagent-installation/k8s-manifests/2-service-and-deployment.yaml

Wait a few minutes, and you should be able to access http://localhost:8080/admin and see django admin

    kubectl get pods
    NAME                                                        READY   STATUS 
    db-postgres-deployment-bd95fc458-dvgqj                      1/1     Running
    django-template-deployment-9c4d6df4b-2mbn7                  1/1     Running
    django-template-deployment-consumer-5b68bc6879-8qf55        1/1     Running
    django-template-pika-deployment-consumer-7b5cb58685-p7hpw   1/1     Running
    rabbit-deployment-5949d576ff-64qn9                          1/1     Running


Installing [dynatrace operator using helm](https://github.com/Dynatrace/dynatrace-operator/tree/main/config/helm/chart/default):
    
    helm repo add dynatrace https://raw.githubusercontent.com/Dynatrace/dynatrace-operator/main/config/helm/repos/stable
    helm install dynatrace-operator dynatrace/dynatrace-operator \
        -f ./cluster-and-oneagent-installation/dynatrace-configuration/values.yaml \
        --atomic \
        --create-namespace --namespace dynatrace \
        --debug

    kubectl apply -f ./cluster-and-oneagent-installation/dynatrace-configuration/dynakube.yaml**


** change the <LIVE_ENVIROMENT_DYNATRACE> and <DYNATRACE_TOKEN> to your dynatrace account

To remove cluster
    
    kind delete cluster

Set the context you had been using before the ride:
    
    kubectl config current-context
    kubectl config get-contexts
    kubectl config use-context YOUR_PREVIOUS_CONTEXT


## Recurring procedures

### Installing new packages and their updates

    docker compose run app poetry update

### Generating a new migration

    docker compose run app python manage.py makemigrations

### To up the project

    docker compose up app-production

### To build image

    docker build -t django-dynatrace-instrumentation:latest . --platform linux/amd64