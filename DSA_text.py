from hashlib import sha1 as SHA_1


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


def isPrime(n):
    """

    The function checks whether the input parameter is a prime number.

    :param n: testing prime
    :return: True or False

    """
    from math import sqrt
    from itertools import count, islice
    if n < 2: return False
    for number in islice(count(2), int(sqrt(n) - 1)):
        if not n % number:
            return False
    return True


def dsa_sign(**kwargs):
    """

    Text file signature function based on DSA algorithm(SHA-1).

    :param kwargs: accepts p, q, h, k, x and filename;
    :return: returns an error message or result;
    """

    def check(p, q, h, x, k):
        """

        The function checks the input values ​​for correctness.

        :param p: p - prime;
        :param q: q - prime, divider of p - 1;
        :param h: h - (1,p-1];
        :param x: x - [1,q];
        :param k: k - [0,q];
        :return: error text or value tuple if everything is correct;
        """
        if (p - 1) % q == 0:
            if 1 < h < p - 1:
                g = fastEXP(h, ((p - 1) // q), p)
                if g > 1:
                    if 0 <= x <= q:
                        if 0 <= k <= q:
                            if isPrime(p) and isPrime(q):
                                y = fastEXP(g, x, p)
                                return (True, g, y)
                            else:
                                return 'P or Q is not prime.'
                        else:
                            return 'Invalid k.'
                    else:
                        return 'Invalid x.'
                else:
                    return 'Invalid g or h.'
            else:
                return 'Invalid h.'
        else:
            return 'Invalid p or q.'

    def append_data(data,r,s):
        """

        Adds a digital signature to the file.

        :param data: string file representation;
        :param r: r - int;
        :param s: s - int;
        :return: text file with digital signature;
        """
        data+='`'+str(r)+'~'+str(s)
        return data

    try:
        p = int(kwargs.get('p', 0))
        q = int(kwargs.get('q', 0))
        h = int(kwargs.get('h', 0))
        x = int(kwargs.get('x', 0))
        k = int(kwargs.get('k', 0))

    except:
        return 'Convert error.'

    check_string = check(p, q, h, x, k)
    if check_string[0] == True:

        filename = kwargs.get('filename')
        if filename is not None:
            try:
                in_file = open(filename, 'rb')
                byte_array = in_file.read()
                in_file.close()
            except:
                return 'I don\'t find file \'{}\' :('.format(filename)
            hash_obj = SHA_1(byte_array)
            my_hash = int(hash_obj.hexdigest(), 16)

            y = check_string[2]
            g = check_string[1]

            r = fastEXP(g, k, p) % q
            s = fastEXP(k, q - 2, q) * ((my_hash + x * r) % q)
            print(r,s)

            if r != 0 and s != 0:
                try:
                    in_file = open(filename, 'r')
                    data = in_file.read()
                    in_file.close()
                    in_file = open(filename, 'w')
                    in_file.write(append_data(data,r,s))
                    in_file.close()
                except:
                    return 'File error.'
                return (r, s, y, my_hash, g)
            else:
                return 'Try other k.'

    else:
        return check_string

def check_sign_dsa(**kwargs):
    """

    The function checks the electronic digital signature (DSA, SHA-1).

    :param kwargs: p,q,y...;
    :return: True or error message with explanation;
    """
    def get_rs(data):
        """

        Get digital signature from file.

        :param data: string file representation;
        :return: r,s - int; data - source file;
        """
        ind_1 = data.rfind('`')
        ind_2 = data.rfind('~')
        if ind_1 != -1 and ind_2 != -1:
            r_str = data[ind_1+1:ind_2]
            s_str = data[ind_2+1:]
        else:
            return 'File don\'t have digital signature!'
        try:
            r = int(r_str)
            s = int(s_str)
        except:
            return 'Convert error'
        data = data[:ind_1]

        return (r,s,data)

    try:
        p = int(kwargs.get('p', 0))
        q = int(kwargs.get('q', 0))
        y = int(kwargs.get('y',0))
        h = int(kwargs.get('h',0))
    except:
        return 'Convert error.'

    filename = kwargs.get('filename')

    if filename is not None:
        try:
            in_file = open(filename, 'r')
            data = in_file.read()
            in_file.close()
        except:
            return 'I don\'t find file \'{}\' :('.format(filename)
        try:
            r, s, data = get_rs(data)
        except:
            return 'File don\'t have digital signature!'

        in_file = open(filename, 'w')
        in_file.write(data)
        in_file.close()


        in_file = open(filename, 'rb')
        byte_array = in_file.read()
        in_file.close()

        in_file = open(filename, 'a')
        in_file.write('`'+str(r)+'~'+str(s))
        in_file.close()

        hash_obj = SHA_1(byte_array)
        my_hash = int(hash_obj.hexdigest(), 16)
        print(my_hash)


        g = fastEXP(h, ((p - 1) // q), p)
        w = fastEXP(s, q - 2, q)

        u1 = (my_hash * w) % q
        u2 = (r * w) % q

        v = (((g ** u1) * (y ** u2)) % p) % q
        print(r,v)
        if r == v:
            return True
        else:
            return False

    return 'File error'


#print(dsa_sign(q = 107,p = 643,h = 2,x = 45,k = 31, filename='test/1.txt'))
#print(check_sign_dsa(q=107,p=643,y=181,h=2,filename='test/1.txt'))