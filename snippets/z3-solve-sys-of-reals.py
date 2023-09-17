import z3

buf = [z3.Real(f'{i:02}') for i in range(24)]

solver = z3.Solver()

solver.add (buf[15] == 91.0)
solver.add (buf[18] == 91.0)
solver.add (buf[0] + buf[0] + 11.0 == buf[0] + 130.0)
solver.add (buf[23] + buf[23] + 6.0 == buf[23] + 127.0)
solver.add (buf[1] * 7.0 == buf[1] + 396.0)
solver.add (buf[22] == 104.0)
solver.add ((buf[2] + 2.0) * 3.0 - 2.0 == (buf[2] - 17.0) * 4.0)
solver.add (buf[21] == (buf[21] + buf[21]) - 44.0)
solver.add (buf[3] == 67.0)
solver.add ((buf[20] * 3.0 - 2.0) * 3.0 - (buf[20] * 5.0 + 2.0) * 4.0 == buf[20] * -8.0 - 146.0)
solver.add ((buf[4] * 5.0 - 2.0) * 5.0 - (buf[4] + buf[4] + 7.0) * 6.0 == buf[4] * 33.0 - 1132.0)
solver.add (buf[19] == (buf[3] + buf[20]) - 16.0)
solver.add ((buf[5] + buf[5]) / 3.0 == (buf[5] + 44.0) / 3.0)
solver.add (buf[17] == 49.0)
solver.add ((buf[6] * 8.0 + 15.0) * 0.1666666666666667 == (buf[6] + buf[6] + 81.0) * 0.5)
solver.add (0.0 - buf[16] / 5.0 == 36.0 - buf[16])
solver.add ((buf[7] * 7.0) / 2.0 == buf[7] * 3.0 + 23.5)
solver.add (buf[14] == buf[14] / 2.0 + 48.0)
solver.add (buf[8] == 110.0)
solver.add (buf[13] == buf[14] / 2.0 - 1.0)
solver.add (buf[9] == 104.0)
solver.add (buf[12] == buf[11])
solver.add (buf[11] == 108.0)
solver.add (buf[10] == 48.0)

assert solver.check() == z3.sat
m = solver.model()

word = ''
for el in buf:
    evaluation = m.evaluate(el)
    value = round(float(evaluation.as_fraction()))
    word += chr(value)
        
print('The word is:', word)
