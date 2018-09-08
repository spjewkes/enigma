#!/usr/bin/env python

import argparse

class Rotor(object):
    def __init__(self, name, mapping, notch):
        super(Rotor, self).__init__()
        assert mapping.isalpha()
        assert notch.isalpha()

        self.name = name
        self.mapping = mapping.upper()
        self.notch = notch.upper()
        self.position = "A"
        self.ring = "A"

    @staticmethod
    def _stoi(value):
        # Converts character to integer 0-25
        assert value.isalpha() and len(value) == 1
        return ord(value.upper()) - ord("A")

    @staticmethod
    def _itos(value):
        # Converts integer to character (in range of 0 to 25)
        # Handles negative value and those greater than 25
        while (value < ord("A")):
               value += 26
        return chr(ord("A") + (value % 26))

    @property
    def position(self):
        return Rotor._itos(self._position)

    @position.setter
    def position(self, value):
        self._position = Rotor._stoi(value)

    @property
    def ring(self):
        return Rotor._itos(self._ring)

    @ring.setter
    def ring(self, value):
        assert value.isalpha()
        self._ring = Rotor._stoi(value)

    def advance(self):
        self.position = Rotor._itos(self._position + 1)

        # Does the next rotor need to advance
        if self.position in self.notch:
            return True
        else:
            return False

    def forward_mapping(self, char):
        # Convert to index 0-25 and read mapping char at this location
        return Rotor._itos(Rotor._stoi(self.mapping[(Rotor._stoi(char) + self._position - self._ring) % 26]) - self._position + self._ring)

    def reverse_mapping(self, char):
        # Find the position of the char in mapping at return its index position as a char
        return Rotor._itos(self.mapping.index(Rotor._itos(Rotor._stoi(char) + self._position - self._ring)) - self._position + self._ring)

class Reflector(object):
    def __init__(self, name, mapping):
        super(Reflector, self).__init__()
        assert mapping.isalpha()

        self.name = name
        self.ref_mapping = mapping.upper()

    def mapping(self, char):
        assert char.isalpha()
        return self.ref_mapping[ord(char.upper()) - ord("A")]

class PlugBoard(object):
    def __init__(self, mappings):
        super(PlugBoard, self).__init__()

        self._forward = dict()
        self._reverse = dict()
        
        for mapping in mappings.split():
            self._forward[mapping[0].upper()] = mapping[1].upper()
            self._reverse[mapping[1].upper()] = mapping[0].upper()

    def mapping(self, char):
        if char in self._forward:
            return self._forward[char]
        elif char in self._reverse:
            return self._reverse[char]
        else:
            return char

class Enigma(object):
    def __init__(self, rotor_1, rotor_2, rotor_3, rotor_offset, ring_setting, reflector, plugboard):
        super(Enigma, self).__init__()

        assert rotor_offset.isalpha() and len(rotor_offset) == 3
        assert ring_setting.isalpha() and len(ring_setting) == 3

        self._rotor = list()
        self._rotor.append(rotor_1)
        self._rotor.append(rotor_2)
        self._rotor.append(rotor_3)

        self._rotor_offset = rotor_offset
        self._ring_setting = ring_setting

        self._reflector = reflector
        self._plugboard = plugboard

        self._reset()

    def _reset(self):
        for i in range(3):
            self._rotor[i].ring = self._ring_setting[i]
            self._rotor[i].position = self._rotor_offset[i]

    def _encode(self, c):
        # print("Start char: {}".format(c))

        enc_c = self._plugboard.mapping(c)
        # print("Plugboard mapping: {}".format(enc_c))

        for i in range(3):
            # print("Rotor {} pre encoding: {}".format(i, enc_c))
            enc_c = self._rotor[i].forward_mapping(enc_c)
            # print("Rotor {} post encoding: {}".format(i, enc_c))

        enc_c = self._reflector.mapping(enc_c)
        # print("Reflector mapping: {}".format(enc_c))

        for i in reversed(range(3)):
            # print("Rotor {} pre encoding: {}".format(i, enc_c))
            enc_c = self._rotor[i].reverse_mapping(enc_c)
            # print("Rotor {} post encoding: {}".format(i, enc_c))

        enc_c = self._plugboard.mapping(enc_c)
        # print("Plugboard mapping: {}".format(enc_c))

        return enc_c

    def _advance(self):
        advance = True
        for i in range(3):
            if advance:
                advance = self._rotor[i].advance()

    def encode(self, test):
        encoded_string = ""

        self._reset()

        for c in test:
            if c.isalpha():
                self._advance()
                encoded_string += self._encode(c)

        return encoded_string
                
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Encrypt and decript messages using electronic version of the Enigma machine')
    parser.add_argument("--text", help="Text to process")
    parser.add_argument("-v", "--verbose", action="store_true", help="increase verbosity")
    args = parser.parse_args()

    if args.verbose:
        print("Processing text: {}".format(args.text))

    rotor_1 = Rotor("Rotor I", "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q")
    rotor_2 = Rotor("Rotor II", "AJDKSIRUXBLHWTMCQGZNPYFVOE", "E")
    rotor_3 = Rotor("Rotor III", "BDFHJLCPRTXVZNYEIWGAKMUSQO", "V")
    rotor_4 = Rotor("Rotor IV", "ESOVPZJAYQUIRHXLNFTGKDCMWB", "J")
    rotor_5 = Rotor("Rotor V", "VZBRGITYUPSDNHLXAWMJQOFECK", "Z")
    rotor_6 = Rotor("Rotor VI", "JPGVOUMFYQBENHZRDKASXLICTW", "ZM")
    rotor_7 = Rotor("Rotor VII", "NZJHGRCXMYSWBOUFAIVLPEKQDT", "ZM")
    rotor_8 = Rotor("Rotor VIII", "FKQHTLXOCBJSPDZRAMEWNIUYGV", "ZM")

    reflect_a = Reflector("Reflector A", "EJMZALYXVBWFCRQUONTSPIKHGD")
    reflect_b = Reflector("Reflector B", "YRUHQSLDPXNGOKMIEBFZCWVJAT")
    reflect_c = Reflector("Reflector C", "FVPJIAOYEDRZXWGCTKUQSBNMHL")

    plugboard = PlugBoard("")

    enigma = Enigma(rotor_3, rotor_2, rotor_1, "AAA", "BBB", reflect_b, plugboard)

    print(enigma.encode(args.text))
