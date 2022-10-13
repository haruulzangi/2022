package utils

import "math/big"

func fib(n int) (*big.Int, *big.Int) {
	if n == 0 {
		return big.NewInt(0), big.NewInt(1)
	}
	a, b := fib(n / 2)
	c := big.NewInt(0).Mul(a, (big.NewInt(0).Sub(big.NewInt(0).Mul(b, big.NewInt(2)), a)))
	d := big.NewInt(0).Add(big.NewInt(0).Mul(a, a), big.NewInt(0).Mul(b, b))
	if n%2 == 0 {
		return c, d
	} else {
		return d, big.NewInt(0).Add(c, d)
	}
}
