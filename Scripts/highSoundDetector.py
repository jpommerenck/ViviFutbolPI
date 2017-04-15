import os
import subprocess
import sys
import re
import time
from dateUtil import get_current_short_date_str, add_seconds_to_date, get_current_date_str, str_to_date, check_for_insert_mark, get_date_str
from fileUtil import get_wav_files_in_directory, newest_wav_in_directory
from dbUtil import get_last_mark, insert_mark


PATH_AUDIO_LOCALIZATION = '/home/pi/ViviFutbolLocal/Audios/'
SECONDS_WAITING_FOR_CONVERT_VIDEO=15
SECONDS_WAITING_FOR_ADD_NEW_MARK=5
MIN_AMPLITUD = 0.30


def main(args=None):

    try:
        var = 0
        last_newest_file = ''
        while var < 10 :
            # Ubicación de los audios para generar las marcas
            audio_path = PATH_AUDIO_LOCALIZATION + get_current_short_date_str()
            # Obtengo todos los audios no procesados
            file_array = get_wav_files_in_directory(audio_path)
            newest_file = newest_wav_in_directory(audio_path + '/')

            # Voy a ir iterando sobre los archivos para obtener las marcas
            if len(file_array) > 0 :
                for file_name in file_array:
                    # Verifico no trabajar sobre el archivo en el que se esta grabando actualmente
                    if (file_name != newest_file) | (newest_file == last_newest_file) :
                        i = 0
                        for i in range(0,14):
                            # Voy a partir el audio en varios audios de 1 segundo para calcular la max aplitud por segundo
                            file_aux = file_name.replace('.wav', "_" + str(i) + ".wav")
                            j = i+1
                            
                            os.system('sox ' + file_name + " " + file_aux + " trim " + str(i) + " " + str(j))
                            proc = subprocess.Popen(['sh','sox.sh', file_aux, '5' ], stdout=subprocess.PIPE)

                            result,errors = proc.communicate()
                            # Obtengo la amplitud para ese segundo
                            amplitude=float(result)
                            os.remove(file_aux)
                            
                            if amplitude > MIN_AMPLITUD:
                                last_mark = str_to_date(get_last_mark())
                                
                                audio_file = file_name.replace(audio_path + "/", '')
                                audio_file = audio_file.replace('.wav', '')
                                new_mark_for_insert = add_seconds_to_date(str_to_date(audio_file), i)

                                # Verifico si no se ingresó una marca anteriormente para esta jugada
                                if check_for_insert_mark(new_mark_for_insert, last_mark, SECONDS_WAITING_FOR_ADD_NEW_MARK):
                                    insert_mark(get_date_str(new_mark_for_insert))

                        os.remove(file_name)
                
            var = var + 1
            time.sleep(SECONDS_WAITING_FOR_CONVERT_VIDEO)
    except KeyboardInterrupt:
        print('Entro a la exception')
    finally:
        print('Program over')

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
