server{
    listen 3000;
    location / {
        proxy_pass http://api:3000;
    }
}