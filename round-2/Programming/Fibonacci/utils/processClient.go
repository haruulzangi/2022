package utils

import (
	"fmt"
	"math/big"
	"net"
	"strings"
)

const (
	ROUND_MIN     = 20
	ROUND_MAX     = 30
	FIB_MIN_INDEX = 20
	FIB_MAX_INDEX = 200
	FLAG          = "HZ{1_h0p3_Y0u_d0N’7_jUd93_M3_1F_1_wA7CH_Y0u_fr0M_7h3_C0rn3r}"
)

func ProcessClient(connection net.Conn) {
	sum := big.NewInt(0)
	round := GetRand(ROUND_MIN, ROUND_MAX)
	data := fmt.Sprintf("%d\n", round)
	active_connection := true

	for i := 0; i < round; i++ {
		nthFib := GetRand(FIB_MIN_INDEX, FIB_MAX_INDEX)
		data = fmt.Sprintf("%s%d ", data, nthFib)
		sum.Add(sum, Fibonacci(nthFib))
	}

	data = data + "\n"
	if _, err := connection.Write([]byte(data)); err != nil {
		fmt.Println("Cannot send data to connection")
		fmt.Println(err.Error())
	}

	//fmt.Println(sum)
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
