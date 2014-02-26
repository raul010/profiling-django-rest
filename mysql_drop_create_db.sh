if [ $# -lt 1 ]
then
	echo "Parâmetro Obrigatório (Nome da Base)"
	exit 1
fi

echo "drop database $1;create database $1" | mysql -u root -p

python manage.py syncdb
