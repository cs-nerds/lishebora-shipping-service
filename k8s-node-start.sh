#!/bin/bash

echo "Creating shipping secrets"

kubectl create secret generic shipping-secret --from-env-file=k8s/secrets/shipping-secrets

echo "Creating shipping app deployment"

kubectl apply -f k8s/deployment.yml

echo "Creating shipping service"

kubectl apply -f k8s/shipping-svc.yml

echo "Checking external port for shipping svc"
kubectl get svc shipping

