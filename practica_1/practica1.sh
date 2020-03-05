#!/usr/bin/env bash

function mqtt_publisher {
    true
}

function mqtt_subscriber {
    true
}

function get_rnd_int() {
    rnd_int_command="from random import randint; print(randint($1, $2))"
    echo $(python3 -c "$rnd_int_command")
}

function get_rnd() {
    rnd_command="from random import random; print($1 + random() * ($2 - $1))"
    echo $(python3 -c "$rnd_command")
}

topics=(/casa/cerradura /casa/pb/temperatura /casa/pb/estancia/luz /casa/pb/estancia/pantalla
        /casa/pa/estudio/luz /casa/pa/estudio/humedad)
qos=(2, $(get_rnd_int 0 2), $(get_rnd_int 0 2), $(get_rnd_int 0 2), $(get_rnd_int 0 2), $(get_rnd_int 0 2))

mqtt_host="192.168.1.1"
mqtt_host="10.12.40.143"
mqtt_host="127.0.0.1"
mqtt_host="192.168.43.153"
# mosquitto > /dev/null &
length=${#topics[*]}


while true; do
count=0


while [ $count -lt $length ]; do
    # mosquitto_pub -h $mqtt_host -t ${topics[$count]} -q ${qos[$count]} -m "hola mundo desde ${topics[$count]}" &
    # mosquitto_pub -h $mqtt_host -t ${topics[$count]} -q 0 -m "hola mundo desde ${topics[$count]}" &
    mosquitto_pub -h $mqtt_host -t ${topics[$count]} -i duplicado -r -m $(get_rnd_int 0 5) &
    ((count++))
    echo $count
    sleep 1
done;
    sleep $(get_rnd 1.5 3)
done;