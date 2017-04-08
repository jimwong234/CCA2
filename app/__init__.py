from flask import Flask

webapp = Flask(__name__)

from app import main
from app import login
from app import registration
from app import user_dashboard
from app import user_postroom
from app import user_myposts
from app import user_searchroom
from app import user_profile
