rsync -av -e ssh --exclude='venv/*' --exclude='output/*' --exclude='data/*' --exclude='.git' --exclude='.idea'  ../cuc_rating root@$t_ip:~/
