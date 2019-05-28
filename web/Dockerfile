# To pull python 3 image
FROM python:3
# Creating a Work directory
WORKDIR /usr/src/app
# copy requirements into work directory created above
COPY requirements.txt ./
# install requirements
RUN python3 -m pip install --user --no-cache-dir -r requirements.txt
# copy project into work directory
COPY . .
# Run our app
CMD [ "python", "app.py" ]