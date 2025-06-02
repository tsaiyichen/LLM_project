# AI Girlfriend System  
Final Project – Fu Jen Catholic University, Academic Year 114

This repository contains the **AI Girlfriend** system developed as a final project for the 114th academic year at **Fu Jen Catholic University**.

## 🚀 Project Setup

Follow the steps below to run the system on your local machine:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   ```
   Move the project folder to your localhost directory.

2. **Set Up MySQL Database**
   - Create a new database named: `LLM_project` in your local MySQL instance.
   - Import the `.sql` files located in the `sql/` folder into the database.

3. **Download `.env` File**
   - Download the `.env` file from the following link:  
     [Download .env](https://drive.google.com/file/d/1mynl9QlVYgV8A5xXFDopQcK4AHpH0zvQ/view?usp=sharing)
   - Place the `.env` file in the root of the project folder.

4. **Run the Flask App**
   - Open the project folder in your IDE.
   - Start the Flask server in developer mode:
     ```bash
     python app.py
     ```

5. **Access the System**
   - Open your browser and go to:  
     `http://localhost:5000`

## 🧠 System Description

- The login system is a mock-up for demo purposes — enter any username and password to proceed.
- Registration is not required and not implemented.
- Backend logic (including LangChain LLM workflow) is implemented in `app.py`.
- Frontend HTML code is located in the `templates/` folder.

## 📂 Project Structure

```
/dataset        # the dataset that fine tuning use
/sql            # SQL schema for database setup
/templates      # Frontend HTML files
app.py          # Main backend logic (Flask + LangChain)
.env           # Environment variables (API keys, DB config)
```
