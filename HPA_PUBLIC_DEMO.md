# 🌐 Public HPA Demo Setup

To share your auto-scaling demo publicly, follow these steps:

## 1. Configure ngrok Authentication
ngrok v3 requires a free account.

1.  **Sign Up / Login:** Go to [dashboard.ngrok.com](https://dashboard.ngrok.com/signup)
2.  **Get Authtoken:** Copy your token from [Your Authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)
3.  **Configure:** Run this command in your terminal (replace `<TOKEN>`):
    ```bash
    ngrok config add-authtoken <YOUR_TOKEN>
    ```

## 2. Start the Demo

### Step A: Ensure App is Accessible Locally
Make sure port-forward is running:
```bash
kubectl port-forward svc/flask-service 8080:5000 &
```
Test: `curl http://localhost:8080`

### Step B: Start Public Tunnel
Expose your local port 8080 to the internet:
```bash
ngrok http 8080
```
This gives you a URL like `https://abc-123.ngrok-free.app`

## 3. Visualize HPA Scaling

While the tunnel is running, open a **separate terminal** to watch the scaling:
```bash
watch -n 2 'kubectl get hpa && echo "" && kubectl get pods -l app=flask-app'
```

## 4. Generate Load (Publicly)
Share your ngrok URL with friends or run a load test against it:
```bash
# Using apache bench (replace URL)
ab -n 5000 -c 50 https://your-ngrok-url.ngrok-free.app/
```

Watch the pods scale up! 🚀
