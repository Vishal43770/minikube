# � Full Implementation Tutorial (The "How-To" Guide)

This guide explains every step we took to transform a simple Flask app into an Enterprise-grade Kubernetes project. You can use these steps for **any application**.

---

## 🛠️ Phase 1: Environment Setup

### 1. Install Kubernetes Tools (Local Linux)
Run these on your local machine to prepare the environment:
```bash
# Update and install Docker
sudo apt update && sudo apt install -y docker.io kubectl

# Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Start your cluster
minikube start --driver=docker

# Connect your local terminal to Minikube's Docker engine
eval $(minikube docker-env)
```

---

## 📦 Phase 2: Building the Add-ons

### 2. Install the Database Operator (CloudNativePG)
This tool manages the "High Availability" logic for you.
```bash
kubectl apply -f https://raw.githubusercontent.com/cloudnative-pg/cloudnative-pg/main/releases/cnpg-1.22.1.yaml
```

### 3. Install Monitoring (Prometheus & Grafana)
This records the health of your project.
```bash
# 1. Add the Helm repository (if using Helm)
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# 2. Install the stack
helm install monitoring prometheus-community/kube-prometheus-stack --namespace monitoring --create-namespace
```

---

## 🏗️ Phase 3: The "Methods" (Implementation)

### 4. Setting up Persistence (PVC)
This creates the "External Hard Drive."
*   **Method:** Create a file `postgres-pvc.yaml` and run:
```bash
kubectl apply -f k8s/postgres-pvc.yaml
```

### 5. Setting up High Availability (Cluster)
This creates the Leader and 2 Standby pods.
*   **Method:** Create a `Cluster` resource (CloudNativePG) and run:
```bash
kubectl apply -f k8s/postgres-cluster.yaml
```

### 6. Setting up Autoscaling (HPA)
This tells Kubernetes to add more web pods when CPU > 50%.
*   **Method:** Create an `HorizontalPodAutoscaler` file and run:
```bash
kubectl apply -f k8s/flask-hpa.yaml
```

---

## 🩺 Phase 4: Monitoring & Troubleshooting

### How to check your "Vital Signs" (Pods)
```bash
# See all running pods
kubectl get pods

# See events (if a pod is crashing)
kubectl describe pod <pod-name>
```

### How to access the Grafana Dashboard
```bash
# 1. Port forward the service
kubectl port-forward svc/monitoring-grafana 3000:80 -n monitoring
```
**Access URL:** `http://localhost:3000`  
**Username:** `admin`  
**Password:** `FR9YgmJ5t8RMQazpMCge9woZcbNHFJecTfMUN5Bg`

---

## 🔄 Phase 5: Adapting to YOUR Application

If you want to use this for a **new app**, just follow these 3 rules:
1.  **Environment Variables:** Point your app's DB_HOST to `hpa-postgres-cluster-rw` (The RW Service).
2.  **Secrets:** Use the kubernetes secrets created by CNPG (`hpa-postgres-cluster-app`) to get the password.
3.  **HPA Metrics:** Ensure your app deployment has **Resource Requests** (CPU/RAM) defined, or HPA won't know when to scale!

---

**Summary of Architecture Ready for Production:**
- **HA:** CloudNativePG handles failover.
- **Persistence:** PVC stores the data.
- **Scaling:** HPA handles the traffic.
- **Observability:** Prometheus & Grafana monitor it all.
