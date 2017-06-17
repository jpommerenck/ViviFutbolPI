import os
import subprocess
import sys
import re
import time
from dateUtil import get_current_short_date_str, add_seconds_to_date, get_current_date_str, str_to_date_time, check_for_insert_mark, get_date_str, get_current_time_int
from fileUtil import get_wav_files_in_directory, newest_wav_in_directory
from dbUtil import get_last_mark, insert_mark, get_config_value
from logger import log_error


def main(args=None):
    try:
        PATH_AUDIO_LOCALIZATION = get_config_value("AUDIOS_LOCALIZATION_PATH")
        SECONDS_WAITING_FOR_CONVERT_VIDEO = int(get_config_value("SECONDS_WAITING_FOR_CONVERT_VIDEO"))
        SECONDS_WAITING_FOR_ADD_NEW_MARK = int(get_config_value("SECONDS_WAITING_FOR_ADD_NEW_MARK"))
        MIN_AMPLITUD = 0.30
        SECONDS_WAITING_FOR_CONVERT_VIDEO = int(get_config_value("SECONDS_WAITING_FOR_CONVERT_VIDEO"))

        START_RECORDING_TIME = get_config_value("START_RECORDING_TIME")
        FINISH_RECORDING_TIME = get_config_value("FINISH_RECORDING_TIME")
        
        START_RECORDING_TIME = START_RECORDING_TIME.replace(":","")
        START_RECORDING_TIME = int(START_RECORDING_TIME.replace(":",""))

        FINISH_RECORDING_TIME = FINISH_RECORDING_TIME.replace(":","")
        FINISH_RECORDING_TIME = int(FINISH_RECORDING_TIME.replace(":",""))

        current_time = get_current_time_int()
        while (current_time >= START_RECORDING_TIME) & (current_time <= FINISH_RECORDING_TIME):
            last_newest_file = ''
            
            # Ubicación de los audios para generar las marcas
            audio_path = PATH_AUDIO_LOCALIZATION + get_current_short_date_str() + "/Aux"
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
                            file_aux = file_name
                            file_aux = file_aux.replace('.wav', "_" + str(i) + ".wav")
                            j = i+1
 
                            os.system('sox ' + file_name + " " + file_aux + " trim " + str(i) + " " + str(j))
                            proc = subprocess.Popen(['sh','sox.sh', file_aux, '5' ], stdout=subprocess.PIPE)

                            result,errors = proc.communicate()
                            # Obtengo la amplitud para ese segundo
                            if (result != ''):
                                amplitude=float(result)
                                os.remove(file_aux)
                                    
                                if amplitude > MIN_AMPLITUD:
                                    print('obtuve una buena amplitud')
                                    audio_file = file_name.replace(audio_path + "/", '')
                                    audio_file = audio_file.replace('.wav', '')
                                    new_mark_for_insert = add_seconds_to_date(str_to_date_time(audio_file), i)
                                        
                                    if get_last_mark()!='':
                                        
                                        last_mark = str_to_date_time(get_last_mark())
                                        # Verifico si no se ingresó una marca anteriormente para esta jugada
                                        if check_for_insert_mark(new_mark_for_insert, last_mark, SECONDS_WAITING_FOR_ADD_NEW_MARK):
                                            insert_mark(get_date_str(new_mark_for_insert))
                                    else:
                                        insert_mark(get_date_str(new_mark_for_insert))

                    os.remove(file_name)
                    file_array = get_wav_files_in_directory(audio_path)
                    
            time.sleep(SECONDS_WAITING_FOR_CONVERT_VIDEO)
            current_time = get_current_time_int()
    except KeyboardInterrupt as e:
        log_error("SYSTEM", 'SYSTEM', 'highSoundDetector.py - main()', str(e))
    finally:
        print('Program over')

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
