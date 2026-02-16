# 📊 Database Monitoring Guide

## 1. Access Grafana
We have set up Grafana in your cluster. To access it, run:
```bash
kubectl port-forward svc/monitoring-grafana 3000:80 -n monitoring
```
Then open: **http://localhost:3000**

## 2. Login
*   **Username:** `admin`
*   **Password:** `FR9YgmJ5t8RMQazpMCge9woZcbNHFJecTfMUN5Bg`

## 3. Import Dashboard
The **CloudNativePG Community** provides an excellent pre-built dashboard.

1.  In Grafana, go to **Dashboards** -> **New** -> **Import**.
2.  Enter Dashboard ID: `20417`
3.  Click **Load**.
4.  Select **Prometheus** as the data source.
5.  Click **Import**.

## 4. View Metrics
You will see:
*   **Transactions/sec** (TPS)
*   **Active Connections**
*   **Replication Lag** (Crucial for HA!)
*   **Resource Usage** (CPU/Memory)


vL3B79dM4d691lM6w8yqK8c2mU4G8j10H9x5zM9k0y58T0O9e3Xw6z1O7L0P6S4y