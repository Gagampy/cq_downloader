import os
import datetime
import json
import CQ
from config import params_dict, download_path


def download_records():
    with CQ.Api(host_api, port_api, 'cardio-account-3293.pem') as api:  # сертификат Исследователя

        # Создание папки data, в которой будут содержаться записи:
        if 'data' not in os.listdir(download_path or os.getcwd()):
            os.mkdir('data')
        os.chdir('data')

        global prev_id
        # Читаем нужные нам записи:
        params_dict['id'] = prev_id

        params = [k + '=' + str(v) for k, v in params_dict.items()]
        params = '&'.join(params)

        for c in api.all(f'/cardiogram?{params}'):
            print('C:', c)
            print('{0}\t{1}'.format(c['id'], datetime.datetime.fromtimestamp(c['date']).strftime(
                '%d.%m.%Y %H:%M:%S')))  # unix timestamp -> дата записи ЭКГ

            prev_id = c['id']

            t = api.get('/token/{0}'.format(c['id']))  # токен на чтение треков
            with CQ.Cloud(host_cloud, port_cloud) as cloud:
                wav_ecg = cloud.get('/file/{0}/100'.format(c['id']), t['token'])  # читаем файл ECG в буфер
                wav_ppg = cloud.get('/file/{0}/200'.format(c['id']), t['token'])  # читаем файл PPG в буфер

            with open('last_record_id.txt', 'w') as f:
                    f.write(str(prev_id))

            # Если есть пара ECG + PPG, загружаем:
            if wav_ecg != None and wav_ppg != None:

                # Создание папок ecg, ppg и rr:
                if 'ecg' not in os.listdir():
                    os.mkdir('ecg')

                if 'ppg' not in os.listdir():
                    os.mkdir('ppg')

                if 'rr' not in os.listdir():
                    os.mkdir('rr')

                # Получение меток давления:
                if 'bloodPressureSystolic' in c.keys() and 'bloodPressureDiastolic' in c.keys():
                    sp = c['bloodPressureSystolic']
                    dp = c['bloodPressureDiastolic']
                else:
                    # if there are no sp and dp use this placeholders:
                    sp = 'x'
                    dp = 'x'

                # Сохранение ЭКГ:
                with open('ecg/{0}-{1}-1K-raw-{2}-{3}.wav'.format(c['id'], c['accountId'], sp, dp), 'wb') as f:
                    f.write(wav_ecg)

                # Сохранение ППГ:
                with open('ppg/{0}-{1}-1K-pgg-{2}-{3}.wav'.format(c['id'], c['accountId'], sp, dp), 'wb') as f:
                    f.write(wav_ppg)  # сохраним на диск

                # Cохранение RR:
                rr = api.first('/analysis/{0}/rr'.format(c['id']))  # RR интервалы
                if rr == None or 'error' in rr and rr['error'] != 0: continue  # пропускаем плохие

                with open('rr/{0}-{1}-rr.json'.format(c['id'], c['accountId']), 'w') as f:
                    json.dump(rr, f)  # сохраним на диск

            # Пропускаем, если пары нет:
            else:
                continue


host_api = 'b-api.cardioqvark.ru'
port_api = 1443
host_cloud = 'b-g2.cardioqvark.ru'
port_cloud = 443
prev_id = params_dict['minId']

#while True:
#    try:
download_records()
#    except:
#        print('Что-то случилось, но всё кулл.')

