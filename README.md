<div align="center">
<h1>
  Interview Scheduling Backend
</h1>

<h4>
  Backend Server for Interview scheduling Application built in Django framework
</h4>
</div>

## <div align="center">Overview</div>

Backend server for API development. The application is deployed via docker.

## <div align="center"> Installation </div>

### Installation of Backend

- Create `backend` docker image:

```console
docker build -t interview-app-backend .
```

- Run `backend` docker container:

```console
docker run -d -p 8000:8000 -v <path_to_django-app>:/app --name interview-app-backend-container interview-app-backend:latest
```




