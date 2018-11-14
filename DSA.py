
def fastEXP(number, stepen, modN):
    """
    Classic rapid exponentiation.

    :param number: base;
    :param stepen: power;
    :param modN: mod;

    Example: 2³ mod 5 == fastEXP(2,3,5)

    :return: result of exponentiation.

    """
    x = 1
    while stepen != 0:
        while (stepen % 2) == 0:
            stepen = stepen // 2
            number = (number * number) % modN
        stepen = stepen - 1
        x = (x * number) % modN

    return x



def dsa(*args, **data):
    """


    The procedure for signing and verifying electronic digital signature
     using the DSA algorithm, using the SHA-3 algorithm.

    :param args: the path to the file '1.txt', for example
    :param data: multiple arguments

    Usage:

        new_dsa('1.txt',q=107,p=643,x=45,k=31,mode='signature',h=2) - example

    :returns: collections:
        when signing: {'result':[y,q,k],'params':[r,s]}
        when check : {'result':[w,u1,u2],'params':[v]}
    """

    filename = args[0]

    try:

        # open file
        in_file = open(filename,'rb')
        byte_array = in_file.read()

        # import SHA-3
        from sha3 import sha3_256

        # generating hash (64 symbols in 10-em)
        hash_obj = sha3_256(byte_array)
        my_hash = int(hash_obj.hexdigest(),16)

        # get mode
        mode = data.get('mode',0)

        # main
        if mode == 'signature':
            q = data.get('q',0)
            if q != 0:

                p = data.get('p',0)
                if p != 0:

                    h = data.get('h',0)
                    if h != 0 and 1 <= h <= p - 1:

                        g = fastEXP(h, ((p - 1) / q), p)
                        if g > 1:

                            x = data.get('x',0)
                            if 0 <= x <= q:

                                y = fastEXP(g, x, p)

                                # signature
                                from random import randrange

                                k = randrange(0,q+1)
                                r = fastEXP(g, k, p) % q
                                s = fastEXP(k, q - 2, q) * ((my_hash + x * r) % q)

                                return {'result': [y,g,k],'params': [r,s], 'hash': my_hash} # {'result': True, 'params': [36,38,131]} - example

                            else:
                                return 'Wrong x!'
                        else:
                            return 'Wrong g!'
                    else:
                        return 'Wrong h!'
                else:
                    return 'Wrong p!'
            else:
                return 'Wrong q!'

        elif mode == 'check':

            q = data.get('q', 0)
            if q != 0:

                p = data.get('p', 0)
                if p != 0:

                    r = data.get('r',0)
                    if r != 0:

                        y = data.get('y',0)
                        if y != 0:

                            g = data.get('g',0)
                            if g != 0:

                                s = data.get('s',0)
                                if s != 0:

                                    w = fastEXP(s, q - 2, q)
                                    u1 = (my_hash * w) % q
                                    u2 = (r * w) % q
                                    v = (((g ** u1) * (y ** u2)) % p) % q

                                    return {'result': [w,u1,u2],'params':[v],'hash': my_hash}

                                else:
                                    return 'Wrong s!'
                            else:
                                return 'Wrong g!'
                        else:
                            return 'Wrong y!'
                    else:
                        return 'Wrong r!'


                else:
                    return 'Wrong p!'
            else:
                return 'Wrong q!'



        elif mode == 0:
            return 'Wrong mode!'


    except FileNotFoundError:
        return 'File not find.'





