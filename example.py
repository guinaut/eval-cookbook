import os
from okareo import Okareo

OKAREO_API_KEY = os.getenv("OKAREO_API_KEY")

okareo = Okareo(OKAREO_API_KEY)

projects = okareo.get_projects()
print(f"Found {len(projects)} projects:")