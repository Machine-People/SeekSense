#!/bin/bash
# setup-cluster.sh

# Create a kind config file
cat << EOF > kind-config.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraMounts:
  - hostPath: /path/to/your/data
    containerPath: /data
EOF

# Create the cluster
kind create cluster --config kind-config.yaml --name seeksense

# Create namespace
kubectl create namespace seeksense

# Create secrets
kubectl create secret generic api-keys \
  --namespace seeksense \
  --from-literal=jinaAI=$JINA_API_KEY \
  --from-literal=AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
  --from-literal=AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

# Add Helm repositories
helm repo add milvus https://milvus-io.github.io/milvus-helm

# Install Milvus with reduced resource requirements
helm install milvus milvus/milvus \
  --namespace seeksense \
  --set cluster.enabled=false \
  --set standalone.resources.limits.cpu=1 \
  --set standalone.resources.limits.memory=2Gi \
  --set standalone.resources.requests.cpu=0.5 \
  --set standalone.resources.requests.memory=1Gi

# Build and load your Docker image
docker build -t seeksense-app:latest .
kind load docker-image seeksense-app:latest --name seeksense

# Install your application using Helm
helm install seeksense ./deployments/helm/seeksense --namespace seeksense