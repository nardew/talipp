class FibRetracement:
    R0 = 0
    R0_236 = 0.236
    R0_382 = 0.382
    R0_5 = 0.5
    R0_618 = 0.618
    R0_786 = 0.786
    R1 = 1.0
    R1_618 = 1.618
    R2_618 = 2.618
    R3_618 = 3.618
    R4_236 = 4.236

    @staticmethod
    def get_retracement_value(fib_coef, value):
        return value + value * fib_coef