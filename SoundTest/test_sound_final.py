import os
import subprocess
import sys
import re
import time

def main(args=None):

    try:
        #while True:
            filename = "/home/pi/ViviFutbolPI/SoundTest/prueba_alto.wav"
            i = 0
            for i in range(0,14):
                file_aux = "/home/pi/ViviFutbolPI/SoundTest/prueba_alto_" + str(i) + ".wav"
                j = i+1

                os.system('sox ' + filename + " " + file_aux + " trim " + str(i) + " " + str(j))

                proc = subprocess.Popen(['sh','sox.sh', file_aux, '5' ], stdout=subprocess.PIPE)
                result,errors = proc.communicate()
                amplitude=float(result)
                os.system('rm '+ file_aux)

                if amplitude > 0.15:
                    print('Sound detected')
                    #os.rename(filename, "data/" + filename)
                else:
                    print('No sound detected')
                    #os.remove(filename)

                #i = i+1
    except KeyboardInterrupt:
        print('')
    finally:
        print('Program over')

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
