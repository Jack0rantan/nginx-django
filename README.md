# nginx-django

## note when deploying
- 1st, please pull from repository to do 'git pull origin coin'.
- 2nd, please comment-out/in the part of "STATIC" in mysite/setting.py
- 3rd, please restart uwsgi & nginx like below
<<<<<<< HEAD
<details><summary>resart command</summary><div>
\```sh
sudo systemctl restart uwsgi
sudo /etc/init.d/nginx restart
\```
</div></details>
