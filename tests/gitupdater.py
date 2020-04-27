
from git import *


repo = Repo('../')

repo.git.reset('--hard')
repo.git.reset('--hard','origin/master')
repo.remotes.origin.pull()
print('Updated.')
