#!/usr/bin/env bash

# https://www.gnu.org/software/bash/manual/bash.html#The-Set-Builtin
# -e  Exit immediately if a command exits with a non-zero status.
# -x Print commands and their arguments as they are executed.
set -e

kind create cluster --config ./cluster-and-oneagent-installation/kind-config.yaml
kubectl create namespace dynatrace-test
kubectl config set-context --current --namespace=dynatrace-test

docker build -t dynatrace-instrumentation-app:latest . --platform linux/amd64
kind load docker-image dynatrace-instrumentation-app:latest

kubectl apply -f ./cluster-and-oneagent-installation/k8s-manifests/0-database-and-broker.yaml &&
kubectl apply -f ./cluster-and-oneagent-installation/k8s-manifests/1-secrets-and-configmap.yaml &&
kubectl apply -f ./cluster-and-oneagent-installation/k8s-manifests/2-service-and-deployment.yaml

helm repo add dynatrace https://raw.githubusercontent.com/Dynatrace/dynatrace-operator/main/config/helm/repos/stable
helm install dynatrace-operator dynatrace/dynatrace-operator \
    -f ./cluster-and-oneagent-installation/dynatrace-configuration/values.yaml \
    --atomic \
    --create-namespace --namespace dynatrace \
    --debug

kubectl apply -f ./cluster-and-oneagent-installation/dynatrace-configuration/dynakube.yaml