class NumberConverter:
    @staticmethod
    def decimal_to_binary(decimal_num):
        return bin(decimal_num)[2:]

    @staticmethod
    def binary_to_decimal(binary_num):
        return int(binary_num, 2)

    @staticmethod
    def decimal_to_octal(decimal_num):
        return oct(decimal_num)[2:]

    @staticmethod
    def octal_to_decimal(octal_num):
        return int(octal_num, 8)

    @staticmethod
    def decimal_to_hex(decimal_num):
        return hex(decimal_num)[2:]

    @staticmethod
    def hex_to_decimal(hex_num):
        return int(hex_num, 16)