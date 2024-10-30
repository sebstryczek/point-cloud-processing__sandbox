import os
import termcolor
from functools import wraps

def gray(text: str) -> str:
  return termcolor.colored(text, color="grey")


def skippable(func):
    @wraps(func)
    def wrapper(self, *args, skip=False, **kwargs):
        if skip:
            return self
        return func(self, *args, **kwargs)
    return wrapper

class Path:
  current_directory: str

  '''
  '''
  def __init__(self):
    self.current_directory = get_current_directory()

  '''
  '''
  def go_to(self, path: str):
    self.current_directory = get_absolute_path(path)
    return self
  
  '''
  '''
  def get_absolute_path(self, path: str):
    return f'{self.current_directory}/{path}';
  
  '''
  '''
  @skippable
  def log_contents(self, skip: bool = False):
    subdirectories = get_subdirectories(self.current_directory)
    files = get_files(self.current_directory)

    for subdir in subdirectories:
      print(f"-- {os.path.basename(subdir)}/")
    
    for file in files:
      print(f"-- {os.path.basename(file)}")

    return self
  
  '''
  '''
  @skippable
  def log_tree(self, skip: bool = False):
    log_tree(self.current_directory)
    return self
  
  '''
  '''
  @skippable
  def log_absolute_path(self, path: str, skip: bool = False):
    print(self.get_absolute_path(path))
    return self
  
  '''
  '''
  def end(self):
    return self
  
'''
'''
def get_current_directory():
  return os.getcwd()

'''
'''
def get_absolute_path(relative_path):
  path_array = os.path.split(relative_path)
  path = os.path.join(*path_array)
  return os.path.abspath(path)

'''
'''
def get_subdirectories(dir_path):
  arr = os.listdir(dir_path)
  sub_dirs = list(filter(lambda x: os.path.isdir(x), map(lambda x: os.path.join(dir_path, x), arr)))

  return sub_dirs

'''
'''
def log_subdirectories(directory_path: str) -> None:
    subdirectories = get_subdirectories(directory_path)

    for i, subdir in enumerate(subdirectories):
        print(f"{i+1}. {os.path.basename(subdir)}")
    print()

'''
'''
def get_files(directory_path: str):
  arr = os.listdir(directory_path)
  sub_dirs = list(filter(lambda x: os.path.isfile(x), map(lambda x: os.path.join(directory_path, x), arr)))

  return sub_dirs

'''
'''
def log_files(directory_path: str):
  files = get_files(directory_path)

  for i, file in enumerate(files):
    print(f"{i+1}. {os.path.basename(file)}")
  print()

'''
'''
def log_tree(directory_path: str, level: int = 1, skip_names: list = ["__pycache__", ".conda_env"]) -> None:
  subdirectories = get_subdirectories(directory_path)

  for subdir in subdirectories:
    if os.path.basename(subdir) in skip_names:
      continue

    print("--" * level + " " + gray(os.path.basename(subdir) + "/"))
    log_tree(subdir, level + 1, skip_names)
    
  files = get_files(directory_path)

  for file in files:
    print("--" * (level) + " " + os.path.basename(file))
