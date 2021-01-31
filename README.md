# P04
Project that integrates Web Development, DB and Machine Learning.

### Objective
The purpose of this project was to make inferences using machine learning models with data entered manually through a Web App, and that these are stored in a database in order to show them as a register.

### Solution
Since the main goal was not to create a complicated model, the Iris dataset was used as a demo.
For the Web App, the Flask library was chosen, due to its simplicity; and a little of Boostrap for design. The database used was PostgresSQL, from which it was connected using SQLAlchemy. Finally, a Decision Tree model was previously trained, whose weight is found in resources (*res/model.pkl*)

### Results
The Web App has an inference page which has a list of registers which have been added from this interfece. It has also a button to **edit** some register and get an updated predicted class, as well as a button to **delete** any register.

![Alt text](imgs/WebApp.PNG?raw=true "Inference Page")
