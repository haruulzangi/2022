package utils

import (
	"net"
	"time"
)

func TimeOut(connection net.Conn, waitTime int) {
	<-time.After(time.Duration(waitTime) * time.Second)
	_, _ = connection.Write([]byte("Sorry, Too Slow, Try again!\n"))
	defer connection.Close()
}
