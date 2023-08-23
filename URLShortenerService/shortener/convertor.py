class Convertor:
    @staticmethod
    def int_to_base62(uid):
        """
        Convert the UID to a base62 string.
        """

        if uid == 0:
            return '0'
        
        charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        result = []
        
        while uid:
            uid, remainder = divmod(uid, 62)
            result.append(charset[remainder])
        
        return ''.join(reversed(result))

    @staticmethod
    def base62_to_int(s):
        """
        Convert a base62 string to an integer.
        """

        charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        base = len(charset)
        result = 0

        for i, c in enumerate(reversed(s)):
            result += charset.index(c) * (base ** i)
        
        return result