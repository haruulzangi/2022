package utils

import (
	"math/rand"
	"time"
)

func GetRand(min int, max int) int {
	rand.Seed(time.Now().UnixNano())
	return rand.Intn(max-min) + min
}
