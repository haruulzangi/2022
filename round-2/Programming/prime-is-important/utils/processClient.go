package utils

import (
	"fmt"
	"net"
	"strings"
)

const (
	MIN_LIMIT = 100000000
	MAX_LIMIT = 1000000000
	FLAG      = "HZ{7h3 pr1m3 c0ll3c710n 15 4 c0ll3c710n 0f c05m371c5 1n v4l0r4n7}"
)

func ProcessClient(connection net.Conn) {
	number := GetRand(MIN_LIMIT, MAX_LIMIT)
	data := fmt.Sprintf("%d\n", number)
	active_connection := true

	if _, err := connection.Write([]byte(data)); err != nil {
		fmt.Println("Cannot send data to connection")
		fmt.Println(err.Error())
	}

	sum := SumOfPrimes(number)
	fmt.Println("SUM =", sum)

	buffer := make([]byte, 1024)
	mLen, err := connection.Read(buffer)
	if err != nil {
		active_connection = false
	}

	response := strings.TrimSpace(string(buffer[:mLen]))
	//fmt.Println(response)
	sumStr := fmt.Sprintf("%v", sum)
	if response == sumStr && active_connection {
		if _, err := connection.Write([]byte(FLAG)); err != nil {
			fmt.Println(err.Error())
		}
	} else if response != sumStr && active_connection {
		msg := "Invalid input sorry, try again!\n"
		if _, err := connection.Write([]byte(msg)); err != nil {
			fmt.Println(err.Error())
		}
	}
	defer connection.Close()
}
