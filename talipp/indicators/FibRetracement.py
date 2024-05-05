class FibonacciRetracement:
    """Fibonacci retracement levels"""

    R0_236 = 0.236
    """23.6% level"""
    R0_382 = 0.382
    """38.2% level"""
    R0_5 = 0.5
    """50.0% level"""
    R0_618 = 0.618
    """61.8% level"""
    R0_786 = 0.786
    """78.6% level"""
    R1 = 1.0
    """100.0% level"""
    R1_618 = 1.618
    """161.8% level"""
    R2_618 = 2.618
    """261.8% level"""
    R3_618 = 3.618
    """361.8% level"""

    @staticmethod
    def get_retracement_value(fibonacci_coefficient: float, value: float) -> float:
        """Calculate output value based on the provided input value and Fibonacci coefficient.

        Args:
            fibonacci_coefficient: Fibonacci coefficient.
            value: Input value.

        Returns:
            Value for given Fibonacci coefficient
        """
        return value + value * fibonacci_coefficient
