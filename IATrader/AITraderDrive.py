'''from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials'''
import datetime

class Drive:
    def __init__(self, name):
        '''self.auth.authenticate_user()
        self.gauth = GoogleAuth()
        self.gauth.credentials = GoogleCredentials.get_application_default()
        self.drive = GoogleDrive(self.gauth)'''

        self.name = name

    '''def save_drive(self, model):
        title = f'{self.name}{datetime.datetime.now()}.h5'
        model.save(title)
        model_file = self.drive.CreateFile({'title': title})
        model_file.SetContentFile(title)
        model_file.Upload()'''

    def save_folder(self, model):
        model.save(f'models/{self.name}.h5')

    def open_folder(self, load_model):
        return load_model(f'models/{self.name}.h5')