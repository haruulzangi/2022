package main

import (
	"fibonacci-sum/utils"
	"fmt"
	"net"
)

const (
	SERVER_PORT = "57777"
	SERVER_TYPE = "tcp"
	WAIT_TIME   = 30
)

func main() {
	fmt.Printf(`
	*******************************
	**** ХАРУУЛЗАНГИ 2022 *********
	**** Sum of Fibonacci *********
	**** Listening %s on %s ***
	*******************************
	`, SERVER_TYPE, SERVER_PORT)
	fmt.Printf("\n")

	server, err := net.Listen(SERVER_TYPE, ":"+SERVER_PORT)
	defer server.Close()

	if err != nil {
		fmt.Println(err.Error())
		panic("Server cannot listen on port")
	}

	for {
		connection, err := server.Accept()
		if err != nil {
			fmt.Println(err.Error())
			panic("Error on client connection")
		}
		go utils.ProcessClient(connection)
		go utils.TimeOut(connection, WAIT_TIME)
	}
}
