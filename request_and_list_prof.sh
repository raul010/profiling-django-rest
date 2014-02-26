#!/bin/bash

# Se por exemplo optar por efetuar 10 Requests e 100 Loops, você receberá dois retornos: o log rerente ao tempo médio de cada parte do ciclo da API Django REST Framework  para estes 10 requests, e também o tempo médio que a sua Base de Dados levou para fazer 1000 Selects em cada um destes 10.

# Alterar ambiente. Ex:
INTERP="/home/raul/.virtualenvs/py3/bin/python"
PROJ="/home/raul/dev/works-py3/profiling/"

REQUEST=1;
LOOP=10
HOST=127.0.0.1;
PORT=8000;

function PrintUsage() {
	echo -e "\n`basename $0`\n

-n \tNome da URL |obrigatorio|\n

-r \tQtde de Requests |default 1|
-l \tQtde de Loops (Selects na Base) |default 10|

-s \tNome do Host |default 127.0.0.1|
-p \tPorta |default 8000|\n"
	exit 1
}
while getopts "hr:l:-n:-p: " OPTION
do
	case $OPTION in
		h) PrintUsage
		;;
		r) REQUEST=$OPTARG
		;;
		l) LOOP=$OPTARG 
		;;
		n) SITE=$OPTARG
		;;
		s) HOST=$OPTARG
		;;
		p) PORTA=$OPTARG
		;;
		?) PrintUsage
		;;
	esac
done

shift $((OPTIND-1))

if [ -z $SITE  ]; then
	echo -e "\nFavor informar o 'Nome da URL'. Ex: -n site\n-h para ajuda\n"
	exit 1
elif [ $REQUEST -lt 1 ]; then
        echo -e "\nValor inválido para REQUEST\n-h para ajuda\n"
	exit 1
elif [ $LOOP -lt 1 ]; then
        echo -e "\nValor inválido para LOOP\n-h para ajuda\n"
        exit 1
fi

count=0
	while [ $REQUEST -gt $count ]; do
		curl http://$HOST:$PORT/$SITE
		echo -e "(`expr $count + 1`) Executando Request: http://$HOST:$PORT/$SITE"		
		sleep 1
		count=`expr $count + 1`
	done

if [ $LOOP -gt 0 ]; then
	sleep 1
	$INTERP $PROJ/manage.py hit_base loop$LOOP 
fi

#/home/raul/.virtualenvs/py3/bin/python /home/raul/dev/works-py3/profiling/manage.py hit_base
