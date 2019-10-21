"""

This is a config file for test.py for CQ API.

It defines filters used for record downloading.
These filters are the API params for a cardiogram object's method GET,
can be found there: http://wiki.cardioqvark.ru/index.php?title=API:cardiogram:GET

Also they are listed below:

id: Integer - id записи (опционально) в URL
accountId: Integer - id учетной записи пациента (опционально) в параметрах URL
desc: Integer - сортировка по возрастанию ( 0 - по умолчанию ) или убыванию ( 1 ) (опционально) в параметрах URL
deviceSerial: String - серийный номер устройства (опционально) в параметрах URL, можно указать несколько раз для поиска по ИЛИ
lead: Lead - отведение тела, с которого снималась кардиограмма
maxBloodPressureDiastolic: Integer - максимальное диастолическое артериальное давление (опционально) в параметрах URL
minBloodPressureDiastolic: Integer - минимальное диастолическое артериальное давление (опционально) в параметрах URL
maxBloodPressureSystolic: Integer - максимальное систолическое артериальное давление (опционально) в параметрах URL
minBloodPressureSystolic: Integer - минимальное систолическое артериальное давление (опционально) в параметрах URL
mахDate: Integer - максимальная дата снятия сигнала (Unix Timestamp) (опционально) в параметрах URL
minDate: Integer - минимальная дата снятия сигнала (Unix Timestamp) (опционально) в параметрах URL
maxDuration: Integer - максимальная длительность записи (сек.) (опционально) в параметрах URL
minDuration: Integer - минимальная длительность записи (сек.) (опционально) в параметрах URL
maxGlucose: Float - максимальный уровень концентрации глюкозы в крови (опционально) в параметрах URL
minGlucose: Float - минимальный уровень концентрации глюкозы в крови (опционально) в параметрах URL
maxId: Integer - максимальный id результата (опционально) в параметрах URL
minId: Integer - минимальный id результата (опционально) в параметрах URL
maxTs: Integer - максимальная дата изменения в БД (Unix Timestamp) (опционально) в параметрах URL
minTs: Integer - минимальная дата изменения в БД (Unix Timestamp) (опционально) в параметрах URL
order: String - сортировка результата ( id - по умолчанию | date | ts ) (опционально) в параметрах URL
sampleRate: Integer - частота записи (Гц) (опционально) в параметрах URL
type: CardiogramType - тип записи (опционально) в параметрах URL
Range: items=[range_start]-[range_end] - в заголовке HTTP запроса (опционально, по умолчанию items=0-19) (допустимые размеры выборки от 10 до 100)
"""

params_dict = {
    'minId': 60000,                      # min id of a record
    #'maxId': 100331,                    # max id of a record
    'minDuration': 180,              # every record with a duration min 180 secs
    'sampleRate': 1000,              # with Fs = 1000 Hz
    'minBloodPressureDiastolic': 1,  # with diastolic blood pressure measurement >= 1!
    'minBloodPressureSystolic': 1,   # with systolic blood pressure measurement >= 1!
    'CardiogramType': 1,             # ECG + PPG
}

download_path = None  # Path to download records, if None downloading will be into the project's folder


with open('data/last_record_id.txt', 'r') as f:
    params_dict['minId'] = f.readline()
print(params_dict)



