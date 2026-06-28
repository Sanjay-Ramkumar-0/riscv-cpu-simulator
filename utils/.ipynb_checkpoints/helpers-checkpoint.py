{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 17,
   "id": "180286a9-8716-4632-b8df-91c5e5fc2801",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "' note: all the inputs and outputs are int '"
      ]
     },
     "execution_count": 17,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "\"\"\" note: all the inputs and outputs are int \"\"\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "c661558b-c2f9-4231-a9de-93c930bc694e",
   "metadata": {},
   "outputs": [],
   "source": [
    "def mask64(value):\n",
    "    \"\"\" to keep only lower 64 bits\"\"\"\n",
    "    return value & 0*FFFFFFFFFFFFFFFF"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "22425f42-c940-4301-bd63-39f8a2949399",
   "metadata": {},
   "outputs": [],
   "source": [
    "def sign_extend(value,bits):\n",
    "    \"\"\" for sign extension, converting width binary number (like a 4-bit or 16-bit integer) into a wider format preserving the sign\"\"\"\n",
    "    sign_bit = 1 << (bits - 1) \n",
    "    \"\"\" ex: when the bits is 4, then it's sign bit is 1000\"\"\"\n",
    "    return (value & (sign_bits-1) - (value & sign_bit))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "33f15ba2-e9e1-4e36-8e4a-4587b1176e38",
   "metadata": {},
   "outputs": [],
   "source": [
    "def zero_extend(value,bits):\n",
    "    return value&((1<bits)-1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "fa449011-04d4-4d01-a151-7ed9a072ca8f",
   "metadata": {},
   "outputs": [],
   "source": [
    "def get_bits(value,high,low):\n",
    "    \"\"\" slicing the required bits\"\"\"\n",
    "    mask = (1 << (high-low+1)) - 1\n",
    "    return (value >> low) & mask"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "515657a2-3228-4371-8773-8afa7cb084c4",
   "metadata": {},
   "outputs": [],
   "source": [
    "def bit(value,position):\n",
    "    \"\"\" returns single bit \"\"\"\n",
    "    return (value>>position) & 1"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "id": "3164512b-6fc0-4dfd-8629-567c073fbb1a",
   "metadata": {},
   "outputs": [],
   "source": [
    "def is_aligned(address,alignment):\n",
    "    \"\"\"\n",
    "    Check address alignment.\n",
    "\n",
    "    Example:\n",
    "        is_aligned(0x1000, 8) -> True\n",
    "        is_aligned(0x1003, 8) -> False\n",
    "    \"\"\"\n",
    "    \n",
    "    return (address % alignment) == 0\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "id": "cf8b2ea0-8f51-4cf4-8063-02bbffa54bd6",
   "metadata": {},
   "outputs": [],
   "source": [
    "def to_signed(value,bits):\n",
    "    \"\"\" to convert the unsigned integer to signed integer\"\"\"\n",
    "    sign_bit = 1 <<(bits - 1)\n",
    "    if value & sign_bit:\n",
    "        return value - (1<<bits)\n",
    "    return value"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "id": "71ff8343-ecbe-4081-88f3-73f430b0f5e3",
   "metadata": {},
   "outputs": [],
   "source": [
    "def to_unsigned(value, bits):\n",
    "    \"\"\"\n",
    "    Convert signed integer to unsigned integer.\n",
    "    \"\"\"\n",
    "    return value & ((1 << bits) - 1)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.13"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
