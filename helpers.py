import time,urllib,requests,os
def create_dir(path):
    if not folder_exist(path):
        os.makedirs(path)
        return True
    return False
def folder_exist(path):
    return os.path.exists(path)

def count_files(path):
    return len([name for name in os.listdir(path) if os.path.isfile(name)])

def fetch_url(url,retries=3):
    #Error flag
    error_audio = True
    retries_in = 0
    while error_audio and retries_in < retries:
        try:
            # Fetch the url
            data = requests.get(url, timeout=1)
            error_audio = False
            retries_in = 0
        except:
            error_audio = True
            retries_in +=1
            time.sleep(0.3)

    return data

def download(url, save_path):
    #download('https://www.larousse.fr/dictionnaires-prononciation/francais/tts/82294fra2', 'file.mp3')
    try:
        # This because the url contains redirection and allow_redirect didn't work.
        r = fetch_url(url)
        file = fetch_url(r.url)
        with open(save_path, 'wb') as f:
            f.write(file.content)
        return True
    except:
        return False
    

def printProgressBar (iteration, total, prefix= '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                        (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()
