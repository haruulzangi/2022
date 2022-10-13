package utils

import (
	"math/big"
)

func SumOfPrimes(n int) *big.Int {
	sum := big.NewInt(2)
	prime := make([]bool, n, n+1)
	for i := 3; i*i < n; i += 2 {
		if prime[i/2] == false {
			for j := i * i; j < n; j += i * 2 {
				prime[j/2] = true
			}
		}
	}
	primes := []int{2}
	for i := 3; i < n; i += 2 {
		if prime[i/2] == false {
			primes = append(primes, i)
			sum.Add(sum, big.NewInt(int64(i)))
		}
	}
	//fmt.Println(primes)
	return sum
}
